import os
from sentence_transformers import SentenceTransformer
from pyabsa import ATEPCCheckpointManager

MOCK_MODE = os.environ.get("MOCK_MODE", "false").lower() == "true"

if MOCK_MODE:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    absa_extractor = None  # Skip Loading Model
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    absa_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    absa_extractor = ATEPCCheckpointManager.get_aspect_extractor(checkpoint='english')