from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex
import numpy as np
from backend.utils.embedder_filtering import embedder_filtering
from backend.utils.get_relation import get_relation
from backend.utils.load_absa import load_absa
from backend.utils.load_embedding import load_embedding
from backend.utils.load_reviews import load_reviews
from backend.utils.weight_calculation import weight_calculation
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

def generate_rfra(nationality, types, star, ski, beach, center, score, guest_type, guest_country, months, nights, requirement):
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
    # Load absa data
    absa_results,clusters,aspect_labels,cluster_vectors = load_absa()
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
    heap = weight_calculation(indices[0], distances, reviews, review_indexes, guest_type, guest_country, months, nights,
                              absa_results,clusters,aspect_labels,cluster_vectors, payload)
    results, aids, rids = get_top_k(reviews, heap, review_indexes, min(5, len(review_indexes)))
    return results, aids