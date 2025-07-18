import os
from sentence_transformers import SentenceTransformer
from pyabsa import ATEPCCheckpointManager

base_dir = os.path.dirname(os.path.abspath(__file__))
absa_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
absa_extractor = ATEPCCheckpointManager.get_aspect_extractor(checkpoint='english')