import time
import mysql.connector


def connect_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="chess"
        )
        print('connected to db')
        return db
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)
        return None


def get_rating(key):
    db = connect_db()
    dbCursor = db.cursor()
    print(key)
    dbCursor.execute('SELECT `rating` FROM `data` WHERE `key` = %s', (key,))
    rating = dbCursor.fetchall()
    dbCursor.close()
    db.close()
    if len(rating) == 0:
        return 'error'
    return str(rating[0][0])


def change_rating(key, value):
    db = connect_db()
    dbCursor = db.cursor()
    rating = dbCursor.execute('''SELECT rating FROM data WHERE key= %s''', (str(key),)).fetchall()
    if len(rating) > 0:
        if rating[0][0] + value >= 0:
            rating = rating[0][0] + value
            dbCursor.execute('''UPDATE data SET rating=%s WHERE key= %s''', (rating, key,))
        db.commit()
    dbCursor.close()
    db.close()


def register_user(params):
    params = params.split('\n')
    login = params[0]
    password = params[1]
    print(login + password)
    db = connect_db()
    dbCursor = db.cursor()
    info = dbCursor.execute('''SELECT id FROM data WHERE username = %s''', (login,)).fetchall()
    if not len(info):
        key = hash(str(time.time()))
        dbCursor.execute('''INSERT into data(username, password, key) VALUES (%s, %s, %s)''', (login, password, key))

        db.commit()
        dbCursor.close()
        db.close()

        return str(key)

    return 'error'


def login_user(params):
    params = params.split('\n')
    login = params[0]
    password = params[1]
    db = connect_db()
    dbCursor = db.cursor()
    dbCursor.execute('SELECT `key` FROM `data` WHERE `username` = %s and `password` = %s', (login, password))
    key = dbCursor.fetchall()
    dbCursor.close()
    db.close()
    if not len(key):
        return 'error'
    return str(key[0][0])
