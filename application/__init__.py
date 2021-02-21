from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy ()
DB_NAME = "database.db"

def create_app ():
    app = Flask (__name__)
    
    app.config ['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    #! Without app.secret_key I can't use session object.
    app.secret_key = '1234'
    
    db.init_app (app)
    
    from .views import main
    from .auth import auth
    
    app.register_blueprint (main, url_prefix = '/')
    app.register_blueprint (auth, url_prefix = '/auth')
    
    #! We import all the file to see that it's working
    from .models import User, Content
    
    create_database (app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.session_protection = "strong"
    login_manager.init_app (app)
    
    @login_manager.user_loader
    def load_user (id):
        return User.query.get (int (id))
    
    return app

#! This function will create a DB in case of not existing.
def create_database (app):
    if not path.exists ('application/' + DB_NAME):
        say_hello ()
        
        db.create_all (app=app)
        print (" * Database created!")
        print ()
        
def say_hello ():
    print()
    print("┌────────────────────────────────────────────────────────────────────────────────┐")
    print("|                                                                                |")
    print("|          Welcome! This is Catalog.                                             |")
    print("|                                                                                |")
    print("|          Github repository: https://github.com/SebFernandez/Catalog            |")
    print("|                                                                                |")
    print("|          Created by Sebastián Fernandez.                                       |")
    print("|                                                                                |")
    print("└────────────────────────────────────────────────────────────────────────────────┘")
    print()