import pandas as pd
import random
aspects = [
    "whose comfort is perfect", "with an enjoyable comfortable bed", "with lovely decoration", "have a nice view", "well cleaned",
    "without any noise", "with an elevator", "with tasty food", "with fast Wi-Fi", "worth costing", "with a great location",
    "flexible for staying", "in which I can expect a safe stay", "parking available", "with a nice pool", "with friendly staff", "with interesting activities",
    "with nice service", "with an air conditioner", "with a nice bathroom"
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
for _ in range(num_queries):
    at = random.choice(acc_types)
    a1, a2, a3 = random.sample(aspects, 3)
    query = f"I want to live in a {at}, which is {a1}, {a2}, and {a3}." if random.random() >= 0.5 else f"Please recommend me a {at}, which is {a1}, {a2}, and {a3}."
    rows.append({'acc_type': at, 'query': query})
df = pd.DataFrame(rows)
df.to_csv('queries_for_ablation.csv', index=False)
