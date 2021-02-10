import mysql.connector

cnx = mysql.connector.connect(user='root', password='digouraye',
                              host='127.0.0.1',
                              database='projet-nsi')



def getNews():
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM news ORDER BY id DESC")
    return cursor.fetchall()

def deleteNews(id):
    cursor = cnx.cursor()
    sql = "DELETE FROM news WHERE id=%s"
    val = (id, )
    cursor.execute(sql, val)
    return True

def addNews(title, content, author):
    cursor = cnx.cursor()
    sql = "INSERT INTO news (title, content, author) VALUES (%s, %s, %s)"
    val = (title, content, author, )
    cursor.execute(sql, val)
    return True

