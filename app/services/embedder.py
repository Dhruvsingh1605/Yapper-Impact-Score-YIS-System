from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: list[str]) -> np.ndarray:
    return model.encode(texts, convert_to_numpy=True)

def compute_relevance(tweet_vecs: np.ndarray, campaign_vec: np.ndarray) -> list[float]:
    sims = cosine_similarity(tweet_vecs, campaign_vec.reshape(1, -1)).flatten()
    return sims.tolist()
