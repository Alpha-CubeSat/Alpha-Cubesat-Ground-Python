import sqlite3
from os.path import exists

from werkzeug.security import generate_password_hash

from config import users_db

create_users_table = """CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    token TEXT UNIQUE,
    token_expiration INTEGER
);"""

def create_user(db):
    username = input('Username: ')
    if user_exists(username):
        print(f'Error: User "{username}" already exists')
        return

    password = input('Password: ')
    password_hash = generate_password_hash(password)
    db.execute('INSERT INTO user (username, password_hash) VALUES (?, ?)',
               (username, password_hash))
    db.commit()
    print(f'Created User "{username}"')

def edit_user(db):
    username = input('Username: ')
    if not user_exists(username):
        print(f'Error: User "{username}" does not exist')
        return

    password = input('Password: ')
    password_hash = generate_password_hash(password)
    db.execute('UPDATE user SET password_hash = ? WHERE username = ?',
               (password_hash, username))
    db.commit()
    print(f'Edited User "{username}"')

def delete_user(db):
    username = input('Username: ')
    if not user_exists(username):
        print(f'Error: User "{username}" does not exist')
        return

    db.execute('DELETE FROM user WHERE username = ?', (username,))
    db.commit()
    print(f'Deleted User "{username}"')

def list_users(db):
    users = db.execute('SELECT username FROM user').fetchall()
    if len(users) > 0:
        print('Current Control Users:')
        for user in users: print(user[0])
    else:
        print('No Users')

def init_table(db):
    db.execute(create_users_table)
    db.commit()
    print('Users Database Created')

def reset_table(db):
    db.execute('DROP TABLE user')
    db.execute(create_users_table)
    db.commit()
    print('Control Users Reset')

def user_exists(username):
    return db.execute('SELECT COUNT(*) FROM user WHERE username = ?', (username,)) \
        .fetchone()[0] != 0

# create database if it does not exist
if not exists(users_db):
    init_table(sqlite3.connect(users_db))

db = sqlite3.connect(users_db)

while True:
    print('CubeSat Backend CLI Tools\n'
          'Options:\n'
          '1. Create Control User\n'
          '2. Edit Control User\n'
          '3. Delete Control User\n'
          '4. List Control Users\n'
          '5. Reset Control Users\n'
          '6. Exit')
    option = input('Choose an Option: ')
    if option == '1':
        create_user(db)
    elif option == '2':
        edit_user(db)
    elif option == '3':
        delete_user(db)
    elif option == '4':
        list_users(db)
    elif option == '5':
        reset_table(db)
    elif option == '6':
        db.close()
        print('Exiting')
        break
    else:
        print('Invalid Option')