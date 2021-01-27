from flask import Blueprint, url_for, render_template, request, redirect, session
from application.models import User
from application.extensions import db

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