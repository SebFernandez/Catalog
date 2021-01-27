from enum import unique
from .extensions import db

class User (db.Model):
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column (db.String (20), unique=True, nullable = False)
    password = db.Column (db.String (20), unique=True, nullable = False)
    
    def __init__ (self, name, password):
        self.name = name
        self.password = password