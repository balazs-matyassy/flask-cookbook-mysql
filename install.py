from app import create_app
from persistence import install

with create_app().app_context():
    install()

    print('Application installation successful.')
