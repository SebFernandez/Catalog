from flask import Flask
from .extensions import db
from .main.views import main

def create_app ():
    app = Flask (__name__)
    
    app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    #! Without app.secret_key I can't use session object.
    app.secret_key = '1234'
    
    db.init_app (app)
    
    app.register_blueprint (main)
    
    return app