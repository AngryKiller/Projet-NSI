import mysql.connector
import bcrypt
from dotenv import load_dotenv
from os import getenv
load_dotenv()

cnx = mysql.connector.connect(user=getenv("DB_USER"), password=getenv("DB_PASSWORD"),
                              host=getenv("DB_HOST"),
                              database=getenv("DB_NAME"))


def register(username, mail, password):
    salt = bcrypt.gensalt()
    hashedpw = bcrypt.hashpw(password.encode("utf-8"), salt)
    cursor = cnx.cursor()
    sql = "INSERT INTO users (username, mail, password) VALUES (%s, %s, %s)"
    val = (username, mail, hashedpw)
    cursor.execute(sql, val)
    cnx.commit()
    return True


def login(username, password):
    cursor = cnx.cursor()
    sql = "SELECT * FROM users WHERE username=%s"
    val = (username, )
    cursor.execute(sql, val)
    userdata = cursor.fetchone()
    if userdata is None:
        return False
    else:
        if bcrypt.checkpw(password.encode("utf-8"), userdata[3].encode("utf-8")):
            return userdata[0]
        else:
            return False


def getUser(userid):
    cursor = cnx.cursor()
    sql = "SELECT * FROM users WHERE id=%s"
    val = (userid, )
    cursor.execute(sql, val)
    return cursor.fetchone()


def isAdmin(userid):
    cursor = cnx.cursor()
    sql = "SELECT admin FROM users WHERE id=%s"
    val = (userid, )
    cursor.execute(sql, val)
    return cursor.fetchone()[0]
