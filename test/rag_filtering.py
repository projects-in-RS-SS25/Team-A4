from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex
import numpy as np
from backend.utils.load_reviews import load_reviews
from backend.utils.load_embedding import load_embedding
from backend.utils.get_relation import get_relation
from backend.utils.embedder_filtering import embedder_filtering

def generate_rf(nationality, types, star, ski, beach, center, score, guest_type, guest_country, months, nights, requirement):
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
    k = min(15, len(annoy_internal_indices))
    top_k_annoy_indices = annoy_internal_indices[:k]
    indices = np.array([top_k_annoy_indices])
    topk_reviews = [reviews[i] for i in indices[0]]
    results = []
    for result in topk_reviews:
        results.append(f"Accommodation ID: {result['accommodation_id']} Review: {result['full_text']}\n")
    return results