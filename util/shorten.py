import mysql.connector
import bcrypt
import string
import random
from dotenv import load_dotenv
from os import getenv

load_dotenv()

cnx = mysql.connector.connect(user=getenv("DB_USER"), password=getenv("DB_PASSWORD"),
                              host=getenv("DB_HOST"),
                              database=getenv("DB_NAME"))


def shortenGuest(url):
    letters = string.ascii_letters
    shortid = (''.join(random.choice(letters) for i in range(6)))
    cursor = cnx.cursor()
    sql = "INSERT INTO links (url, shorten) VALUES (%s, %s)"
    val = (url, shortid)
    cursor.execute(sql, val)
    cnx.commit()
    return shortid


def getlinkfromid(id):
    cursor = cnx.cursor()
    sql = "SELECT url FROM links WHERE shorten=%s"
    val = (id,)
    cursor.execute(sql, val)
    return cursor.fetchone()
