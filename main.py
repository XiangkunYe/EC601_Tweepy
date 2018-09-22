import tweepy
import json
import urllib.request
import sys
import os
import io
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw, ImageFont

consumer_key = "dKvsn8YRgSICPa9PWbLL0VLz0"
consumer_secret = "moF5isCVG3CkKGc9GYUwfWMHaVAPYlSime3nd2EXLRYt0teMTp"
access_key = "804211084634689536-RJovRQ2u49VgM9U8xfesouPpiJmGG3O"
access_secret = "qIBxB527HcS5kPchwc7QS2s7eR8zVoM4zVwSZRkXR3HXF"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/yxk/Documents/Python/601/GoogleVisionKey.json"

def get_tweet_pic(cus_id, picnum):

    folder = os.getcwd()+"/result"

    if not os.path.exists(folder):
        os.makedirs(folder)

    os.chdir(folder+'/')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    new_tweets = api.user_timeline(id = cus_id, count=10)
    all_tweets = []
    all_tweets.extend(new_tweets)
    oldest = all_tweets[-1].id - 1

    while len(new_tweets) > 0:

        if int(picnum) <= 200:
            new_tweets = api.user_timeline(id = cus_id, count=int(picnum), max_id=oldest)
        else:
            new_tweets = api.user_timeline(id = cus_id, count=200, max_id=oldest)

        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1

        if len(all_tweets) > int(picnum):
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

def analypic():

    picname = list(os.popen('ls'))

    for pic in picname:

        if '.jpg' in pic:

            pict = pic.strip()
            client = vision.ImageAnnotatorClient()

            file_name = os.path.join(
                os.path.dirname(__file__),
                pict)

            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)

            response = client.label_detection(image=image)
            labels = response.label_annotations

            im = Image.open(file_name)
            draw = ImageDraw.Draw(im)
            labeldes = []

            for label in labels:
                labeldes.append(label.description+'\n')

            labeldcp = ''.join(labeldes)
            myfont = ImageFont.truetype("Chalkduster.ttf", 35)
            fillcolor = 'red'

            draw.text((50, 40), labeldcp, font=myfont, fill=fillcolor)
            im.save(file_name, 'JPEG')

def pic2mp4():
    os.popen('ffmpeg -framerate 24 -r 1 -i jpg%04d.jpg -t 600 -vf scale=1280:720 output.mp4')

def main():
    cus_id = input('Please input the ID of twitter account you want to search: ')
    picnum = input('Please input the number of tweets you want to search: ')
    print('Image download start!')

    try:
        get_tweet_pic(cus_id, picnum)
    except:
        print('Opps, you might enter a wrong id or invaild number, please try again.')
        main()

    print('Image download finish!')
    print('Image analysis start!')

    try:
        analypic()
    except:
        print("Opps, maybe you forget to export the directory of GoogleVision's key? Please try again.")
        sys.exit()

    print('Image analysis finish!')

    try:
        pic2mp4()
    except:
        print('Opps, maybe you forget to install ffmpeg? Please try again.')
        sys.exit()

    print('Mission Complete')
    sys.exit()

if __name__ == '__main__':
    main()
