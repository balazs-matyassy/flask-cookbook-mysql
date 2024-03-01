import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_TITLE = os.environ.get('APP_TITLE')
    APP_SUBTITLE = os.environ.get('APP_SUBTITLE')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_PORT = int(os.environ.get('DB_PORT') or 3306)
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_DATABASE = os.environ.get('DB_DATABASE')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or 4 * 1024 * 1024)
