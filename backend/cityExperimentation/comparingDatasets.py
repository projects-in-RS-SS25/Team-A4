import pandas as pd

# User for MatchingEngine.

reviews_df = pd.read_csv("../../Team-A4/data/train.csv")
world_cities = pd.read_csv("../../Team-A4/data/worldcities.csv")

review_countries = set(reviews_df['accommodation_country'].dropna().str.strip().unique())
city_countries = set(world_cities['country'].dropna().str.strip().unique())

in_reviews_not_in_cities = sorted(review_countries - city_countries)
in_cities_not_in_reviews = sorted(city_countries - review_countries)

print("Countries in reviews but NOT in world cities dataset:")
for country in in_reviews_not_in_cities:
    print(f"- {country}")

print("\nCountries in world cities dataset but NOT in reviews dataset:")
for country in in_cities_not_in_reviews:
    print(f"- {country}")

print(f"\nTotal in reviews: {len(review_countries)}")
print(f"Total in world cities: {len(city_countries)}")
print(f"Review-only countries: {len(in_reviews_not_in_cities)}")
print(f"City-only countries: {len(in_cities_not_in_reviews)}")
