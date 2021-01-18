from flask import Flask, render_template, request, redirect
from util.news import getNews
from util.users import register

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html', news=getNews())

@app.route('/register', methods=['POST', 'GET'])
def registerRoute():
    if request.method == "POST":
        if register(request.form['username'], request.form['mail'], request.form['password']):
            return redirect('/')
    else:
        return render_template('register.html')

    return render_template('register.html')


@app.route('/digou')
def test():
    return 'Digouraye'