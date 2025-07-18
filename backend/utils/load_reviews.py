import os
import pickle
import pandas as pd

def load_reviews(dataset_path=None, cache_path=None):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if dataset_path is None:
        dataset_path = os.path.join(base_dir, 'data', 'train.csv')
    if cache_path is None:
        cache_path = os.path.join(base_dir, 'data', "reviews.pkl")
    reviews = []
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            reviews = pickle.load(f)
    else:
        df = pd.read_csv(dataset_path)
        for _, row in df.iterrows():
            review = {
                "title": row["review_title"],
                "positive": row["review_positive"],
                "negative": row["review_negative"],
                "full_text": f"{row['review_title']}:{row['review_positive']};{row['review_negative']}",
                "score": row["review_score"],
                "helpful": row["review_helpful_votes"],
                "guest_type": row["guest_type"],
                "guest_country": row["guest_country"],
                "room_nights": row["room_nights"],
                "month": row["month"],
                "accommodation_id": row["accommodation_id"],
                "accommodation_type": row["accommodation_type"],
                "accommodation_score": row["accommodation_score"],
                "accommodation_country": row["accommodation_country"],
                "accommodation_star_rating": row["accommodation_star_rating"],
                "location_is_beach": row["location_is_beach"],
                "location_is_ski": row["location_is_ski"],
                "location_is_city_center": row["location_is_city_center"]
            }
            reviews.append(review)
        with open(cache_path, "wb") as f:
            pickle.dump(reviews, f)
    return reviews
