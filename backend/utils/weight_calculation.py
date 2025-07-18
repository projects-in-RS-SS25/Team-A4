import math
import heapq
import numpy as np
from .triplet_table import triplet_table
from .categorize_nights import categorize_nights


def weight_calculation(indices, distances, reviews, review_indexes, guest_type, guest_country, months, nights, absa,
                       absa_vector):
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
        country_factor = 0 if guest_country_relation == 0 else ((gc[(gc['guest_country'] == guest_country) & (
                    gc["accommodation_id"] == reviews[review_indexes[idx]]["accommodation_id"])].iloc[0][
            'avg_score']) / 40)
        type_factor = 0 if guest_type_relation == 0 else ((gt[(gt['guest_type'] == guest_type) & (
                    gt["accommodation_id"] == reviews[review_indexes[idx]]["accommodation_id"])].iloc[0][
            'avg_score']) / 40)
        month_factor = 0 if months == -1 else (6 - min(abs(reviews[review_indexes[idx]]["month"] - months),
                                                       12 - abs(reviews[review_indexes[idx]]["month"] - months))) / 24
        night_factor = 0 if nights == -1 or (
                    categorize_nights(reviews[review_indexes[idx]]["room_nights"]) != categorize_nights(
                nights)) else 0.25
        if absa is not None:
            absa_arr = np.array(absa[review_indexes[idx]])
            vec_arr = np.array(absa_vector)
            mask = (vec_arr != 0)
            if np.any(mask):
                focused_absa = absa_arr[mask]
                focused_vec = vec_arr[mask]
                norm_absa = np.linalg.norm(focused_absa)
                norm_vec = np.linalg.norm(focused_vec)
                if norm_vec > 0 and norm_absa > 0:
                    base_match_score = np.dot(focused_absa, focused_vec) / (
                            norm_vec * norm_absa)
                    distance = (base_match_score + 1) / 2
                else:
                    distance = distances[0][i]
            else:
                distance = distances[0][i]
        else:
            distance = distances[0][i]
        weight = ((distances[0][
                       i] * distance) * 5) + log_scaled_helpful + country_factor + type_factor + month_factor + night_factor
        heapq.heappush(heap, (-weight, idx))
    return heap
