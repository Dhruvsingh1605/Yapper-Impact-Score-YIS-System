# app/routers/score.py

from fastapi import APIRouter, HTTPException
from typing import List, Dict
from pydantic import BaseModel

from app.services.embedder import embed_texts, compute_relevance
from app.services.scorer import (
    engagement_score,
    final_tweet_score,
    aggregate_user_scores,
)
from app.models.config import WEIGHTS

class Tweet(BaseModel):
    text: str
    retweet_count: int
    reply_count: int
    favorite_count: int

class ScoreResponse(BaseModel):
    yis: float
    details: Dict[str, float]

router = APIRouter()

@router.post("/", response_model=ScoreResponse)
async def compute_yis(tweets: List[Tweet]):
    # 1. Validate input
    if not tweets:
        raise HTTPException(status_code=400, detail="Tweet list is empty.")

    # 2. Embed tweets & campaign brief
    texts = [t.text for t in tweets]
    tweet_vecs = embed_texts(texts)

    # Read campaign brief (ensure path is correct)
    try:
        with open("data/raw/campaign_brief.txt", "r") as f:
            brief_text = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Campaign brief not found.")

    campaign_vec = embed_texts([brief_text])[0]

    # 3. Compute semantic relevance
    relevances = compute_relevance(tweet_vecs, campaign_vec)

    # 4. Compute engagement and final scores per tweet
    tweet_scores = []
    total_engagement = 0
    for tweet, rel in zip(tweets, relevances):
        eng = engagement_score(
            tweet.retweet_count,
            tweet.reply_count,
            tweet.favorite_count,
            WEIGHTS,
        )
        tweet_scores.append(final_tweet_score(eng, rel))
        total_engagement += eng

    # 5. Aggregate into total YIS
    total_yis = aggregate_user_scores(tweet_scores)

    # 6. Prepare detail metrics
    details = {
        "tweet_count": len(tweets),
        "total_engagement": total_engagement,
        "average_relevance": sum(relevances) / len(relevances),
    }

    return {"yis": total_yis, "details": details}
