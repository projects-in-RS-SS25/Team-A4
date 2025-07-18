import os
import numpy as np
from sentence_transformers import SentenceTransformer
from backend.app_config import base_dir
from backend.utils.load_reviews import load_reviews

def load_embedding(embedder, reviews, cache_path=os.path.join(base_dir, 'data', "embedding.npy")):
    if os.path.exists(cache_path):
        embedding = np.load(cache_path)
    else:
        print('embedding start')
        embedding = embedder.encode([review["full_text"] for review in reviews], convert_to_numpy=True,
                                    normalize_embeddings=True, show_progress_bar=True)
        np.save(cache_path, embedding)
    return embedding

load_embedding(SentenceTransformer("all-MiniLM-L6-v2"), load_reviews())