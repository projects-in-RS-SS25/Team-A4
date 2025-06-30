from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from backend.main import load_embedding, load_reviews

def generate_r(nationality, types, star, ski, beach, center, score, guest_type, guest_country, months, nights, requirement):
    # Multithreading, in order to accelerate the embedding process:
    # torch.set_num_threads(8)
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    payload = requirement
    # Load the dataset:
    reviews = load_reviews()
    # Load or create the embedding of dataset:
    embedding = load_embedding(embedder, reviews)
    # Load or create the relationship between reviews and accommodations:
    dimension = embedding.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embedding)
    # Turn the input of user into vector for the following search phase:
    query_embedding = embedder.encode(payload)
    # Find the 5 most similar or all reviews comparing with the input of user and use as the given data for LLM:
    D, I = index.search(np.array([query_embedding]), 15)
    topk_reviews = [reviews[i] for i in I[0]]
    results = "\n"
    for result in topk_reviews:
        results = results + f"Accommodation ID: {result['accommodation_id']} Review: {result['full_text']}\n"
    return results