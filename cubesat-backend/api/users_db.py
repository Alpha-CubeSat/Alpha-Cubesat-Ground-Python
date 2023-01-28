import sqlite3

from flask import g

# import user_gen_cli
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
    db = get_db()

    # user_gen_cli.init_table(db)

# https://flask.palletsprojects.com/en/2.2.x/tutorial/database/
# @click.command('init-db')
# def init_db_command():
#     init_db()
#     click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    # app.cli.add_command(init_db_command)