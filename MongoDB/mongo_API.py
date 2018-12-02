import pymongo
import main_mongo
import collections
import random
from tqdm import tqdm

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["tweepy"]
mycol = mydb["users"]


def autofill():
    '''
    Create some fake datas into our database for test.
    '''

    namedic = [
        'Kun',
        'Pang',
        'Wan',
        'Su',
        'Chen',
        'Jack',
        'Steve',
        'Jobs',
        'Tim',
        'Cook']
    iddic = [
        'tim_cook',
        'RED',
        'zaralarsson',
        'BlackButterRecs',
        'FlippDinero',
        'NBA',
        'ThonMaker14',
        'Tesla',
        'elonmusk',
        'BillGates']
    numdic = ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100']

    for i in tqdm(range(100)):
        user_name = random.choice(namedic)
        cus_id = random.choice(iddic)
        picnum = random.choice(numdic)
        imgnum = main_mongo.get_tweet_pic(cus_id, picnum)
        mycol.insert_one(
            {'username': user_name, 'searchid': cus_id, 'picnum': imgnum})


def search(key):
    '''
    Use the searchid as key to search in our database, return a dictionary contain user who searched this id and time.
    '''

    res = collections.defaultdict(int)
    for x in mycol.find({'searchid': key}):
        res[x['username']] += 1
    return dict(res)


def avgnum():
    '''
    Return the averange number of images per feed.
    '''

    sum = 0
    cnt = 0
    for x in mycol.find():
        cnt += 1
        sum += int(x['picnum'])

    return sum / cnt


def most_pop():
    '''
    Return the most popular descriptors and the time it has been searched.
    '''

    col = collections.Counter()
    for x in mycol.find():
        col.update({x['searchid']: 1})
    return col.most_common(1)


if __name__ == '__main__':
    
    print('Autofilling: ')
    autofill()
    print('User who searched Tim Cook before: ', search('tim_cook'))
    print('Averange number of images per feed: ', avgnum())
    print('Most popular descriptors: ', most_pop())
