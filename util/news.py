import mysql.connector

cnx = mysql.connector.connect(user='root', password='digouraye',
                              host='127.0.0.1',
                              database='projet-nsi')



def getNews():
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM news ORDER BY id DESC")
    return cursor.fetchall()
