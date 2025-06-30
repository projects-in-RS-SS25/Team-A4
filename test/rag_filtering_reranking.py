from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from backend.main import triplet_table, load_embedding, load_reviews, get_relation, embedder_filtering, get_top_k, categorize_nights
import math
import heapq
def weight_calculation(indices, distances, reviews, review_indexes, guest_type, guest_country, months, nights):
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
        weight = ((distances[0][i] * distances[0][i]) * 5) + log_scaled_helpful + country_factor + type_factor + month_factor + night_factor
        heapq.heappush(heap, (-weight, idx))
    return heap

def generate_rfr(nationality, types, star, ski, beach, center, score, guest_type, guest_country, months, nights, requirement):
    # Multithreading, in order to accelerate the embedding process:
    # torch.set_num_threads(8)
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    payload = requirement
    # Load the dataset:
    reviews = load_reviews()
    # Load or create the embedding of dataset:
    embedding_primary = load_embedding(embedder, reviews)
    # Load or create the relationship between reviews and accommodations:
    id_to_reviews, accommodations = get_relation()
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
    heap = weight_calculation(indices[0], distances, reviews, review_indexes, guest_type, guest_country, months, nights)
    results, aids, rids= get_top_k(reviews, heap, review_indexes, min(5, len(review_indexes)))
    return results