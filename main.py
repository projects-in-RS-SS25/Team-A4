from sentence_transformers import SentenceTransformer
import ollama
import faiss
import numpy as np
import pandas as pd
import torch
import os
import pickle
from collections import defaultdict

def load_reviews(dataset_path='train.csv', cache_path="reviews.pkl"):
    reviews = []
    if os.path.exists(cache_path):
        # Load if there is the cache document for reviews exists
        with open(cache_path, "rb") as f:
            reviews = pickle.load(f)
    else:
        # Create and save the dictionary for reviews, to reduce the processing time.
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

def load_embedding(embedder, reviews, cache_path="embedding.npy"):
    # Load if there is the cache document for embedding exists
    if os.path.exists(cache_path):
        embedding = np.load(cache_path)
    else:
        # Create and save the vector list for embedded reviews, to reduce the processing time.
        embedding = embedder.encode([review["full_text"] for review in reviews], convert_to_numpy=True)
        np.save(cache_path, embedding)
    return embedding

def get_relation(dataset_path='train.csv', accommodations_path = 'accommodations.csv', cache_path="relations.pkl"):
    if os.path.exists(cache_path):
        # Load if there is the cache document for relations from accommodation ids to reviews exists
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
        # Load if there is the cache document for characteristics of accommodations exists
        accommodations = pd.read_csv(accommodations_path)
    else:
        df = pd.read_csv(dataset_path)
        accommodations = df.groupby('accommodation_id').agg({
            'accommodation_score': 'first',
            'accommodation_star_rating': 'first',
            'location_is_ski': 'first',
            'location_is_beach': 'first',
            'location_is_city_center': 'first',
            'accommodation_type': 'first'
        }).reset_index()
        accommodations.to_csv(accommodations_path, index=False)
    return id_to_reviews, accommodations

def main():
    # Multithreading, in order to accelerate the embedding process.
    # torch.set_num_threads(8)
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    payload = input("Please type your requirements of accommodation: \n")
    # Load the dataset
    reviews = load_reviews()
    # Load or create the embedding of dataset
    embedding = load_embedding(embedder, reviews)
    dimension = embedding.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embedding)
    # Turn the input of user into vector for the following search phase.
    query_embedding = embedder.encode(payload)
    # Find the 5 most similar reviews comparing with the input of user and use as the given data for LLM.
    distances, indices = index.search(np.array([query_embedding]), 5)
    results = "\n"
    for i, idx in enumerate(indices[0]):
        result = reviews[idx]
        results = results + f"Accommodation ID: {result['accommodation_id']} Review: {result['full_text']}\n"
    # Create the prompt for LLM
    prompt = (
        payload +
        "\n\nThe data for this recommendation is as follows. "
        "Please ONLY make recommendation based on the following reviews.\n"
        f"<reviews>{results}\n</reviews>\n"
        "Before answering, check once more:\n"
        "Is your recommendation based **only** on the above reviews?\n"
        "Did you provide ONLY the accommodation_id and your reason?\n"
        "If not, regenerate your answer.\n"
        "The review is always given, which is shown in the format of <reviews>contents</reviews>.\n"
        "You are strictly forbidden from using any other knowledge.\n"
    )
    # Print the payload, in order to check if the data and requirements are added successfully.
    print(prompt)
    # Generate the answer. Please make sure ollama is downloaded in your computer and is working now.
    # Also please make sure you have downloaded this model locally using "ollama pull" in terminal.
    response_a = ollama.chat(model='deepseek-r1:7b', messages=[
        {
            'role': 'user',
            'content': prompt
        },
    ])
    print(response_a['message']['content'])

if __name__ == "__main__":
    get_relation()
    main()