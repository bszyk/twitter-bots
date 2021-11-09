import os
from pathlib import Path
import tweepy
import csv
from datetime import datetime

ROOT = Path(__file__).resolve().parents[0]


def get_tweet(tweets_file, excluded_tweets=None):
    """Get tweet to post from CSV file"""

    with open(tweets_file) as csvfile:
        reader = csv.DictReader(csvfile)
        possible_tweets = [row["tweet"] for row in reader]

    if excluded_tweets:
        recent_tweets = [status_object.text for status_object in excluded_tweets]
        possible_tweets = [tweet for tweet in possible_tweets if tweet not in recent_tweets]

    # UTC
    current_hour = int(datetime.now().strftime("%H"))

    # morning
    if current_hour > 6 and current_hour < 14:
        selected_tweet = possible_tweets[0]
    # afternoon
    elif current_hour > 14 and current_hour < 19:
        selected_tweet = possible_tweets[1]
    # night
    else:
        selected_tweet = possible_tweets[2]

    return selected_tweet


def lambda_handler(event, context):
    print("Get credentials")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    print("Authenticate")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    print("Get tweet from csv file")
    tweets_file = ROOT / "tweets.csv"
    # recent_tweets = api.user_timeline()[:3]
    tweet = get_tweet(tweets_file)

    print(f"Post tweet: {tweet}")
    api.update_status(tweet)

    return {"statusCode": 200, "tweet": tweet}
