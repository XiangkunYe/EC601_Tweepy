import pymongo
import main_mongo
import collections
import random
from tqdm import tqdm

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["tweepy"]
mycol = mydb["users"]

def autofill():

    namedic = ['Kun', 'Pang', 'Wan', 'Su', 'Chen', 'Jack', 'Steve', 'Jobs', 'Tim', 'Cook']
    iddic = ['tim_cook', 'RED', 'zaralarsson', 'BlackButterRecs', 'FlippDinero', 'NBA', 'ThonMaker14', 'Tesla', 'elonmusk', 'BillGates']
    numdic = ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100']

    for i in tqdm(range(100)):
        user_name = random.choice(namedic)
        cus_id = random.choice(iddic)
        picnum = random.choice(numdic)
        imgnum = main_mongo.get_tweet_pic(cus_id, picnum)
        mycol.insert_one({'username': user_name, 'searchid': cus_id, 'picnum': imgnum})

def search(key):

    res = collections.defaultdict(int)
    for x in mycol.find({'searchid': key}):
        res[x['username']] += 1
    return dict(res)

def avgnum():

    sum = 0
    cnt = 0
    for x in mycol.find():
        cnt += 1
        sum += int(x['picnum'])

    return sum/cnt

def most_pop():

    col = collections.Counter()
    for x in mycol.find():
        col.update({x['searchid']: 1})
    return col.most_common(1)

if __name__ == '__main__':
    #autofill()
    print(search('tim_cook'))
    print(avgnum())
    print(most_pop())
