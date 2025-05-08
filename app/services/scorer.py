def engagement_score(retweets, replies, likes, weights: dict) -> float:
    return (retweets * weights["retweet"]
          + replies  * weights["reply"]
          + likes    * weights["like"])

def final_tweet_score(eng_score: float, relevance: float) -> float:
    return eng_score * relevance

def aggregate_user_scores(tweet_scores: list[float]) -> float:
    return sum(tweet_scores)
