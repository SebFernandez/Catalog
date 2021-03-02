from flask_login import UserMixin
from sqlalchemy.orm import backref
from . import db

'''
CREATE DB

#!Open Python editor

>>> from application.extensions import db
>>> from application import create_app
>>> db.create_all(app=create_app())

#! This will create DB inside of application folder
#! Then enter

sqlite3 application/db.sqlite3

#! Once you are in SQLite, enter '.tables' to check if there are tables
'''

class Content (db.Model):
    id = db.Column (db.Integer, primary_key=True, autoincrement = True)
    name = db.Column (db.String (20), unique=True, nullable = False)
    year = db.Column (db.String (10), nullable = False)
    genre = db.Column (db.String (20), nullable = False)
    rating = db.Column (db.Float, nullable = False)
    user_rating = db.Column (db.Integer, nullable = False, default= 0)
    content_type = db.Column (db.String (10), nullable = False)
    user_id = db.Column (db.Integer, db.ForeignKey ('user.id'), nullable = False)
    
    def __init__ (self, name, year, genre, rating, content_type, user_id):
        self.name = name
        self.year = year
        self.genre = genre
        self.rating = rating
        self.user_rating = 0
        self.content_type = content_type
        self.user_id = user_id
        
class User (db.Model, UserMixin):
    id = db.Column (db.Integer, primary_key = True, autoincrement = True)
    username = db.Column (db.String (50), unique = True, nullable = False)
    email = db.Column (db.String (20), unique = True, nullable = False)
    password = db.Column (db.String (20), nullable = False)
    catalog = db.relationship ('Content', order_by = 'Content.name')
    
    def __init__ (self, username, email, password):
        self.username = username
        self.email = email
        self.password = password