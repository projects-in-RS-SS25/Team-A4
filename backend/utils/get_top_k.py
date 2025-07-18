import heapq
from collections import defaultdict


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
    results = "\n"
    for (ranksum, first, second, third) in top_k:
        if first != -1:
            result = reviews[review_indexes[first]]
            results = results + f"Accommodation ID: {result['accommodation_id']} Review: {result['full_text']}\n"
            rids.append(first)
        if second != -1:
            result = reviews[review_indexes[second]]
            results = results + f"Accommodation ID: {result['accommodation_id']} Review: {result['full_text']}\n"
            rids.append(second)
        if third != -1:
            result = reviews[review_indexes[third]]
            results = results + f"Accommodation ID: {result['accommodation_id']} Review: {result['full_text']}\n"
            rids.append(third)
    return results, aids, rids
