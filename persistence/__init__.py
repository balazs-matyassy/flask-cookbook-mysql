import click
import pymysql
import pymysql.cursors
from flask import g, current_app
from pymysql.constants import CLIENT
from werkzeug.security import generate_password_hash


def init_app(app):
    app.cli.add_command(__install_command)
    app.before_request(__connect)
    app.teardown_appcontext(__disconnect)


def get_connection(multi_statements=False):
    client_flag = CLIENT.MULTI_STATEMENTS if multi_statements else 0

    return pymysql.connect(
        host=current_app.config['DB_HOST'],
        port=current_app.config['DB_PORT'],
        user=current_app.config['DB_USERNAME'],
        password=current_app.config['DB_PASSWORD'],
        database=current_app.config['DB_DATABASE'],
        cursorclass=pymysql.cursors.DictCursor,
        client_flag=client_flag
    )


def install():
    with get_connection(True) as db:
        with current_app.open_resource('schema.sql') as file:
            digest = generate_password_hash('Admin123.')

            with db.cursor() as cursor:
                cursor.execute(file.read().decode('utf8'), {'password': digest})
                db.commit()


@click.command('install')
def __install_command():
    install()

    click.echo('Application installation successful.')


def __connect():
    if 'db' not in g:
        g.db = get_connection()


def __disconnect(e):
    if 'db' in g:
        g.pop('db').close()
