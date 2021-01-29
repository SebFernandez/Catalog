from flask import Blueprint, url_for, render_template, request, redirect, session
from application.models import User
from application.extensions import db
from operator import itemgetter
import requests

main = Blueprint('main', __name__)

@main.route ('/')
def index ():
    if 'loged' not in session:
        User.query.delete()
        db.session.commit ()
        
        return render_template ("index.html")
    else:
        information = User.query.all()
        
        return render_template ("index.html", information=information)

@main.route ('/search', methods = ["GET", "POST"])
def search ():
    if request.method == "POST":
        user_search = request.form.get ("name").replace (' ', '+')
        
        return redirect (url_for('main.search_results', name = user_search))
    
    return render_template ("search.html")

@main.route ('/search/<name>')
def search_results(name):
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
                
            rlist = sorted (dlist, key=itemgetter ('Title'), reverse=False)
            
    return render_template ("search.html", table=True, list = rlist)
    
@main.route ('/login')
def login ():
    session['loged'] = True
    
    return redirect (url_for ('main.index'))

@main.route ('/logout')
def logout ():
    session.pop ('loged', None)
    
    return redirect (url_for ('main.index'))

@main.route ('/add', methods = ["GET", "POST"])
def add ():
    if request.method == "GET":
        return render_template ("add.html")
    elif request.method == "POST":
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