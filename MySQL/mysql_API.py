import mysql.connector
import main_mysql
import collections
import random
from tqdm import tqdm

mydb = mysql.connector.connect(
    host = "localhost",
    user = "enter your user name",
    passwd = "enter your passward",
    database = 'users',
    auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()

def createdatabase():
    '''
    If you haven't created this database yet, please annotate line 7: database = users and run this function.
    '''

    mycursor.execute("CREATE DATABASE users")

def createtable():
    '''
    If you haven't created this table yet, please run this function.
    '''

    mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), searchid VARCHAR(255), picnum VARCHAR(255))")

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
        imgnum = main_mysql.get_tweet_pic(cus_id, picnum)

        sql = "INSERT INTO customers (username, searchid, picnum) VALUES (%s, %s, %s)"
        val = []
        val.append((user_name, cus_id, imgnum))

        mycursor.executemany(sql, val)
        mydb.commit()

def search(key):
    '''
    Use the searchid as key to search in our database, return a dictionary contain user who searched this id and time.
    '''

    mycursor.execute("SELECT username FROM customers WHERE searchid = '{}'".format(key))
    myresult = mycursor.fetchall()

    res = collections.defaultdict(int)
    for x in myresult:
        res[x[0]] += 1
    return dict(res)

def avgnum():
    '''
    Return the averange number of images per feed.
    '''

    sum = 0
    cnt = 0
    mycursor.execute("SELECT picnum FROM customers")
    myresult = mycursor.fetchall()

    for x in myresult:
        cnt += 1
        sum += int(x[0])

    return sum / cnt

def most_pop():
    '''
    Return the most popular descriptors and the time it has been searched.
    '''

    mycursor.execute("SELECT searchid FROM customers")
    myresult = mycursor.fetchall()

    col = collections.Counter()
    for x in myresult:
        col.update({x[0]: 1})
    return col.most_common(1)

if __name__ == '__main__':

    #createdatabase()
    #createtable()

    #print('Autofilling: ')
    #autofill()
    print('User who searched Tim Cook before: ', search('tim_cook'))
    print('Averange number of images per feed: ', avgnum())
    print('Most popular descriptors: ', most_pop())
