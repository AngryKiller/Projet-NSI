from flask import Flask, render_template, request, redirect, flash, session
from util.news import getNews, deleteNews
from util.users import register, login, getUser, isAdmin

app = Flask(__name__, static_url_path='/static')

app.secret_key = b'_5eey"F3z\digouc]/'


@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', news=getNews(), user=getUser(session['user']))
    else:
        return render_template('index.html', news=getNews())


@app.route('/register', methods=['POST', 'GET'])
def registerRoute():
    if request.method == "POST":
        if register(request.form['username'], request.form['mail'], request.form['password']):
            flash('Vous avez été inscrit avec succès', 'success')
            return redirect('/')
    else:
        return render_template('register.html')

    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def loginRoute():
    if request.method == "POST":
        user = login(request.form['username'], request.form['password'])
        if user:
            session['user'] = user
            flash('Vous êtes connecté!', 'success')
            return redirect('/')
    else:
        return render_template('login.html')

    return render_template('login.html')


@app.route('/logout')
def logoutRoute():
    session.pop('user', None)
    return redirect('/')


@app.route('/admin')
def adminRoute():
    if 'user' in session and isAdmin(session['user']):
        return render_template('admin/index.html', user=getUser(session['user']))
    else:
        return redirect('/')

@app.route('/admin/news')
def adminNewsRoute():
    if 'user' in session and isAdmin(session['user']):
        return render_template('admin/news.html', user=getUser(session['user']), news=getNews())
    else:
        return redirect('/')

@app.route('/admin/news/delete')
def deletenewsroute():
    if 'user' in session and isAdmin(session['user']):
        id = request.args.get('id', '')
        deleteNews(id)
        flash("L'actualité a été supprimée", 'success')
        return redirect('/admin/news')
    else:
        return redirect('/')



@app.route('/digou')
def test():
    return 'Digouraye'