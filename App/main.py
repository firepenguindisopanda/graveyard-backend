import os
from flask import Flask
from flask_login import LoginManager, current_user
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import timedelta
from flask_jwt_extended import JWTManager


from App.database import create_db

from App.views import (
    index_views,
    user_views,
    graveyard_views,
    grave_views,
    deceased_views,
    customer_views,
    reservation_views,
    payment_views
)

# New views must be imported and added to this list

views = [
    index_views,
    user_views,
    graveyard_views,
    grave_views,
    deceased_views,
    customer_views,
    reservation_views,
    payment_views
]

def add_views(app, views):
    for view in views:
        app.register_blueprint(view)


def loadConfig(app, config):
    app.config['ENV'] = os.environ.get('ENV', 'DEVELOPMENT')
    if app.config['ENV'] == "DEVELOPMENT":
        app.config.from_object('App.config')
        app.config['JWT_EXPIRATION_DELTA'] =  timedelta(days=7)
    else:
        app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['JWT_EXPIRATION_DELTA'] =  timedelta(days=int(os.environ.get('JWT_EXPIRATION_DELTA')))
        app.config['DEBUG'] = os.environ.get('ENV').upper() != 'PRODUCTION'
        app.config['ENV'] = os.environ.get('ENV')
        
    for key, value in config.items():
        app.config[key] = config[key]

def create_app(config={}):
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    loadConfig(app, config)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app, views)
    JWTManager(app)
    app.app_context().push()
    return app