import os
import json
from backend.app_config import base_dir
import numpy as np

def load_absa(result_path=os.path.join(base_dir, 'data', 'cleaned_absa_results.jsonl'), clusters_path=os.path.join(base_dir, 'data', 'clusters.json'), labels_path=os.path.join(base_dir, 'data', 'aspect_labels.json')):
    try:
        with open(clusters_path, 'r', encoding='utf-8') as f:
            clusters = json.load(f)
    except Exception as e:
        return None,None,None,None
    try:
        with open(labels_path, 'r', encoding='utf-8') as f:
            aspect_labels = json.load(f)
    except Exception as e:
        return None,None,None,None
    absa_results = []
    try:
        with open(result_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f):
                line = line.strip()
                if line:
                    try:
                        item = json.loads(line)
                        absa_results.append(item)
                    except json.JSONDecodeError as e:
                        return None,None,None,None
    except Exception as e:
        return None,None,None,None
    cluster_vectors = []
    for label in clusters.keys():
        center_vector = clusters[label]["center_embedding"]
        cluster_vectors.append(np.array(center_vector))
    print('absa load success')
    return absa_results,clusters,aspect_labels,cluster_vectors
