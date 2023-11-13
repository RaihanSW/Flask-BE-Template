# config.py
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s' % (os.environ.get('DB_USER'), os.environ.get('DB_PASSWORD'), os.environ.get('DB_HOST'), os.environ.get('DB_PORT'), os.environ.get('DB_NAME'))
    # SQLALCHEMY_BINDS = {
    #     # 'sisco': 'mysql+pymysql://%s:%s@%s:%s/%s' % (os.environ.get('SISCO_DB_USER'), os.environ.get('SISCO_DB_PASSWORD'), os.environ.get('SISCO_DB_HOST'), os.environ.get('SISCO_DB_PORT'), os.environ.get('SISCO_DB_NAME')),
    #     # 'branch': 'mysql+pymysql://%s:%s@%s:%s/jnamicro_branch' % (os.environ.get('DB_USER'), os.environ.get('DB_PASSWORD'), os.environ.get('DB_HOST'), os.environ.get('DB_PORT')),
    # }

class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TrainingConfig(Config):
    ENV = "training"
    DEBUG = False
    SQLALCHEMY_ECHO = False

class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
    SQLALCHEMY_ECHO = False
