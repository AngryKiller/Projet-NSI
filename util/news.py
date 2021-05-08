import mysql.connector
from dotenv import load_dotenv
from os import getenv
load_dotenv()

cnx = mysql.connector.connect(user=getenv("DB_USER"), password=getenv("DB_PASSWORD"),
                              host=getenv("DB_HOST"),
                              database=getenv("DB_NAME"))



def getNews():
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM news ORDER BY id DESC")
    return cursor.fetchall()

def getArticle(id):
    cursor = cnx.cursor()
    sql = "SELECT * FROM news WHERE id=%s"
    val = (id, )
    cursor.execute(sql, val)
    return cursor.fetchone()


def deletearticle(id):
    cursor = cnx.cursor()
    sql = "DELETE FROM news WHERE id=%s"
    val = (id,)
    cursor.execute(sql, val)
    return True

def addarticle(title, content, author):
    cursor = cnx.cursor()
    sql = "INSERT INTO news (title, content, author) VALUES (%s, %s, %s)"
    val = (title, content, author, )
    cursor.execute(sql, val)
    return True

def editarticle(id, title, content):
    cursor = cnx.cursor()
    sql = "UPDATE news SET title=%s, content=%s WHERE id=%s"
    val = (title, content, id, )
    cursor.execute(sql, val)
    return True
