import os

DEBUG = True
SECRET_KEY = 'secret key!'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        os.path.dirname(__file__), '../data-dev.sqlite3')
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"

