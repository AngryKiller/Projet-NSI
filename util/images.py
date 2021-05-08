import mysql.connector
from dotenv import load_dotenv
from os import getenv
load_dotenv()

cnx = mysql.connector.connect(user=getenv("DB_USER"), password=getenv("DB_PASSWORD"),
                              host=getenv("DB_HOST"),
                              database=getenv("DB_NAME"))



def getImages():
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM images ORDER BY id DESC")
    return cursor.fetchall()


def deleteimage(id):
    cursor = cnx.cursor()
    sql = "DELETE FROM images WHERE id=%s"
    val = (id, )
    cursor.execute(sql, val)
    return True


def addimage(title, file):
    cursor = cnx.cursor()
    sql = "INSERT INTO images (title, image) VALUES (%s, %s)"
    val = (title, file, )
    cursor.execute(sql, val)
    return True