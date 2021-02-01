from flask import Blueprint, url_for, render_template, request, redirect, session
from application.models import User
from application.extensions import db
from operator import itemgetter
import requests

main = Blueprint('main', __name__)

@main.route ('/', methods = ["GET", "POST"])
def index ():
    if request.method == "GET":
        if 'loged' not in session:
            User.query.delete()
            db.session.commit ()
            
            return render_template ("index.html")
        else:
            information = User.query.all()
            
            return render_template ("index.html", edit = False, information=information)
    if request.method == "POST":
        print ("hola")
        
        if request.form.get ("delete") == 'delete':
            title = request.form.get ("name")
            
            #! Returns models object. movie.id -> ID, movie.name -> name, movie.password -> password.
            movie = User.query.filter_by(name=title).first()
            
            if (movie):
                db.session.delete(movie)
                db.session.commit ()
            
            return redirect (url_for ('main.index'))
        
        elif request.form.get ("edit") == 'edit':
            title = request.form.get ("name")
            
            return redirect (url_for ('main.edit', movie_name = title))

@main.route ('/search', methods = ["GET", "POST"])
def search ():
    if request.method == "POST":
        user_search = request.form.get ("name").replace (' ', '+')
        
        return redirect (url_for('main.search_results', name = user_search))
    
    return render_template ("search.html")

@main.route ('/search/<name>',  methods = ["GET", "POST"])
def search_results(name):
    if request.method == "GET":
        URL = 'https://www.omdbapi.com/?s=' + name + '&apikey=678cd26e'
        
        q = requests.get(url=URL)
        r = q.json()
            
        d = {}
        dlist = []
            
        if q.status_code == 200:
            if r['Response'] == 'True':
                for i in r['Search']:
                    d = {
                        'Title' : i.get ('Title'),
                        'Year' : i.get ('Year')
                    }
                        
                    dlist.append (d)
                
                #! Param 'key' needs the key to sort.            
                rlist = sorted (dlist, key=itemgetter ('Title'), reverse=False)
                
                return render_template ("search.html", table=True, list = rlist)
        
        return redirect(url_for('main.search'))
    
    elif request.method == "POST":
        title = request.form.get ("title")
        year = request.form.get ("year")
        
        if not bool(User.query.filter_by(name=title).first()):
        
            new_movie = User (name=title, password=year)
            
            print (title, year)
            
            db.session.add (new_movie)
            db.session.commit ()
        
        return redirect (url_for("main.index"))

@main.route ('/edit/<movie_name>', methods = ["GET", "POST"])
def edit (movie_name):
    movie = User.query.filter_by(name=movie_name).first()
    
    if request.method == "GET":
        return render_template ("index.html", edit = True, id = movie.id, name = movie.name)
    
    elif request.method == "POST":
    
        movie.password = request.form.get ('year')
    
        db.session.commit ()
    
        return redirect (url_for ('main.index'))
   
@main.route ('/login')
def login ():
    session['loged'] = True
    
    return redirect (url_for ('main.index'))

@main.route ('/logout')
def logout ():
    session.pop ('loged', None)
    
    return redirect (url_for ('main.index'))

'''
@main.route ('/add', methods = ["GET", "POST"])
def add ():
    if request.method == "POST":
            name = request.form.get ("username")
            password = request.form.get ("password")
            
            print (name, password)
            
            new_user = User (name=name, password=password)
            
            #! Query to check if a row already exists.
            if not bool(User.query.filter_by(name=new_user.name).first()):    
                db.session.add (new_user)
                db.session.commit ()
                
                return redirect (url_for("main.index"))
            else:
                User.query.delete()
                db.session.commit ()
                
                return 'No'
                
'''