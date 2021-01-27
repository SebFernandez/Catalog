from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy ()

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