import pandas as pd
import random
from test.plain_rag import generate_r
from test.rag_filtering import generate_rf
from test.rag_filtering_reranking import generate_rfr
from test.rag_filtering_reranking_absa import generate_rfra
from tqdm import tqdm
random.seed(42)
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
rows = []
num_queries = 50 #Could change the numbers of querys here
for _ in tqdm(range(num_queries), desc="Generating test data... "):
    at = random.choice(acc_types)
    a1, a2, a3 = random.sample(aspects, 3)
    query = f"I want to live in a {at}, which is {a1}, {a2}, and {a3}." if random.random() >= 0.5 else f"Please recommend me a {at}, which is {a1}, {a2}, and {a3}."
    rows.append({'acc_type': at, 'query': query,
                 'aspect_1': a1, "aspect_2": a2, 'aspect_3': a3,
                 'plain_rag': generate_r(None, [at], -1, -1, -1, -1, -1, None, None, -1,-1,
                                                                     query),
                 'filtering': generate_rf(None, [at], -1, -1, -1, -1, -1, None, None, -1,-1,
                                        query),
                 'reranking': generate_rfr(None, [at], -1, -1, -1, -1, -1, None, None, -1,-1,
                                         query),
                 'absa': generate_rfra(None, [at], -1, -1, -1, -1, -1, None, None, -1,-1,
                                      query)})
df = pd.DataFrame(rows)
df.to_csv('queries_for_ablation.csv', index=False, sep='㏦')
