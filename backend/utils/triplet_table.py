import os
import pandas as pd
from backend.app_config import base_dir

def triplet_table(input_csv=os.path.join(base_dir, 'data', 'train.csv'), gc_csv=os.path.join(base_dir, 'data', 'guest_country_accommodation.csv'), gt_csv=os.path.join(base_dir, 'data', 'guest_type_accommodation.csv')):
    if os.path.exists(gc_csv) and os.path.exists(gt_csv):
        gc = pd.read_csv(gc_csv)
        gt = pd.read_csv(gt_csv)
        return gc, gt
    df = pd.read_csv(input_csv)
    df = df.dropna(subset=['guest_country', 'guest_type', 'accommodation_id', 'review_score'])

    gc_df = df.groupby([ 'guest_country', 'accommodation_id']) \
        .agg(avg_score=('review_score', 'mean'),
             count=('review_score', 'count')) \
        .reset_index()
    gc_df = gc_df[gc_df['count'] > 5]
    gc_df.to_csv(gc_csv, index=False)
    gt_df = df.groupby([ 'guest_type', 'accommodation_id']) \
        .agg(avg_score=('review_score', 'mean'),
             count=('review_score', 'count')) \
        .reset_index()
    gt_df = gt_df[gt_df['count'] > 5]
    gt_df.to_csv(gt_csv, index=False)
    return gc_df, gt_df
