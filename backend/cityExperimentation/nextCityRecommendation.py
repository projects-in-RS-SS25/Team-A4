import os
import joblib
import pandas as pd
import numpy as np
import re
import ollama

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(base_dir, "data", "city_count_model.pkl")
encoder_path = os.path.join(base_dir, "data", "city_count_encoder.pkl")
rf_model = joblib.load(model_path)
encoder = joblib.load(encoder_path)


def predict_city_count(preferred_nights: int, checkin_month: int) -> int:
    # Constant For Mocking
    device = "mobile"
    cross_border = True

    input_df = pd.DataFrame([[checkin_month, device]], columns=["checkin_month", "device_class"])
    encoded_input = encoder.transform(input_df)
    input_vector = np.hstack([[preferred_nights, int(cross_border)], encoded_input[0]])
    prediction = rf_model.predict([input_vector])[0]
    return max(1, round(prediction))


def get_city_for_accommodation(accommodation_id: int) -> str:
    city_df = pd.read_csv(os.path.join(base_dir, "data", "accommodation_cities.csv"))
    match = city_df[city_df["accommodation_id"] == accommodation_id]
    if not match.empty:
        return match.iloc[0]["accommodation_city"]
    return "Unknown City"


def suggest_next_cities(accommodation_id: int, country: str, city: str, guest_type: str, center: int, beach: int, ski: int, month: int, nights: int, requirement: str, next_city_count: int) -> str:
    prompt = f"""
    You are a helpful travel assistant planning a multi-city holiday within 
    {country}.
    Respond like an API, not like a ChatBot.

    The user wants to:
    - Start In: {city}
    - Traveler Type: {guest_type}
    - Holiday Preferences: {('center' if center == 1 else '')} {('beach' if beach == 1 else '')} {('ski' if ski == 1 else '')}
    - Start Month: {month}
    - Total Nights: {nights}
    - Notes from User: "{requirement}"

    The trip starts in {city}. Please recommend exactly {next_city_count} more cities that are:
    - Major and known cities.
    - Logically connected for an itinerary (e.g., geographically close or forming a sensible route).
    - Suitable for this traveler's preferences.
    - Not the starting city ({city}).
    - Realistic to reach within the trip duration.
    - Each city should feel like a natural next step in the route.

    For each next city, give:
    1. City Name
    2. 1-2 Sentence Reason Why It Makes a Good Next Stop

    Keep responses realistic — No teleporting across the country. 
    Avoid overly touristy or far-flung cities unless it makes geographic or thematic sense.

    Format:
    1. City Name – Reason
    2. City Name – Reason 
    ...
    """

    response = ollama.chat(model='deepseek-r1:1.5b', messages=[
        {
            'role': 'user',
            'content': prompt
        },
    ])

    raw_output = response['message']['content'].strip()
    cleaned_output = re.sub(r"<think>.*?</think>", "", raw_output, flags=re.DOTALL).strip()
    return cleaned_output
