import math
from sentence_transformers import SentenceTransformer
from pyabsa import ATEPCCheckpointManager
import ollama
import faiss
import numpy as np
import pandas as pd
import torch
import os
import pickle
from collections import defaultdict
import heapq
import re
import json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
base_dir = os.path.dirname(os.path.abspath(__file__))
absa_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
absa_extractor = ATEPCCheckpointManager.get_aspect_extractor(checkpoint='multilingual')
aspects_const = [
    'Room Comfort', 'Bed', 'Decoration', 'View', 'Clean', 'Noise',
    'Elevator', 'Food', 'Internet', 'Value of Money', 'Location',
    'Flexibility', 'Security', 'Parking', 'Pool', 'Staff', 'Activity',
    'Service', 'Air Conditioner', 'Bath'
]
aspect2idx = {aspect: idx for idx, aspect in enumerate(aspects_const)}
aspect2idx.update({
    "transport": 10, "transportation": 10, "metro": 10, "subway":10, "tram":10, "taxi": 10, "access": 10, "bus": 10,
    "receptionist": 15, "front desk": 15, "host": 15, "manager": 15, "assist": 17, "support": 17, "communication": 15, "offer": 17, "owner": 15,
    "floor": 4, "wall": 4, "dirt": 4, "dust": 4, "hair": 4,
    "room": 0, "rooms" : 0, "suite": 0, "space": 0, "windows": 0,
    "breakfast": 7, "breakfasts": 7, "dinner": 7, "restaurant": 7, "meal": 7, "meals": 7, "menu": 7, "buffet": 7, "drink": 7, "drinks": 7, "cafe": 7, "cafes": 7, "kitchen": 7, "bar":7, "supper": 7, "brunch": 7,
    "price": 9, "money": 9, "expensive": 9,
    "check in": 11, "check out": 11, "check-in": 11, "check-out": 11, "reservation": 11,
    "safety": 12, "lock": 12,
    "ac": 18, "fan": 18, "fans": 18, "heat": 18, "heats": 18, "aircon": 18, "airconditioner": 18,
    "bathroom": 19, "bathrooms": 19, "shower": 19, "bathtub": 19, "toilet": 19, "sink": 19, "hairdryer": 19, "mirror": 19, "water": 14, "robes": 19,
    "balcony": 3, "mountain": 3, "ocean": 3, "sea": 3, "garden": 3, "landscape": 3, "panorama": 3,
    "spacious": 0, "large": 0, "well-equipped": 0, "modern": 2, "modernly furnished": 2,
    "authentic": 2, "central": 10, "convenient": 10, "walking distance": 10, "close to": 10,
    "scraping": 5, "loud": 5, "noisy": 5, "quiet": 5,
    "friendly": 15, "kind": 15, "helpful": 15,
    "dirty": 4, "not clean": 4,
    "suitable for family": 16, "family": 16,
    "well laid out": 2, "lake": 3,
})
def load_reviews(dataset_path=os.path.join(base_dir, 'data', 'train.csv'), cache_path=os.path.join(base_dir, 'data', "reviews.pkl")):
    reviews = []
    if os.path.exists(cache_path):
        # Load if there is the cache document for reviews exists:
        with open(cache_path, "rb") as f:
            reviews = pickle.load(f)
    else:
        # Create and save the dictionary for reviews, to reduce the processing time:
        df = pd.read_csv(dataset_path)
        for _, row in df.iterrows():
            review = {
                "title": row["review_title"],
                "positive": row["review_positive"],
                "negative": row["review_negative"],
                "full_text": f"{row['review_title']}:{row['review_positive']};{row['review_negative']}",
                "score": row["review_score"],
                "helpful": row["review_helpful_votes"],
                "guest_type": row["guest_type"],
                "guest_country": row["guest_country"],
                "room_nights": row["room_nights"],
                "month": row["month"],
                "accommodation_id": row["accommodation_id"],
                "accommodation_type": row["accommodation_type"],
                "accommodation_score": row["accommodation_score"],
                "accommodation_country": row["accommodation_country"],
                "accommodation_star_rating": row["accommodation_star_rating"],
                "location_is_beach": row["location_is_beach"],
                "location_is_ski": row["location_is_ski"],
                "location_is_city_center": row["location_is_city_center"]
            }
            reviews.append(review)
        with open(cache_path, "wb") as f:
            pickle.dump(reviews, f)
    return reviews

def categorize_nights(n):
    if n == 1:
        return 0
    elif n == 2:
        return 1
    elif 3 <= n <= 4:
        return 2
    elif 5 <= n <= 10:
        return 3
    else:
        return 4

def load_embedding(embedder, reviews, cache_path=os.path.join(base_dir, 'data', "embedding.npy")):
    # Load if there is the cache document for embedding exists:
    if os.path.exists(cache_path):
        embedding = np.load(cache_path)
    else:
        # Create and save the vector list for embedded reviews, to reduce the processing time:
        embedding = embedder.encode([review["full_text"] for review in reviews], convert_to_numpy=True, normalize_embeddings=True)
        np.save(cache_path, embedding)
    return embedding

def load_absa(dataset_path=os.path.join(base_dir, 'data', 'ABSA_results.csv'), sep = "㏦", cache_path=os.path.join(base_dir, 'data', "absa.pkl")):
    if(os.path.exists(cache_path)):
        with open(cache_path, "rb") as f:
            absa = pickle.load(f)
    else:
        if(os.path.exists(dataset_path)):
            df_absa = pd.read_csv(dataset_path, sep=sep)
            absa = df_absa[aspects_const].values.tolist()
            with open(cache_path, 'wb') as f:
                pickle.dump(absa, f)
        else: return None
    return absa

def load_aspect_vectors(cache_path=os.path.join(base_dir, 'data', "absa_vectors.pkl")):
    if(os.path.exists(cache_path)):
        with open(cache_path, "rb") as f:
            aspect_vectors = pickle.load(f)
    else:
        aspect_vectors = absa_model.encode(aspects_const, batch_size=32, normalize_embeddings=True)
        with open(cache_path, 'wb') as f:
            pickle.dump(aspect_vectors, f)
    return aspect_vectors
def get_relation(dataset_path=os.path.join(base_dir, 'data', 'train.csv'), accommodations_path=os.path.join(base_dir, 'data', 'accommodations.csv'), cache_path=os.path.join(base_dir, 'data', "relations.pkl")):
    if os.path.exists(cache_path):
        # Load if there is the cache document for relations from accommodation ids to reviews exists:
        with open(cache_path, "rb") as f:
            id_to_reviews = pickle.load(f)
    else:
        df = pd.read_csv(dataset_path)
        id_to_reviews = defaultdict(list)
        for idx, aid in enumerate(df['accommodation_id']):
            id_to_reviews[aid].append(idx)
        with open(cache_path, "wb") as f:
            pickle.dump(id_to_reviews, f)
    if os.path.exists(accommodations_path):
        # Load if there is the cache document for characteristics of accommodations exists:
        accommodations = pd.read_csv(accommodations_path)
    else:
        df = pd.read_csv(dataset_path)
        accommodations = df.groupby('accommodation_id').agg({
            'accommodation_score': 'first',
            'accommodation_star_rating': 'first',
            'location_is_ski': 'first',
            'location_is_beach': 'first',
            'location_is_city_center': 'first',
            'accommodation_type': 'first',
            'accommodation_country': 'first'
        }).reset_index()
        accommodations.to_csv(accommodations_path, index=False)
    return id_to_reviews, accommodations

def triplet_table(input_csv=os.path.join(base_dir, 'data', 'train.csv'), gc_csv=os.path.join(base_dir, 'data', 'guest_country_accommodation.csv'), gt_csv=os.path.join(base_dir, 'data', 'guest_type_accommodation.csv')):
    if os.path.exists(gc_csv) and os.path.exists(gt_csv):
        gc = pd.read_csv(gc_csv)
        gt = pd.read_csv(gt_csv)
        return gc, gt
    df = pd.read_csv(input_csv)
    df = df.dropna(subset=['guest_country', 'guest_type', 'accommodation_id', 'review_score'])

    gc_df = df.groupby([ 'guest_country', 'accommodation_id']) \
        .agg(avg_score=('review_score', 'mean'),
             count=('review_score', 'count')) \
        .reset_index()
    gc_df = gc_df[gc_df['count'] > 5]
    gc_df.to_csv(gc_csv, index=False)
    gt_df = df.groupby([ 'guest_type', 'accommodation_id']) \
        .agg(avg_score=('review_score', 'mean'),
             count=('review_score', 'count')) \
        .reset_index()
    gt_df = gt_df[gt_df['count'] > 5]
    gt_df.to_csv(gt_csv, index=False)
    return gc_df, gt_df

def embedder_filtering(embedding, id_to_reviews, accommodations, nationality, accommodation_type, star, ski, beach, center, score):
    qualified_accommodations = accommodations
    # Filtering according to the need of user:
    if nationality is not None:
        qualified_accommodations = qualified_accommodations[qualified_accommodations['accommodation_country'] == nationality]
    if accommodation_type:
        qualified_accommodations = qualified_accommodations[qualified_accommodations['accommodation_type'].isin(accommodation_type)
        ]
    if star != -1:
        qualified_accommodations = qualified_accommodations[qualified_accommodations['accommodation_star_rating'] >= star]
    if ski != -1:
        qualified_accommodations = qualified_accommodations[qualified_accommodations['location_is_ski'] == ski]
    if beach != -1:
        qualified_accommodations = qualified_accommodations[qualified_accommodations['location_is_beach'] == beach]
    if center != -1:
        qualified_accommodations = qualified_accommodations[qualified_accommodations['location_is_city_center'] == center]
    if score != -1:
        qualified_accommodations = qualified_accommodations[qualified_accommodations['accommodation_score'] >= score]
    qualified_ids = set(qualified_accommodations['accommodation_id'])
    review_indexes = []
    for aid in qualified_ids:
        # Build the relation of indexes before and after filtering:
        review_indexes.extend(id_to_reviews.get(aid, []))
    embedding = embedding[review_indexes]
    return embedding, review_indexes

def calculate_absa_query(request, aspect_vectors):
    result = absa_extractor.predict(request)
    new_aspects_to_encode = []
    current_batch_new_aspect_map = {}
    for aspect in result["aspect"]:
        if aspect not in aspect2idx and aspect not in current_batch_new_aspect_map:
            new_aspects_to_encode.append(aspect)
            current_batch_new_aspect_map[aspect] = None
    '''
    if new_aspects_to_encode:
        new_aspect_vecs = absa_model.encode(new_aspects_to_encode, batch_size=32, normalize_embeddings=True)
        aspect_index = faiss.IndexFlatIP(aspect_vectors.shape[1])
        aspect_index.add(aspect_vectors)
        D, I = aspect_index.search(new_aspect_vecs, 1)
        for k, new_aspect in enumerate(new_aspects_to_encode):
            sim = D[k][0]
            idx_match = I[k][0]
            aspect2idx[new_aspect] = idx_match if sim >= 0.5 else -1
    '''
    aspect_vector = [0] * len(aspects_const)
    count_vector = [0] * len(aspects_const)
    for k, aspect in enumerate(result["aspect"]):
        idx = aspect2idx.get(aspect, -1)
        if (idx != -1):
            aspect_vector[aspect2idx[aspect]] = result["confidence"][k] * (1 if result["sentiment"][k] == "Positive" else (-1 if result["sentiment"][k] == "Negative" else 0))
            count_vector[aspect2idx[aspect]]  += 1
    absa_vector = [x / y if y != 0 else 0 for x, y in zip(aspect_vector, count_vector)]
    return absa_vector


def weight_calculation(indices, distances, reviews, review_indexes, guest_type, guest_country, months, nights, absa, absa_vector):
    heap = []
    guest_country_relation = 0 if guest_country is None else 1
    guest_type_relation = 0 if guest_type is None else 1
    gc, gt = triplet_table()
    for i, idx in enumerate(indices):
        accommodation = reviews[review_indexes[idx]]["accommodation_id"]
        if guest_country is not None:
            if gc[(gc['guest_country'] == guest_country) & (gc["accommodation_id"] == accommodation)].empty:
                guest_country_relation = 0
        if guest_type is not None:
            if gt[(gt['guest_type'] == guest_type) & (gt["accommodation_id"] == accommodation)].empty:
                guest_type_relation = 0
        if guest_country_relation == guest_type_relation == 0:
            break
    for i, idx in enumerate(indices):
        helpful_votes = reviews[review_indexes[idx]]['helpful']
        log_scaled_helpful = 0.25 * math.log10(1 + helpful_votes) / math.log10(1 + 91)
        country_factor = 0 if guest_country_relation == 0 else ((gc[(gc['guest_country'] == guest_country) & (gc["accommodation_id"] == reviews[review_indexes[idx]]["accommodation_id"])].iloc[0]['avg_score']) / 40)
        type_factor = 0 if guest_type_relation == 0 else ((gt[(gt['guest_type'] == guest_type) & (gt["accommodation_id"] == reviews[review_indexes[idx]]["accommodation_id"])].iloc[0]['avg_score']) / 40)
        month_factor = 0 if months == -1 else (6 - min(abs(reviews[review_indexes[idx]]["month"] - months), 12 - abs(reviews[review_indexes[idx]]["month"] - months))) / 24
        night_factor = 0 if nights == -1 or (categorize_nights(reviews[review_indexes[idx]]["room_nights"]) != categorize_nights(nights)) else 0.25
        if absa != None:
            absa_arr = np.array(absa[review_indexes[idx]])
            vec_arr = np.array(absa_vector)
            mask = (vec_arr != 0)
            if np.any(mask):
                focused_absa = absa_arr[mask]
                focused_vec = vec_arr[mask]
                norm_absa = np.linalg.norm(focused_absa)
                norm_vec = np.linalg.norm(focused_vec)
                if norm_vec > 0 and norm_absa > 0:
                    base_match_score = np.dot(focused_absa, focused_vec) / (
                                norm_vec * norm_absa)
                    distance = (base_match_score + 1) / 2
                else:
                    distance = distances[0][i]
            else:
                distance = distances[0][i]
        else:
            distance = distances[0][i]
        weight = ((distances[0][i] * distance) * 5) + log_scaled_helpful + country_factor + type_factor + month_factor + night_factor
        heapq.heappush(heap, (-weight, idx))
    return heap


def get_top_k(reviews, heap, review_indexes, k):
    dict_rankcount = {}
    heap_avgfirst = []
    aids = []
    rids = []
    for rank, (weight, idx) in enumerate(heap):
        result = reviews[review_indexes[idx]]
        aid = result['accommodation_id']
        ranksum, first, second, third = dict_rankcount.get(aid, (0, -1, -1, -1))
        dict_rankcount[aid] = (ranksum + len(heap) - rank, idx if first == -1 else first, idx if (first != -1 and second == -1) else second, idx if (first != -1 and second != -1 and third == -1) else third)
    for id, (ranksum, first, second, third) in dict_rankcount.items():
        heapq.heappush(heap_avgfirst, (ranksum, first, second, third))
        aids.append(id)
    top_k = heapq.nlargest(min(k, len(heap_avgfirst)), heap_avgfirst)
    results = "\n"
    for (ranksum, first, second, third) in top_k:
        if first != -1:
            result = reviews[review_indexes[first]]
            results = results + f"Accommodation ID: {result['accommodation_id']} Review: {result['full_text']}\n"
            rids.append(first)
        if second != -1:
            result = reviews[review_indexes[second]]
            results = results + f"Accommodation ID: {result['accommodation_id']} Review: {result['full_text']}\n"
            rids.append(second)
        if third != -1:
            result = reviews[review_indexes[third]]
            results = results + f"Accommodation ID: {result['accommodation_id']} Review: {result['full_text']}\n"
            rids.append(third)
    return results, aids, rids

def to_json(reviews, review_indexes, rids, aids, response):
    main_response = response['message']['content'].split("</think>")[-1]
    target_id = []
    target_reviews = []
    other_reviews = []
    for id in aids:
        if str(id) in main_response:
            target_id.append(id)
    if not target_id:
        print("Answer from LLM is not an available id?!")
    for rid in rids:
        result = reviews[review_indexes[rid]]
        title = str(result['title']) if str(result['title']).strip().lower() != "nan" else "Untitled"
        pro = str(result['positive']) if str(result['positive']).strip().lower() != "nan" else "Nothing"
        contra = str(result['negative']) if str(result['negative']).strip().lower() != "nan" else "Nothing"
        if result['accommodation_id'] in target_id:
            target_reviews.append({
                "accommodation_id": result['accommodation_id'],
                "title": title,
                "pro": pro,
                "contra": contra,
            })
        else:
            other_reviews.append({
                "accommodation_id": result['accommodation_id'],
                "title": title,
                "pro": pro,
                "contra": contra,
            })
    result = {
        "response": main_response,
        "target_reviews": target_reviews,
        "other_reviews": other_reviews,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def generate(nationality, types, star, ski, beach, center, score, guest_type, guest_country, months, nights, requirement):
    # Multithreading, in order to accelerate the embedding process:
    # torch.set_num_threads(8)
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    payload = requirement
    # Load the dataset:
    reviews = load_reviews()
    aspect_vectors = load_aspect_vectors()
    # Load or create the embedding of dataset:
    embedding_primary = load_embedding(embedder, reviews)
    # Load or create the relationship between reviews and accommodations:
    id_to_reviews, accommodations = get_relation()
    # Load absa data
    absa = load_absa()
    # Filtering the embedding:
    embedding, review_indexes = embedder_filtering(embedding_primary, id_to_reviews, accommodations, nationality, types, star, ski, beach, center, score)
    dimension = embedding.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embedding)
    # Turn the input of user into vector for the following search phase:
    query_embedding = embedder.encode(payload)
    # Find the 5 most similar or all reviews comparing with the input of user and use as the given data for LLM:
    if len(review_indexes) == 0:
        print("No accommodation that fits your need found... So we can't give you any recommendation.")
        return
    distances, indices = index.search(np.array([query_embedding]), len(review_indexes))
    absa_vector = calculate_absa_query(payload, aspect_vectors)
    heap = weight_calculation(indices[0], distances, reviews, review_indexes, guest_type, guest_country, months, nights, absa, absa_vector)
    results, aids, rids= get_top_k(reviews, heap, review_indexes, min(5, len(review_indexes)))
    # Create the prompt for LLM:
    prompt = (
            payload +
            "\n\nThe data for this recommendation is as follows. "
            "Please ONLY make recommendation based on the following reviews.\n"
            f"<reviews>{results}\n</reviews>\n"
            "Before answering, check once more:\n"
            "Have you recommended and ONLY recommended ONE recommendation?\n"
            "Is your recommendation based **only** on the above reviews?\n"
            "Did you provide ONLY the accommodation_id and your reason?\n"
            "If not, regenerate your answer.\n"
            "The review is always given, which is shown in the format of <reviews>contents</reviews>.\n"
            "You are strictly forbidden from using any other knowledge.\n"
    )
    # Print the payload, in order to check if the data and requirements are added successfully:
    print(prompt)
    # Generate the answer. Please make sure ollama is downloaded in your computer and is working now:
    # Also please make sure you have downloaded this model locally using "ollama pull" in terminal:
    response = ollama.chat(model='deepseek-r1:1.5b', messages=[
        {
            'role': 'user',
            'content': prompt
        },
    ])
    print(response['message']['content'])
    json_result = to_json(reviews, review_indexes, rids, aids, response)
    print(json_result)
    return json_result

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    nationality = data.get('accommodation_country', None)
    types = data.get('accommodation_type', [])
    star = float(data.get('accommodation_star', -1))
    ski = int(data.get('ski', -1))
    beach = int(data.get('beach', -1))
    center = int(data.get('center', -1))
    score = float(data.get('score', -1))
    guest_type = data.get('guest_type', None)
    guest_country = data.get('guest_country', None)
    months = int(data.get('months', -1))
    nights = int(data.get('nights', -1))
    requirement = data.get('requirement', "Please recommend me such an accommodation.")
    return generate(nationality, types, star, ski, beach, center, score, guest_type, guest_country, months, nights, requirement)


if __name__ == '__main__':
    # generate(None, ["Resort"], -1, -1, -1, -1, -1, None, None, -1,-1,
             # "I want to live in a Resort, which is with an elevator, with interesting activities, and with nice service.")
    app.run(host="0.0.0.0", port=5001)
