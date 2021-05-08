import mysql.connector
from dotenv import load_dotenv
from os import getenv
load_dotenv()

cnx = mysql.connector.connect(user=getenv("DB_USER"), password=getenv("DB_PASSWORD"),
                              host=getenv("DB_HOST"),
                              database=getenv("DB_NAME"))


def getSettings():
    cursor = cnx.cursor()
    sql = "SELECT * FROM settings WHERE id=1"
    cursor.execute(sql)
    return cursor.fetchone()


def updateSettings(title, desc):
    cursor = cnx.cursor()
    sql = "UPDATE settings SET title=%s, description=%s WHERE id=1"
    val = (title, desc, )
    cursor.execute(sql, val)
    return True