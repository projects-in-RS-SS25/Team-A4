import math
import heapq
import numpy as np
from .triplet_table import triplet_table
from .categorize_nights import categorize_nights
from app_config import *

def weight_calculation(indices, distances, reviews, review_indexes, guest_type, guest_country, months, nights, absa_results, clusters, aspect_labels, cluster_vectors, requirement):
    global aspects_cleaned, sentiments_cleaned
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

    if absa_results is not None:
        absa_requirement = absa_extractor.predict(requirement)
        aspects_requirement = absa_requirement['aspect']
        aspects_embedding = absa_model.encode(aspects_requirement, normalize_embeddings=True)
        sentiments_requirement = absa_requirement['sentiment']
        aspects_cleaned = []
        sentiments_cleaned = []
        for idx, aspect in enumerate(aspects_requirement):
            if aspect in aspect_labels.keys():
                if aspect_labels[aspect] != -1:
                    aspects_cleaned.append(aspect_labels[aspect])
                    sentiments_cleaned.append(sentiments_requirement[idx])
                else:
                    continue
            else:
                similarities = np.dot(aspects_embedding[idx], cluster_vectors)
                max_idx = np.argmax(similarities)
                cluster_id = list(clusters.keys())[max_idx]
                aspects_cleaned.append(cluster_id)
                sentiments_cleaned.append(sentiments_requirement[idx])
    for i, idx in enumerate(indices):
        similarity = 2 - (distances[0][i] ** 2 / 2)  # from angular to cosine
        helpful_votes = reviews[review_indexes[idx]]['helpful']
        log_scaled_helpful = 0.25 * math.log10(1 + helpful_votes) / math.log10(1 + 91)
        country_factor = 0 if guest_country_relation == 0 else ((gc[(gc['guest_country'] == guest_country) & (
                    gc["accommodation_id"] == reviews[review_indexes[idx]]["accommodation_id"])].iloc[0][
            'avg_score']) / 40)
        type_factor = 0 if guest_type_relation == 0 else ((gt[(gt['guest_type'] == guest_type) & (
                    gt["accommodation_id"] == reviews[review_indexes[idx]]["accommodation_id"])].iloc[0][
            'avg_score']) / 40)
        month_factor = 0 if months == -1 \
            else (6 - min(abs(reviews[review_indexes[idx]]["month"] - months),
                12 - abs(reviews[review_indexes[idx]]["month"] - months))) / 24
        night_factor = 0 if (nights == -1
                             or (
                    categorize_nights(reviews[review_indexes[idx]]["room_nights"]) != categorize_nights(
                nights))) else 0.25
        if absa_results is not None:
                absa_review = absa_results[idx]["extracted_aspect_sentiments"]
                weight_sum_absa = 0
                score_absa = 0
                for item in absa_review:
                    if item['cluster_label'] not in aspects_cleaned:
                        weight_sum_absa += 1
                        score_absa += 0.5
                        if item['sentiment'] == "Positive":
                            score_absa += 0.5
                        elif item['sentiment'] == "Negative":
                            score_absa -= 0.5
                    else:
                        weight_sum_absa += 3
                        if item['sentiment'] == sentiments_cleaned[aspects_cleaned.index(item['cluster_label'])]:
                            score_absa += 3
                distance = score_absa / weight_sum_absa
        else:
            distance = similarity
        weight = ((similarity * distance) * 5) + log_scaled_helpful + country_factor + type_factor + month_factor + night_factor
        heapq.heappush(heap, (-weight, idx))
    return heap
