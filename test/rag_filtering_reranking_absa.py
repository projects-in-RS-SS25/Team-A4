from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from backend.main import load_absa, load_embedding, load_reviews, load_aspect_vectors, get_relation, embedder_filtering, get_top_k, calculate_absa_query, weight_calculation
def generate_rfra(nationality, types, star, ski, beach, center, score, guest_type, guest_country, months, nights, requirement):
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
    index = faiss.IndexFlatL2(dimension)
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
    return results