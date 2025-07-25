import os
from pydantic import BaseModel
from cityExperimentation.nextCityRecommendation import (
    get_city_for_accommodation,
    predict_city_count,
    suggest_next_cities
)
import numpy as np
import ollama


MOCK_MODE = os.environ.get("MOCK_MODE", "False").lower() == "true"
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RecommendationRequest(BaseModel):
    accommodation_country: str | None = None
    accommodation_type: list[str]
    accommodation_star: float
    ski: int
    beach: int
    center: int
    score: float
    guest_type: str | None = None
    guest_country: str | None = None
    months: int
    nights: int
    requirement: str



def generate(recommendation_request: RecommendationRequest):

    if MOCK_MODE:
        accommodation_id = -1955434893
        city = get_city_for_accommodation(accommodation_id)
        predicted_city_count = predict_city_count(
            recommendation_request.nights,
            recommendation_request.months
        )
        next_city_count = predicted_city_count - 1

        next_city_suggestion = suggest_next_cities(
            accommodation_id=accommodation_id,
            country=recommendation_request.accommodation_country,
            city=city,
            guest_type=recommendation_request.guest_type,
            center=recommendation_request.center,
            beach=recommendation_request.beach,
            ski=recommendation_request.ski,
            month=recommendation_request.months,
            nights=recommendation_request.nights,
            requirement=recommendation_request.requirement,
            next_city_count=next_city_count
        )

        return {
            "response": f"Accommodation ID: {accommodation_id} in {city}."
                        f" Recommendation: This place fits your preferences very well.",

            "target_reviews": [
                {
                    "title": "Great location!",
                    "accommodation_id": accommodation_id,
                    "pro": "Very close to the city center and clean rooms.",
                    "contra": "Breakfast was average."
                }
            ],

            "other_reviews": [
                {
                    "title": "Nice Budget Option",
                    "accommodation_id": accommodation_id,
                    "pro": "Affordable and friendly staff.",
                    "contra": "A bit noisy at night."
                },

            ],
            "starting_city": city,
            "city_count": predicted_city_count,
            "next_cities_suggestion": next_city_suggestion,
        }


    from annoy import AnnoyIndex
    from sentence_transformers import SentenceTransformer
    from .load_reviews import load_reviews
    from .load_embedding import load_embedding
    from .get_relation import get_relation
    from .load_absa import load_absa
    from .embedder_filtering import embedder_filtering
    from .weight_calculation import weight_calculation
    from .get_top_k import get_top_k
    from .to_json import to_json

    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    payload = recommendation_request.requirement

    reviews = load_reviews()
    embedding_primary = load_embedding(embedder, reviews)
    id_to_reviews, accommodations = get_relation()
    absa_results, clusters, aspect_labels, cluster_vectors = load_absa()

    nationality = recommendation_request.accommodation_country
    types = recommendation_request.accommodation_type
    star = recommendation_request.accommodation_star
    ski = recommendation_request.ski
    beach = recommendation_request.beach
    center = recommendation_request.center
    score = recommendation_request.score
    guest_type = recommendation_request.guest_type
    guest_country = recommendation_request.guest_country
    months = recommendation_request.months
    nights = recommendation_request.nights

    embedding, review_indexes = embedder_filtering(embedding_primary, id_to_reviews, accommodations, nationality, types,
                                                   star, ski, beach, center, score)
    if len(review_indexes) == 0:
        print("No accommodation that fits your need found... So we can't give you any recommendation.")
        return

    dimension = embedding.shape[1]
    embedding = np.ascontiguousarray(embedding)
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
                              absa_results, clusters, aspect_labels, cluster_vectors, payload)
    results, aids, rids = get_top_k(reviews, heap, review_indexes, min(5, len(review_indexes)))

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

    print(prompt)

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



