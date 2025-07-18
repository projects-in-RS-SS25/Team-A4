import os
import pickle
import pandas as pd
from app_config import base_dir, aspects_const

def load_absa(dataset_path=os.path.join(base_dir, 'data', 'ABSA_results.csv'), sep = "㏦", cache_path=os.path.join(base_dir, 'data', "absa.pkl")):
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            absa = pickle.load(f)
    else:
        if os.path.exists(dataset_path):
            df_absa = pd.read_csv(dataset_path, sep=sep)
            absa = df_absa[aspects_const].values.tolist()
            with open(cache_path, 'wb') as f:
                pickle.dump(absa, f)
        else: return None
    return absa