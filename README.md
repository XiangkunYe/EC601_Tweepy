# Twitter Image Analysis Using Google Vision

Hello! I'm Xiangkun Ye and I write this tweepy project for EC601.

Just as their name, the twe folder **MongoDB** and **MySQL** is for MongoDB and MySQL respectively.

## Before start:

  1. Using pip to install **tweepy**, **Pillow**, **tqdm**, **pymongo** and **mysql-connector-python**.
  
  2. Install [MongoDB](https://www.mongodb.com) and [MySQL](https://www.mysql.com/downloads/) and [ffmpeg](https://www.ffmpeg.org/download.html)
  
  3. Change the **consumer_key/secret**, **access_key/secret**, **GOOGLE_APPLICATION_CREDENTIALS** in **main_mongo/mysql.py** into your own, for **main_mysql.py**, please also **change** the **user** and passwd into your own.
  
  4. If you want to use the MySQL version, please be sure to create the **users** database and **customers** table using createdatabase and createtable in mysql_API.py

## Usage

### 1. Run directly
Both of **main_mongo/mysql.py** and **mongo/mysql_API.py** can be run directly, just do it and follow the instruction!

### 2. Use as API
Also both of them contain several API, every API have a brief introduction in the beginning tell you it's main function, please import to use them!
  
Have fun with them! If there's any bug, please tell me, if you're professor or TA, please give me a good grade!

