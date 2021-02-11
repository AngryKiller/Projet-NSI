import mysql.connector

cnx = mysql.connector.connect(user='root', password='digouraye',
                              host='127.0.0.1',
                              database='projet-nsi')



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
    val = (id, )
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
