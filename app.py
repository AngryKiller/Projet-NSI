from flask import Flask, render_template, request, redirect, flash, session, url_for, send_from_directory
from util.news import getNews, deletearticle, addarticle, getArticle, editarticle
from util.users import register, login, getUser, isAdmin
from util.shorten import shortenGuest, getlinkfromid
from util.settings import getSettings, updateSettings
from util.images import getImages, deleteimage, addimage
from werkzeug.utils import secure_filename

import os

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__, static_url_path='/static')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = b'_5eey"F3z\digouc]/'


@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', news=getNews(), user=getUser(session['user']), settings=getSettings())
    else:
        return render_template('index.html', news=getNews(), settings=getSettings())


@app.route('/register', methods=['POST', 'GET'])
def registerRoute():
    if request.method == "POST":
        if register(request.form['username'], request.form['mail'], request.form['password']):
            flash('Vous avez été inscrit avec succès', 'green')
            return redirect('/')
    else:
        return render_template('register.html', settings=getSettings())

    return render_template('register.html', settings=getSettings())


@app.route('/login', methods=['POST', 'GET'])
def loginRoute():
    if request.method == "POST":
        user = login(request.form['username'], request.form['password'])
        if user:
            session['user'] = user
            flash('Vous êtes connecté!', 'green')
            return redirect('/')
        else:
            flash('Utilisateur ou mot de passe incorrect', 'red')
            return redirect('/login')
    else:
        return render_template('login.html', settings=getSettings())

    return render_template('login.html', settings=getSettings())


@app.route('/logout')
def logoutRoute():
    session.pop('user', None)
    return redirect('/')

@app.route('/img/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/admin', methods=['POST', 'GET'])
def adminRoute():
    if 'user' in session and isAdmin(session['user']):
        if request.method == 'POST':
            file = request.files['banner']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                res = updateSettings(request.form['websiteTitle'], request.form['websiteDesc'], filename)
                flash("Paramètres mis à jour!", 'green')
                return redirect('/admin')
            else:
                res = updateSettings(request.form['websiteTitle'], request.form['websiteDesc'], False)
                if res == True:
                    flash('Paramètres mis à jour!', 'green')
                    return redirect('/admin')
                else:
                    flash('Une erreur est survenue', 'red')
                    return redirect('/admin')
        else:
            return render_template('admin/index.html', user=getUser(session['user']), settings=getSettings())
    else:
        return redirect('/')

@app.route('/admin/')
def adminRedirect():
    return redirect('/admin')

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
        deletearticle(id)
        flash("L'actualité a été supprimée", 'green')
        return redirect('/admin/news')
    else:
        return redirect('/')

@app.route('/admin/news/add', methods=['POST', 'GET'])
def addnewsroute():
    if 'user' in session and isAdmin(session['user']):
        if request.method == "POST":
            res = addarticle(request.form['newsTitle'], request.form['newsContent'], session['user'])
            if res == True:
                flash("L'actualité a été ajoutée", "green")
                return redirect('/admin/news')
            else:
                flash("Une erreur est survenue lors de l'ajout", "red")
                return redirect('/admin/news')
        else:
            return render_template('admin/edit.html', user=getUser(session['user']))
    else:
        return redirect('/')

@app.route('/admin/news/edit', methods=['POST', 'GET'])
def editnewsroute():
    if 'user' in session and isAdmin(session['user']):
        if request.method == "POST":
            res = editarticle(request.form['id'], request.form['newsTitle'], request.form['newsContent'])
            if res == True:
                flash("L'actualité a été modifiée", "green")
                return redirect('/admin/news')
            else:
                flash("Une erreur est survenue lors de la modification", "red")
                return redirect('/admin/news')
        else:
            id = request.args.get('id', '')
            return render_template('admin/edit.html', user=getUser(session['user']), article=getArticle(id), edit=True)
    else:
        return redirect('/')


@app.route('/shorten', methods=['POST'])
def shorten():
    if request.form['url']:
        res = shortenGuest(request.form['url'])
        if res:
            flash("Voici votre lien: "+res, "blue")
            return redirect('/')

@app.route('/l/<shortid>')
def shortRedirect(shortid):
    print(getlinkfromid(shortid))
    url = getlinkfromid(shortid)[0]
    return redirect(url)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/images')
def images():
    if 'user' in session:
        return render_template('images.html', images=getImages(), user=getUser(session['user']), settings=getSettings())
    else:
        return render_template('images.html', images=getImages(), settings=getSettings())


@app.route('/admin/images')
def adminImages():
    if 'user' in session and isAdmin(session['user']):
        return render_template('admin/images.html', images=getImages(), user=getUser(session['user']))
    else:
        return redirect('/')

@app.route('/admin/images/delete')
def deleteimageroute():
    if 'user' in session and isAdmin(session['user']):
        id = request.args.get('id', '')
        deleteimage(id)
        flash("L'image a été supprimée", 'green')
        return redirect('/admin/images')
    else:
        return redirect('/')


@app.route('/admin/images/add', methods=['POST', 'GET'])
def imageAdd():
    if 'user' in session and isAdmin(session['user']):
        if request.method == 'POST':
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                res = addimage(request.form['imageTitle'], filename)
                flash("Image ajoutée!", 'green')
                return redirect('/admin/images')
            else:
                flash('Une erreur est survenue', 'red')
                return redirect('/admin/images')
        else:
            return render_template('admin/addimage.html', user=getUser(session['user']), settings=getSettings())
    else:
        return redirect('/')


@app.route('/digou')
def test():
    return 'Digouraye'