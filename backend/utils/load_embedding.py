import os
import numpy as np
from app_config import base_dir


def load_embedding(embedder, reviews, cache_path=os.path.join(base_dir, 'data', "embedding.npy")):
    if os.path.exists(cache_path):
        embedding = np.load(cache_path)
    else:
        embedding = embedder.encode([review["full_text"] for review in reviews], convert_to_numpy=True,
                                    normalize_embeddings=True)
        np.save(cache_path, embedding)
    return embedding
