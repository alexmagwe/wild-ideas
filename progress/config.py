from os import path,environ
from dotenv import load_dotenv

basedir=path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir,'.flaskenv'))
class Development:
    DB_NAME='progress'
    SECRET_KEY='7ca1b230ca5bcda875a3c5a1eb2babc20233226775f7619c904e8902a3a36e22'
    # SQLALCHEMY_DATABASE_URI='sqlite:////'+os.path.join(basedir,DB_NAME)+'.sqlite'
    SQLALCHEMY_DATABASE_URI=environ.get('DATABASE_URL')
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    FLASK_APP='app.py'
    DEBUG=True
    SSL_REDIRECT=True
class Production(object):
    SQLALCHEMY_DATABASE_URI=environ.get('DATABASE_URL')
    FLASK_APP='run.py'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SSL_REDIRECT=True
    LOG_TO_STDOUT = environ.get('LOG_TO_STDOUT')
configs={'development':Development,'production':Production}
	
