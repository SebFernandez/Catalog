from flask import Blueprint, session, redirect, url_for, request
from flask.templating import render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from application.models import User

auth = Blueprint ('auth', __name__)

@auth.route ('/login',  methods = ["GET", "POST"])
def login ():
    if request.method == "POST":
        email = request.form.get ("email")
        password = request.form.get ("password")
        
        user = User.query.filter_by(email=email).first ()
        
        if user and check_password_hash (user.password, password):
            login_user (user, remember=True)
            
            print ()
            print (f" * {user.username} has loged in.")
            print ()
            
            return redirect (url_for ('main.index'))
        
    return render_template ("login.html", user=current_user)
        

@auth.route ('/logout')
@login_required
def logout ():
    print ()
    print (f" * {current_user.username} has loged out.")
    print ()
    
    logout_user ()
    
    return redirect (url_for ('main.index'))

@auth.route ('/sign-in',  methods = ["GET", "POST"])
def sign_in ():
    if request.method == "POST":
        username = request.form.get ("username")
        email = request.form.get ("email")
        password = request.form.get ("password")
        
        if username and email and password:
            if not User.query.filter_by(email=email).first () and not User.query.filter_by(username=username).first ():
                new_user = User (email=email, username=username, password=generate_password_hash(password, method="sha256"))
                
                db.session.add (new_user)
                db.session.commit ()
                
                session ['loged'] = True
                login_user (new_user, remember=True)
                
                print ()
                print (" * New user was added to database.")
                print ()
                print (f" * Username:   {new_user.username}")
                print (f" * Email:      {new_user.email}")
                print (f" * Password:   {new_user.password}")
                print ()
            
                return redirect (url_for ('main.index'))
    
    return render_template ("sign_in.html", user=current_user)