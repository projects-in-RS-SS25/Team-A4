from collections import defaultdict
import os
import pickle
import pandas as pd
from backend.app_config import base_dir

def get_relation(dataset_path=os.path.join(base_dir, 'data', 'train.csv'), accommodations_path=os.path.join(base_dir, 'data', 'accommodations.csv'), cache_path=os.path.join(base_dir, 'data', "relations.pkl")):
    if os.path.exists(cache_path):
        # Load if there is the cache document for relations from accommodation ids to reviews exists:
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
        # Load if there is the cache document for characteristics of accommodations exists:
        accommodations = pd.read_csv(accommodations_path)
    else:
        df = pd.read_csv(dataset_path)
        accommodations = df.groupby('accommodation_id').agg({
            'accommodation_score': 'first',
            'accommodation_star_rating': 'first',
            'location_is_ski': 'first',
            'location_is_beach': 'first',
            'location_is_city_center': 'first',
            'accommodation_type': 'first',
            'accommodation_country': 'first'
        }).reset_index()
        accommodations.to_csv(accommodations_path, index=False)
    return id_to_reviews, accommodations
