import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = "postgresql://mimynnjj:np_g5bc17eiHAiK25WNkSrZcCejH06WV@hattie.db.elephantsql.com/mimynnjj"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
