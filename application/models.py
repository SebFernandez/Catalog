from enum import unique
from .extensions import db

class Content (db.Model):
    id = db.Column (db.Integer, primary_key=True, autoincrement = True)
    name = db.Column (db.String (20), unique=True, nullable = False)
    year = db.Column (db.String (10), nullable = False)
    genre = db.Column (db.String (20), nullable = False)
    rating = db.Column (db.Float, nullable = False)
    user_rating = db.Column (db.Integer, nullable = False, default= 0)
    content_type = db.Column (db.String (10), nullable = False)
    
    def __init__ (self, name, year, genre, rating, content_type):
        self.name = name
        self.year = year
        self.genre = genre
        self.rating = rating
        self.user_rating = 0
        self.content_type = content_type