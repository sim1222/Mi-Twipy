import datetime

import tweepy
import requests
import json
from config import CONFIG
from misskey import Misskey
import time

# Twitter APIインスタンスを作成

consumer_key = CONFIG["CONSUMER_KEY"]
consumer_secret = CONFIG["CONSUMER_SECRET"]
access_token = CONFIG["ACCESS_TOKEN"]
access_token_secret = CONFIG["ACCESS_SECRET"]


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)

misskey_addr = CONFIG["MISSKEY_ADDRESS"]
misskey_token = CONFIG["MISSKEY_API"]

# Misskey APIインスタンスを作成
mk = Misskey(misskey_addr, misskey_token)

global last_tw_id
last_tw_id: int = 1




def gettw():
    #for tweet in public_tweets:
        global last_tw_id
        public_tweets = api.home_timeline(since_id=last_tw_id, count=40)

        if len(public_tweets) == 0:
            print("already noted")
            return


        for tweet in reversed(public_tweets):

            print()
            print("getting...")
            print("Last ID: " + str(last_tw_id))
            print("Tweet ID: " + str(tweet.id))
            print("Posted from: " + tweet.user.name)
            print("Posted Time: " + str(tweet.created_at))
            print(tweet.text)
            print()
            if tweet.id > last_tw_id:
                mk.notes_create(
                    text="ID: " + str(tweet.id) + "\n"
                         + "Name: " + tweet.user.name.translate(str.maketrans({'@': '＠', '#': '＃'})) + "\n"
                         + "Time: " + str(tweet.created_at) + "\n"
                         + "\n"
                         + tweet.text.translate(str.maketrans({'@': '＠', '#': '＃'})) + "\n"
                         + "https://twitter.com/" + str(tweet.user.screen_name) + "/status/" + str(tweet.id),
                    visibility="home",
                    #local_only=True
                )
                print("noted")
            else:
                print("already noted")
            time.sleep(2)


        last_tw_id = public_tweets[0].id



while True:
    try:
        start = time.time()
        gettw()
        print("lastID: " + str(last_tw_id))
        used_time = time.time() - start
        print("time: " + str(used_time))
        print("sleep...")
        if 60-used_time > 0:
            mk.notes_create(text="Sleep: " + str(int(60-used_time)) + "\n"
                            "Next: " + str(datetime.datetime.now() + datetime.timedelta(seconds=60-used_time)), visibility="home", local_only=True)
            time.sleep(60-used_time)

        else:
            mk.notes_create(text="Sleep: " + str(int(used_time)) + "\n"
                            "Next: " + str(datetime.datetime.now() + datetime.timedelta(seconds=used_time)), visibility="home", local_only=True)
            time.sleep(1)


    except TimeoutError:
        print("timeout")
        time.sleep(60)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print("timeout" + str(e))
        time.sleep(60)

