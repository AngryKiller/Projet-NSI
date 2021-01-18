import mysql.connector
import bcrypt

cnx = mysql.connector.connect(user='root', password='digouraye',
                              host='127.0.0.1',
                              database='projet-nsi')



def register(username, mail, password):
    salt = bcrypt.gensalt()
    hashedpw = bcrypt.hashpw(password.encode("utf-8"), salt)
    cursor = cnx.cursor()
    sql = "INSERT INTO users (username, mail, password) VALUES (%s, %s, %s)"
    val = (username, mail, hashedpw)
    cursor.execute(sql, val)
    cnx.commit()
    return True

