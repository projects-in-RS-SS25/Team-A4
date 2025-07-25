import pandas as pd
import re
from collections import defaultdict, Counter
from tqdm import tqdm
import csv
import os
import time

# MatchingEngine is used for building the accommodation_cities.csv file.


def load_city_data(worldcities_path):
    world_cities = pd.read_csv(worldcities_path)

    cities_by_country = defaultdict(set)

    for _, row in world_cities.iterrows():
        country = row['country']
        city = row['city']

        if pd.notnull(country) and pd.notnull(city):
            if country == "United States":     # These differences were identified using comparingDatasets.py
                country = "United States of America"
            elif country == "Czechia":
                country = "Czech Republic"
            elif country == "North Macedonia":
                country = "Macedonia"
            cities_by_country[country].add(city.lower())
    """
    for _, row in us_cities.iterrows():
        city = row['city']
        if pd.notnull(city):
            cities_by_country["United States of America"].add(city.lower())
    """
    return cities_by_country


def filter_ambiguous_cities(cities_by_country):
    ambiguous_city_names = {
        "nice", "friendly", "beach", "of", "street", "sound", "view", "garden", "west", "east",
        "north", "south", "bay", "city", "center", "central", "mountain", "valley", "lake",
        "price", "short", "home", "box", "ocean", "continental", "airport", "many", "house", "happy", "comfort",
        "north beach", "south beach", "long island", "ocean beach", "oasis", "cook", "jamaica", "cool",
        "lake view", "independence", "hills", "bath", "day", "park", "long", "union", "king", "early",
        "ocean view", "rich", "interior", "bar", "worth", "roll", "deal", "much", "ferry", "felt",
        "northern", "western", "eastern", "southern", "between", "keys", "guys", "young", "hilton",
        "holiday", "learned", "universal", "mcdonald", "wall", "paradise", "island", "tea", "coffee", "surprise",
        "sisters", "grill", "twin", "walls", "gas", "toast", "key", "guy", "point", "campus", "green", "pillow",
        "white", "champaign", "hurricane", "welcome", "celebration", "lucky", "hampton", "monument", "sale",
    }

    for country in cities_by_country:
        cities_by_country[country] -= ambiguous_city_names


def apply_manual_fixes(cities_by_country):

    cities_by_country["Israel"].add("tel aviv")

    cities_by_country["Greece"].update({
        "athens", "thessaloniki", "patras", "heraklion", "chania", "rhodes", "corfu",
        "volos", "ioannina", "kavala", "kalamata", "larisa", "samos", "kos", "naxos",
        "paros", "mykonos", "santorini", "crete", "sifnos", "thassos", "zakynthos", "lefkas",
        "alexandroupoli", "skiathos", "skopelos", "nafpaktos", "kastoria", "metsovo"
    })
    cities_by_country["Italy"].update({
        "capri", "ischia", "procida", "elba", "pantelleria", "aeolian islands", "stromboli", "lipari",
        "etna", "vesuvius", "amalfi coast", "cinque terre", "lake como", "lake garda", "lake maggiore",
        "dolomites", "val d'orcia", "chianti", "ligurian coast", "trentino", "south tyrol", "sicily", "sardinia",
        "calabria", "puglia", "umbria", "tuscany", "lazio", "campania", "veneto",
        "lombardy", "emilia-romagna", "sicily"
    })
    cities_by_country["Spain"].update({
        "mallorca", "majorca", "menorca", "minorca", "ibiza", "formentera", "tenerife", "gran canaria", "lanzarote",
        "fuerteventura", "la palma", "la gomera", "canary islands", "balearic islands", "costa brava",
        "costa del sol", "costa blanca", "andalusia", "catalonia", "basque country", "la rioja",
        "galicia", "castile and leon", "castile-la mancha", "valencia region",
        "pyrenees", "sierra nevada", "alpujarras", "camino de santiago", "ronda gorge", "montserrat",
        "el teide", "doñana", "tabernas desert", "cabo de gata", "cap de creus", "picos de europa", "costa dorada"
    })

    cities_by_country["United States of America"].update({
        "nyc", "grand canyon", "yellowstone", "yosemite", "zion", "arches", "bryce canyon", "glacier",
        "rocky mountain", "great smoky mountains", "acadia", "death valley", "joshua tree",
        "everglades", "mount rainier", "redwood", "badlands", "canyonlands", "sequoia", "olympic",
        "maui", "oahu", "kauai", "big island", "key west", "florida keys", "cape cod",
        "outer banks", "hilton head", "myrtle beach", "gulf shores", "jersey shore",
        "naples beach", "panama city beach", "virgin islands",
        "new england", "pacific northwest", "midwest", "deep south", "rocky mountains", "appalachia",
        "napa valley", "sonoma", "hudson valley", "adirondacks", "catskills", "great plains",
        "ozarks", "texas hill country", "finger lakes", "lake tahoe", "lake george", "niagara falls",
        "disney world", "disneyland", "universal studios", "las vegas strip", "hollywood",
        "mackinac island", "block island", "martha's vineyard", "nantucket", "lake michigan",
        "lake superior", "lake huron", "lake erie", "lake powell", "lake havasu",
        "aspen", "vail", "jackson hole", "mammoth", "lake placid", "killington",
        "route 66", "blue ridge parkway", "skyline drive", "big sur", "sedona", "santa fe",
        "pigeon forge", "gatlinburg", "branson", "south padre island", "bar harbor"
    })


def load_and_prepare_reviews(review_path):
    reviews_df = pd.read_csv(review_path)
    reviews_df['all_text'] = (reviews_df[['review_title', 'review_positive', 'review_negative']]
                              .fillna('').agg(' '.join, axis=1))
    reviews_df['all_text'] = reviews_df['all_text'].str.lower()
    reviews_df['accommodation_country'] = reviews_df['accommodation_country'].fillna('')
    return reviews_df


def build_city_matchers(cities_by_country):
    sorted_cities_cache = {}
    regex_cache = {}
    for country, cities in cities_by_country.items():
        sorted_cities = sorted(cities, key=len, reverse=True)
        sorted_cities_cache[country] = sorted_cities
        regex_cache[country] = [re.compile(rf'\b{re.escape(city)}\b') for city in sorted_cities]
    return sorted_cities_cache, regex_cache


def match_cities_to_reviews(filtered_reviews, cities_by_country):
    sorted_cities_cache, regex_cache = build_city_matchers(cities_by_country)
    results = {}

    for acc_id, group in filtered_reviews.groupby('accommodation_id'):
        country = group['accommodation_country'].iloc[0].strip()
        if not country:
            results[acc_id] = ("none", 0)
            continue

        sorted_cities = sorted_cities_cache.get(country, [])
        regexes = regex_cache.get(country, [])

        if not sorted_cities or not regexes:
            results[acc_id] = ("none", 0)
            continue

        city_mentions = []
        text = group['all_text'].str.cat(sep=' ')

        for pattern, city in zip(regexes, sorted_cities):
            count = len(pattern.findall(text))
            city_mentions.extend([city] * count)

        counter = Counter(city_mentions)
        if counter:
            most_common_city, count = counter.most_common(1)[0]
            results[acc_id] = (most_common_city.title(), count)
        else:
            results[acc_id] = ("none", 0)

    return results


def export_results_to_csv(all_reviews, cities_by_country, output_path, batch_size=1000):
    grouped = all_reviews.groupby('accommodation_id')
    batch_keys = list(grouped.groups.keys())

    processed_ids = set()
    if os.path.exists(output_path):
        try:
            processed_df = pd.read_csv(output_path, usecols=['accommodation_id'])
            processed_ids = set(processed_df['accommodation_id'].unique())
        except Exception:
            processed_ids = set()

    if not os.path.exists(output_path):
        with open(output_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["accommodation_id", "accommodation_country", "accommodation_city", "mention_count"])

    remaining_ids = [id for id in batch_keys if id not in processed_ids]

    total_matched = 0
    total_processed = 0
    start_time = time.time()

    for i in tqdm(range(0, len(remaining_ids), batch_size), desc="Processing batches"):
        batch_ids = remaining_ids[i:i + batch_size]
        batch_df = all_reviews[all_reviews['accommodation_id'].isin(batch_ids)].copy()
        results = match_cities_to_reviews(batch_df, cities_by_country)

        rows = []
        matched_in_batch = 0
        for acc_id in batch_ids:
            acc_group = batch_df[batch_df['accommodation_id'] == acc_id]
            acc_country = acc_group['accommodation_country'].iloc[0]
            city, count = results.get(acc_id, ("none", 0))
            if city != "none":
                matched_in_batch += 1
            rows.append([acc_id, acc_country, city, count])

        total_matched += matched_in_batch
        total_processed += len(batch_ids)

        pd.DataFrame(rows).to_csv(output_path, mode='a', index=False, header=False)

        print(
            f"Batch {i // batch_size + 1}: matched {matched_in_batch}/{len(batch_ids)} "
            f"({(matched_in_batch / len(batch_ids)) * 100:.1f}%)")

    elapsed = time.time() - start_time
    print(f"\nSummary: matched {total_matched}/{total_processed} "
          f"accommodations ({(total_matched / total_processed) * 100:.1f}%) in {elapsed:.1f} seconds")


def main():
    worldcities_path = "../data/worldcities.csv"
    # uscities_path = "data/uscities.csv"
    review_path = "../data/train.csv"
    output_path = "../data/accommodation_cities.csv"

    cities_by_country = load_city_data(worldcities_path)
    filter_ambiguous_cities(cities_by_country)
    apply_manual_fixes(cities_by_country)
    all_reviews = load_and_prepare_reviews(review_path)
    export_results_to_csv(all_reviews, cities_by_country, output_path)


if __name__ == "__main__":
    main()
