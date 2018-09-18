import tweepy
import json
import urllib.request
import sys

consumer_key = "dKvsn8YRgSICPa9PWbLL0VLz0"
consumer_secret = "moF5isCVG3CkKGc9GYUwfWMHaVAPYlSime3nd2EXLRYt0teMTp"
access_key = "804211084634689536-RJovRQ2u49VgM9U8xfesouPpiJmGG3O"
access_secret = "qIBxB527HcS5kPchwc7QS2s7eR8zVoM4zVwSZRkXR3HXF"

def get_tweet_pic(cus_id):

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    new_tweets = api.user_timeline(id = cus_id, count=20)
    all_tweets = []
    all_tweets.extend(new_tweets)
    oldest = all_tweets[-1].id - 1

    while len(new_tweets) > 0:

        new_tweets = api.user_timeline(id = cus_id, count=200, max_id=oldest)
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1

        if len(all_tweets) > 10:
            break

    tweets_images = []

    for i in all_tweets:
        try:
            if i.entities['media'][0]['type']=='photo':
                    tweets_images.append(i.entities['media'][0]['media_url'])
        except:
            pass

    for n in range(len(tweets_images)):
        url = str(tweets_images[n])
        picnum = "%04d" % n
        urllib.request.urlretrieve(url, f"jpg{picnum}.jpg")

    print(len(all_tweets))

cus_id = sys.argv
get_tweet_pic(cus_id)
