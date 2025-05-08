# app/pipeline/embed_and_score.py

import json
import mlflow
import pandas as pd

from app.services.embedder import embed_texts, compute_relevance
from app.services.scorer import (
    engagement_score,
    final_tweet_score,
    aggregate_user_scores,
)
from app.models.config import WEIGHTS, EMBED_MODEL_NAME

DATA_RAW       = "data/raw/mock_tweets.json"
BRIEF_PATH     = "data/raw/campaign_brief.txt"
OUTPUT_REPORT  = "data/raw/processed/yis_report.csv"

def load_data(path: str = DATA_RAW):
    with open(path, "r") as f:
        return json.load(f)

def run_pipeline():
    # 1. Load data
    tweets  = load_data()
    texts   = [t["text"] for t in tweets]
    metrics = [
        (t["retweet_count"], t["reply_count"], t["favorite_count"])
        for t in tweets
    ]

    # 2. Log params
    mlflow.log_param("embedding_model", EMBED_MODEL_NAME)
    mlflow.log_param("num_tweets", len(tweets))

    # 3. Embeddings
    tweet_vecs   = embed_texts(texts)
    with open(BRIEF_PATH, "r") as f:
        brief_text = f.read()
    campaign_vec = embed_texts([brief_text])[0]

    # 4. Relevance
    relevances = compute_relevance(tweet_vecs, campaign_vec)

    # 5. Scoring
    tweet_scores = []
    for (rt, rp, lk), rel in zip(metrics, relevances):
        eng = engagement_score(rt, rp, lk, WEIGHTS)
        tweet_scores.append(final_tweet_score(eng, rel))

    # 6. Aggregate
    total_yis = aggregate_user_scores(tweet_scores)
    mlflow.log_metric("user_yis", total_yis)

    # 7. Save report
    df = pd.DataFrame([{
        "user": tweets[0]["user"]["screen_name"],  # adjust if multi-user
        "tweet_count": len(tweets),
        "total_engagement": sum(
            engagement_score(rt, rp, lk, WEIGHTS)
            for (rt, rp, lk) in metrics
        ),
        "avg_relevance": sum(relevances) / len(relevances),
        "final_YIS": total_yis,
    }])
    df.to_csv(OUTPUT_REPORT, index=False)

    # 8. Log artifacts
    mlflow.log_artifact(DATA_RAW)
    mlflow.log_artifact(BRIEF_PATH)
    mlflow.log_artifact(OUTPUT_REPORT)

def main():
    mlflow.set_experiment("YIS-Pipeline")
    with mlflow.start_run():
        run_pipeline()

if __name__ == "__main__":
    main()
