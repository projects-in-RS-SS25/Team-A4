import os
import pickle
from app_config import base_dir, absa_model, aspects_const

def load_aspect_vectors(cache_path=os.path.join(base_dir, 'data', "absa_vectors.pkl")):
    if(os.path.exists(cache_path)):
        with open(cache_path, "rb") as f:
            aspect_vectors = pickle.load(f)
    else:
        aspect_vectors = absa_model.encode(aspects_const, batch_size=32, normalize_embeddings=True)
        with open(cache_path, 'wb') as f:
            pickle.dump(aspect_vectors, f)
    return aspect_vectors