import sqlite3
from os.path import exists

import click
from flask import g
from werkzeug.security import generate_password_hash

from config import users_db


def get_db() -> sqlite3.Connection:
    if 'db' not in g:
        g.db = sqlite3.connect(users_db)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    # create database if it does not exist and create admin user
    if not exists(users_db):
        db = sqlite3.connect(users_db)
        db.execute("""CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            token TEXT UNIQUE,
            token_expiration INTEGER
        )""")
        db.execute('INSERT INTO user (username, password_hash) VALUES (?, ?)',
                         ('admin', generate_password_hash('admin')))
        db.commit()
        print('Users Database Created')


# Use "flask init-db" in the terminal to create the db manually
# https://flask.palletsprojects.com/en/2.3.x/tutorial/database/
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    init_db()
    app.cli.add_command(init_db_command)
    app.teardown_appcontext(close_db)
