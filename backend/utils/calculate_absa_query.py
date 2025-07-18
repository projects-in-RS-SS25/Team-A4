import faiss
from app_config import absa_extractor, absa_model, aspects_const, aspect2idx


def calculate_absa_query(request, aspect_vectors):
    result = absa_extractor.predict(request)
    new_aspects_to_encode = []
    current_batch_new_aspect_map = {}
    for aspect in result["aspect"]:
        if aspect not in aspect2idx and aspect not in current_batch_new_aspect_map:
            new_aspects_to_encode.append(aspect)
            current_batch_new_aspect_map[aspect] = None

    if new_aspects_to_encode:
        new_aspect_vecs = absa_model.encode(new_aspects_to_encode, batch_size=32, normalize_embeddings=True)
        aspect_index = faiss.IndexFlatIP(aspect_vectors.shape[1])
        aspect_index.add(aspect_vectors)
        D, I = aspect_index.search(new_aspect_vecs, 1)
        for k, new_aspect in enumerate(new_aspects_to_encode):
            sim = D[k][0]
            idx_match = I[k][0]
            aspect2idx[new_aspect] = idx_match if sim >= 0.5 else -1

    aspect_vector = [0] * len(aspects_const)
    count_vector = [0] * len(aspects_const)
    for k, aspect in enumerate(result["aspect"]):
        idx = aspect2idx.get(aspect, -1)
        if idx != -1:
            aspect_vector[aspect2idx[aspect]] = (result["confidence"][k] *
            (1 if result["sentiment"][k] == "Positive" else (-1 if result["sentiment"][k] == "Negative" else 0)))
            count_vector[aspect2idx[aspect]] += 1
    absa_vector = [x / y if y != 0 else 0 for x, y in zip(aspect_vector, count_vector)]
    return absa_vector
