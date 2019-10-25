import os

ADMINS = ['gokhancacan3@gmail.com']
DEBUG = False
SECRET_KEY = 'top secret!'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        os.path.dirname(__file__), '../data.sqlite3')
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"



