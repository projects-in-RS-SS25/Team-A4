import json


def to_json(reviews, review_indexes, rids, aids, response):
    main_response = response['message']['content'].split("</think>")[-1]
    target_id = []
    target_reviews = []
    other_reviews = []
    for id in aids:
        if str(id) in main_response:
            target_id.append(id)
    if not target_id:
        print("Answer from LLM is not an available id?!")
    for rid in rids:
        result = reviews[review_indexes[rid]]
        title = str(result['title']) if str(result['title']).strip().lower() != "nan" else "Untitled"
        pro = str(result['positive']) if str(result['positive']).strip().lower() != "nan" else "Nothing"
        contra = str(result['negative']) if str(result['negative']).strip().lower() != "nan" else "Nothing"
        if result['accommodation_id'] in target_id:
            target_reviews.append({
                "accommodation_id": result['accommodation_id'],
                "title": title,
                "pro": pro,
                "contra": contra,
            })
        else:
            other_reviews.append({
                "accommodation_id": result['accommodation_id'],
                "title": title,
                "pro": pro,
                "contra": contra,
            })
    result = {
        "response": main_response,
        "target_reviews": target_reviews,
        "other_reviews": other_reviews,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)