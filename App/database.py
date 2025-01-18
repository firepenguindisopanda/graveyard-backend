from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_migrate(app):
    return Migrate(app, db)

def create_db(app):
    db.init_app(app)
    db.create_all()
    
def init_db(app):
    db.init_app(app)