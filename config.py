import os

from dotenv import load_dotenv
load_dotenv(verbose=True)

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'this bagaça'

