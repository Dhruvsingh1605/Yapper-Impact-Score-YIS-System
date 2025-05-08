import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

def random_engagement():
    return {
        "retweet_count": random.randint(0, 50),
        "reply_count": random.randint(0, 20),
        "favorite_count": random.randint(0, 200),
    }

def random_timestamp(days_back=7):
    now = datetime.utcnow()
    delta = timedelta(days=random.randint(0, days_back),
                      seconds=random.randint(0, 86400))
    return (now - delta).isoformat() + "Z"

def create_mock_tweet(tweet_id):
    tweet = {
        "id": tweet_id,
        "text": fake.sentence(nb_words=10),
        "created_at": random_timestamp(),
        "user": {"screen_name": fake.user_name()},
    }
    tweet.update(random_engagement())
    # 50% chance to include the campaign hashtag
    if random.random() < 0.5:
        tweet["text"] += " #yapdrop"
    return tweet

def main(num_tweets=100, output_path="data/raw/mock_tweets.json"):
    tweets = [create_mock_tweet(i) for i in range(1, num_tweets + 1)]
    with open(output_path, "w") as f:
        json.dump(tweets, f, indent=2)
    print(f"Generated {len(tweets)} mock tweets → {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-tweets", type=int, default=100)
    parser.add_argument("--output", type=str, default="data/raw/mock_tweets.json")
    args = parser.parse_args()
    main(args.num_tweets, args.output)
