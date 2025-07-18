def embedder_filtering(embedding, id_to_reviews, accommodations, nationality, accommodation_type, star, ski, beach,
                       center, score):
    qualified_accommodations = accommodations
    if nationality is not None:
        qualified_accommodations = qualified_accommodations[
            qualified_accommodations['accommodation_country'] == nationality]
    if accommodation_type:
        qualified_accommodations = qualified_accommodations[
            qualified_accommodations['accommodation_type'].isin(accommodation_type)
        ]
    if star != -1:
        qualified_accommodations = qualified_accommodations[
            qualified_accommodations['accommodation_star_rating'] >= star]
    if ski != -1:
        qualified_accommodations = qualified_accommodations[qualified_accommodations['location_is_ski'] == ski]
    if beach != -1:
        qualified_accommodations = qualified_accommodations[qualified_accommodations['location_is_beach'] == beach]
    if center != -1:
        qualified_accommodations = qualified_accommodations[
            qualified_accommodations['location_is_city_center'] == center]
    if score != -1:
        qualified_accommodations = qualified_accommodations[qualified_accommodations['accommodation_score'] >= score]
    qualified_ids = set(qualified_accommodations['accommodation_id'])
    review_indexes = []
    for aid in qualified_ids:
        review_indexes.extend(id_to_reviews.get(aid, []))
    embedding = embedding[review_indexes]
    return embedding, review_indexes
