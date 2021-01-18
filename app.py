from flask import Flask, render_template
from util.news import getNews
import mysql.connector


app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html', news=getNews())

@app.route('/digou')
def test():
    return 'Digouraye'