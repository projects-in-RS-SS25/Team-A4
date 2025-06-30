from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from backend.main import load_embedding, load_reviews, get_relation, embedder_filtering

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
    index = faiss.IndexFlatIP(dimension)
    index.add(embedding)
    # Turn the input of user into vector for the following search phase:
    query_embedding = embedder.encode(payload)
    # Find the 5 most similar or all reviews comparing with the input of user and use as the given data for LLM:
    if len(review_indexes) == 0:
        print("No accommodation that fits your need found... So we can't give you any recommendation.")
        return
    distances, indices = index.search(np.array([query_embedding]), len(review_indexes))
    top_k = min(15, len(review_indexes))
    topk_indices = indices[0][:top_k]
    topk_reviews = [reviews[review_indexes[idx]] for idx in topk_indices]
    results = "\n"
    for result in topk_reviews:
        results = results + f"Accommodation ID: {result['accommodation_id']} Review: {result['full_text']}\n"
    return results