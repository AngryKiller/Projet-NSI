from flask import Flask, render_template
import mysql.connector

cnx = mysql.connector.connect(user='root', password='digouraye',
                              host='127.0.0.1',
                              database='projet-nsi')

app = Flask(__name__, static_url_path='/static')

cursor = cnx.cursor()

cursor.execute("SELECT * FROM news")

news = cursor.fetchall()

@app.route('/')
def index():
    return render_template('index.html', news=news)

@app.route('/digou')
def test():
    return 'Digouraye'