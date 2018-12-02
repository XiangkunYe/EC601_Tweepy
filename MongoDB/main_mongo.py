import tweepy
import json
import urllib.request
import sys
import os
import io
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw, ImageFont
import pymongo

consumer_key = 'input your consumer key'
consumer_secret = 'input your consumer secret'
access_key = 'input your access token'
access_secret = 'input your access token secret'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="input the path you save the google vision key json file"


def get_tweet_pic(cus_id, picnum):
    '''
    Download pictures in Twitter according to the id 'cus_id' and number 'picnum'.
    '''

    curdir = os.getcwd()
    if 'result' not in curdir:
        curdir += "/result"
        folder = curdir + '/' + cus_id
    else:
        folder = curdir + '/' + cus_id

    if not os.path.exists(folder):
        os.makedirs(folder)

    os.chdir(folder + '/')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    new_tweets = api.user_timeline(id=cus_id, count=10)
    all_tweets = []
    all_tweets.extend(new_tweets)
    oldest = all_tweets[-1].id - 1

    while len(new_tweets) > 0:

        if int(picnum) <= 200:
            new_tweets = api.user_timeline(
                id=cus_id, count=int(picnum), max_id=oldest)
        else:
            new_tweets = api.user_timeline(id=cus_id, count=200, max_id=oldest)

        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1

        if len(all_tweets) > int(picnum):
            break

    tweets_images = []

    for i in all_tweets:
        try:
            if i.entities['media'][0]['type'] == 'photo':
                tweets_images.append(i.entities['media'][0]['media_url'])
        except BaseException:
            pass

    for n in range(len(tweets_images)):
        url = str(tweets_images[n])
        picnum = "%04d" % n
        urllib.request.urlretrieve(url, f"jpg{picnum}.jpg")

    os.chdir(curdir + '/')
    return len(tweets_images)


def analypic(cus_id):
    '''
    Use Google Vision API to analyze the picture in folder 'cus_id'.
    '''

    curdir = os.getcwd()
    os.chdir(curdir + '/' + cus_id + '/')
    picname = list(os.popen('ls'))

    for pic in picname:

        if '.jpg' in pic:

            pict = pic.strip()
            client = vision.ImageAnnotatorClient()

            file_name = os.path.join(
                os.path.dirname(__file__), pict)

            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)

            response = client.label_detection(image=image)
            labels = response.label_annotations

            im = Image.open(file_name)
            draw = ImageDraw.Draw(im)
            labeldes = []

            for label in labels:
                labeldes.append(label.description + '\n')

            labeldcp = ''.join(labeldes)
            myfont = ImageFont.truetype("Chalkduster.ttf", 35)
            fillcolor = 'red'

            draw.text((50, 40), labeldcp, font=myfont, fill=fillcolor)
            im.save(file_name, 'JPEG')

    os.chdir(curdir + '/')


def pic2mp4(cus_id):
    '''
    Make pictures in folder 'cus_id' into video.
    '''

    curdir = os.getcwd()
    os.chdir(curdir + '/' + cus_id + '/')

    os.popen(
        'ffmpeg -framerate 24 -r 1 -i jpg%04d.jpg -t 600 -vf scale=1280:720 output.mp4')

    os.chdir(curdir + '/')


def main():

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["tweepy"]
    mycol = mydb["users"]

    user_name = input('Please input your user name: ')
    cus_id = input(
        'Please input the ID of twitter account you want to search: ')
    picnum = input('Please input the number of tweets you want to search: ')
    print('Image download start!')

    try:
        imgnum = get_tweet_pic(cus_id, picnum)
    except BaseException:
        print('Opps, you might enter a wrong id or invaild number, please try again.')
        main()

    print('Image download finish!')
    print('Image analysis start!')

    try:
        analypic(cus_id)
    except BaseException:
        print("Opps, maybe you forget to export the directory of GoogleVision's key? Please try again.")
        sys.exit()

    print('Image analysis finish!')

    try:
        pic2mp4(cus_id)
    except BaseException:
        print('Opps, maybe you forget to install ffmpeg? Please try again.')
        sys.exit()

    mycol.insert_one(
        {'username': user_name, 'searchid': cus_id, 'picnum': imgnum})

    print('Mission Complete')
    sys.exit()


if __name__ == '__main__':
    main()
