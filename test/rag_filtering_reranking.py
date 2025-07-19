from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex
import numpy as np
from backend.utils.load_reviews import load_reviews
from backend.utils.load_embedding import load_embedding
from backend.utils.get_relation import get_relation
from backend.utils.embedder_filtering import embedder_filtering
from backend.utils.triplet_table import triplet_table
from backend.utils.categorize_nights import categorize_nights
import math
import heapq

def get_top_k(reviews, heap, review_indexes, k):
    dict_rankcount = {}
    heap_avgfirst = []
    aids = []
    rids = []
    for rank, (weight, idx) in enumerate(heap):
        result = reviews[review_indexes[idx]]
        aid = result['accommodation_id']
        ranksum, first, second, third = dict_rankcount.get(aid, (0, -1, -1, -1))
        dict_rankcount[aid] = (
            ranksum + len(heap) - rank, idx if first == -1 else first,
            idx if (first != -1 and second == -1) else second,
            idx if (first != -1 and second != -1 and third == -1) else third)
    for id, (ranksum, first, second, third) in dict_rankcount.items():
        heapq.heappush(heap_avgfirst, (ranksum, first, second, third))
        aids.append(id)
    top_k = heapq.nlargest(min(k, len(heap_avgfirst)), heap_avgfirst)
    results = []
    for (ranksum, first, second, third) in top_k:
        if first != -1:
            result = reviews[review_indexes[first]]
            results.append(f"Accommodation ID: {result['accommodation_id']} Review: {result['full_text']}\n")
            rids.append(first)
        if second != -1:
            result = reviews[review_indexes[second]]
            results.append(f"Accommodation ID: {result['accommodation_id']} Review: {result['full_text']}\n")
            rids.append(second)
        if third != -1:
            result = reviews[review_indexes[third]]
            results.append(f"Accommodation ID: {result['accommodation_id']} Review: {result['full_text']}\n")
            rids.append(third)
    return results, aids, rids
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
        similarity = 1 - (distances[0][i] / 2)
        helpful_votes = reviews[review_indexes[idx]]['helpful']
        log_scaled_helpful = 0.25 * math.log10(1 + helpful_votes) / math.log10(1 + 91)
        country_factor = 0 if guest_country_relation == 0 else ((gc[(gc['guest_country'] == guest_country) & (gc["accommodation_id"] == reviews[review_indexes[idx]]["accommodation_id"])].iloc[0]['avg_score']) / 40)
        type_factor = 0 if guest_type_relation == 0 else ((gt[(gt['guest_type'] == guest_type) & (gt["accommodation_id"] == reviews[review_indexes[idx]]["accommodation_id"])].iloc[0]['avg_score']) / 40)
        month_factor = 0 if months == -1 else (6 - min(abs(reviews[review_indexes[idx]]["month"] - months), 12 - abs(reviews[review_indexes[idx]]["month"] - months))) / 24
        night_factor = 0 if nights == -1 or (categorize_nights(reviews[review_indexes[idx]]["room_nights"]) != categorize_nights(nights)) else 0.25
        weight = ((similarity ** 2) * 5) + log_scaled_helpful + country_factor + type_factor + month_factor + night_factor
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
    annoy_index = AnnoyIndex(dimension, 'angular')
    for i, vec in enumerate(embedding):
        annoy_index.add_item(i, vec)
    annoy_index.build(100)
    query_embedding = embedder.encode(payload)
    query_embedding = np.ascontiguousarray(query_embedding)
    annoy_internal_indices, annoy_distances = annoy_index.get_nns_by_vector(
        query_embedding, len(embedding), include_distances=True
    )
    distances = np.array([annoy_distances])
    indices = np.array([annoy_internal_indices])
    heap = weight_calculation(indices[0], distances, reviews, review_indexes, guest_type, guest_country, months, nights)
    results, aids, rids= get_top_k(reviews, heap, review_indexes, min(5, len(review_indexes)))
    return results, aids