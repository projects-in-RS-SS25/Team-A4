import os
from sentence_transformers import SentenceTransformer
from pyabsa import ATEPCCheckpointManager

base_dir = os.path.dirname(os.path.abspath(__file__))
absa_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
absa_extractor = ATEPCCheckpointManager.get_aspect_extractor(checkpoint='multilingual')
aspects_const = [
    'Room Comfort', 'Bed', 'Decoration', 'View', 'Clean', 'Noise',
    'Elevator', 'Food', 'Internet', 'Value of Money', 'Location',
    'Flexibility', 'Security', 'Parking', 'Pool', 'Staff', 'Activity',
    'Service', 'Air Conditioner', 'Bath'
]
aspect2idx = {aspect: idx for idx, aspect in enumerate(aspects_const)}
aspect2idx.update({
    "transport": 10, "transportation": 10, "metro": 10, "subway":10, "tram":10, "taxi": 10, "access": 10, "bus": 10,
    "receptionist": 15, "front desk": 15, "host": 15, "manager": 15, "assist": 17, "support": 17, "communication": 15, "offer": 17, "owner": 15,
    "floor": 4, "wall": 4, "dirt": 4, "dust": 4, "hair": 4,
    "room": 0, "rooms" : 0, "suite": 0, "space": 0, "windows": 0,
    "breakfast": 7, "breakfasts": 7, "dinner": 7, "restaurant": 7, "meal": 7, "meals": 7, "menu": 7, "buffet": 7, "drink": 7, "drinks": 7, "cafe": 7, "cafes": 7, "kitchen": 7, "bar":7, "supper": 7, "brunch": 7,
    "price": 9, "money": 9, "expensive": 9,
    "check in": 11, "check out": 11, "check-in": 11, "check-out": 11, "reservation": 11,
    "safety": 12, "lock": 12,
    "ac": 18, "fan": 18, "fans": 18, "heat": 18, "heats": 18, "aircon": 18, "airconditioner": 18,
    "bathroom": 19, "bathrooms": 19, "shower": 19, "bathtub": 19, "toilet": 19, "sink": 19, "hairdryer": 19, "mirror": 19, "water": 14, "robes": 19,
    "balcony": 3, "mountain": 3, "ocean": 3, "sea": 3, "garden": 3, "landscape": 3, "panorama": 3,
    "spacious": 0, "large": 0, "well-equipped": 0, "modern": 2, "modernly furnished": 2,
    "authentic": 2, "central": 10, "convenient": 10, "walking distance": 10, "close to": 10,
    "scraping": 5, "loud": 5, "noisy": 5, "quiet": 5,
    "friendly": 15, "kind": 15, "helpful": 15,
    "dirty": 4, "not clean": 4,
    "suitable for family": 16, "family": 16,
    "well laid out": 2, "lake": 3,
})