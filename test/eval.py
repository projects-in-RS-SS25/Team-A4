from test.rag_filtering import generate_rf
from test.rag_filtering_reranking import generate_rfr
from test.rag_filtering_reranking_absa import generate_rfra
from tqdm import tqdm
from typing import List, Dict, Any
import numpy as np
import random
from tqdm.asyncio import tqdm
import ollama
import asyncio
async def ask_LLM(review: str, aspect: str) -> int:
    """
    Asks an LLM to determine if a review contains a specific aspect.
    Returns 1 if related, 0 if not.
    """
    prompt = (f"You are a professional emotional dimension analyst. Your task is to analyse whether this review contains the aspect I mentioned. If it is mentioned, please return 1. Otherwise, please return 0.\n"
              f"The review is: {review}\n"
              f"The aspect we care about is: {aspect}\n"
              f"Your response MUST be ONLY '1' or '0'. Do NOT include any other text, explanations, or punctuation.\n")
    try:
        response = await ollama.chat(model='llama3.1:8b', messages=[ # Use await for async call
            {
                'role': 'user',
                'content': prompt
            },
        ])
        content = response['message']['content'].strip()
        if "1" in content:
            return 1
        else:
            return 0
    except Exception as e:
        print(f"\nError calling LLM for review '{review[:50]}...' and aspect '{aspect}': {e}")
        return 0

async def get_method_hits(reviews_list: List[str], aspects_to_check: List[str]) -> int:
    tasks = []
    for review_text in reviews_list:
        for aspect in aspects_to_check:
            tasks.append(ask_LLM(review_text, aspect))
    if tasks:
        hits = await asyncio.gather(*tasks)
        return sum(hits)
    return 0

async def eval(seed: int):
    random.seed(seed)
    aspects = [
        "whose comfort is perfect", "with an enjoyable comfortable bed", "with lovely decoration", "have a nice view", "well cleaned",
        "without any noise", "with an elevator", "with tasty food", "with fast Wi-Fi", "whose value of cost is great", "with a great location",
        "flexible for staying", "in which I can expect a safe stay", "parking available", "with a nice pool", "with friendly staff", "with interesting activities",
        "with nice service", "with an useful air conditioner", "with a nice bathroom"
    ]
    acc_types = [
        "Hotel", "Bed and Breakfast", 'ApartHotel', 'Hostel',
        'Resort', 'Apartment', 'Motel', 'Guest house', 'Farm stay',
        'Lodge', 'Villa', 'Camping', 'Capsule Hotel', 'Inn', 'Holiday home',
        'Homestay', 'Chalet', 'Ryokan', 'Holiday Park', 'Country house',
        'Boat', 'Tented camp', 'Student accommodation', 'Riad',
        'Cruise', 'Love Hotel', 'Japanese-style Business Hotel'
    ]
    rf_scores = []
    rfr_scores = []
    rfra_scores = []
    num_queries = 50 #Could change the numbers of querys here
    for _ in tqdm(range(num_queries), desc="making evaluation"):
        at = random.choice(acc_types)
        a1, a2, a3 = random.sample(aspects, 3)
        query = f"I want to live in a {at}, which is {a1}, {a2}, and {a3}." if random.random() >= 0.5 else f"Please recommend me a {at}, which is {a1}, {a2}, and {a3}."
        rf_reviews, rf_ids = generate_rf(None, [at], -1, -1, -1, -1, -1, None, None, -1,-1,
                                     query)
        rfr_reviews, rfr_ids = generate_rfr(None, [at], -1, -1, -1, -1, -1, None, None, -1,-1,
                                     query)
        rfra_reviews, rfra_ids = generate_rfra(None, [at], -1, -1, -1, -1, -1, None, None, -1,-1,
                                     query)
        rf_hit = await get_method_hits(rf_reviews, [a1, a2, a3])
        rfr_hit = await get_method_hits(rfr_reviews, [a1, a2, a3])
        rfra_hit = await get_method_hits(rfra_reviews, [a1, a2, a3])
        rf_scores.append(rf_hit / rf_ids)
        rfr_scores.append(rfr_hit / rfr_ids)
        rfra_scores.append(rfra_hit / rfra_ids)
    mean_rf = np.mean(rf_scores)
    mean_rfr = np.mean(rfr_scores)
    mean_rfra = np.mean(rfra_scores)
    print(f"mean hit per accommodation for rag with filtering (baseline): {mean_rf}")
    print(f"mean hit per accommodation for rag with filtering + ranksum reranking: {mean_rfr}")
    print(f"mean hit per accommodation for rag with filtering + ranksum reranking + absa: {mean_rfra}")

if __name__ == '__main__':
    asyncio.run(eval(81925))