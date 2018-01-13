import sqlite3
from hashlib import md5
import os
from flask import Flask, flash, render_template, request

app = Flask(__name__)
app.secret_key = 'PythonCyberGuruIceServer'
conn = sqlite3.connect('simple.db')
con = sqlite3.connect('event.db')
s = conn.cursor()


def hash_string(s):
    return md5(s.encode()).hexdigest()


def check_login(user):  # User check function
    query = 'SELECT * FROM users WHERE login = "{}"'.format(user)
    s.execute(query)
    exist = s.fetchone()
    if exist is None:
        return False
    else:
        return True


def auth(login, password):  # Authorization check function
    query = 'SELECT * FROM users WHERE login ="()" and password ="{}"'.format(password)
    s.execute(query)
    result = s.fetchone()
    if result is None:
        return False
    else:
        return True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login', '')
        password = request.form.get('password', '')
        if login == '' or password == '':
            flash("Login or password is missing. Try Again")
            render_template('login.html')

        password = hash_string(password)
        query = 'SELECT * FROM users WHERE login = ? and password = ?'
        s.execute(query, [login, password])
        result = s.fetchone()
        if result is None:
            flash("User doesn't exist or password is incorrect. Try again")
        flash('You were successfully logged in')
        return render_template('storage.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        login = request.form.get('login', '')
        password = request.form.get('password', '')

        if login == '' or password == '':
            flash("Login or password is missing")
            render_template('register.html')

        if check_login(login):
            flash("This login already exist")
            render_template('register.html')
        password = hash_string(password)
        query = 'INSERT INTO users (login,password) VALUES ("{}","{}")'.format(login, password)
        s.execute(query)
        conn.commit()
        flash("Success")
        return render_template('login.html')


@app.route('/storage', methods=['GET', 'POST'])
def storage():
    if request.method == 'GET':
        return render_template('storage.html')

    else:
        event = request.form.get('Event', '')
        date = request.form.get('Date', '')

    if event == '' or date == '':
        flash('Event or Data is missing!')
        render_template('storage.html')

    if check_login(login):

        if auth(login, password):

            response = "Welcome, " + login + "! You have successfully introduced your idea!"

            insert_query = 'INSERT INTO events (login,event,date) VALUES ("{}","{}","{}")'.format(login, event, date)

            s.execute(insert_query)
            conn.commit()

            return render_template('storage.html', response=response)

        else:
            return "Wrong password! Turn back!"

    else:
        response = "Glad to see you , in our rows, " + login + '!\nYou have successfully introduced your idea!'

        insert_query = 'INSERT INTO users (login,password) VALUES ("{}","{}")'.format(login, password)
        s.execute(insert_query)

        insert_query = 'INSERT INTO events (login,event,date) VALUES ("{}","{}","{}")'.format(login, event, date)
        s.execute(insert_query)

        return render_template('storage.html', response=response)


if __name__ == '__main__':
    init_query = 'CREATE TABLE IF NOT EXISTS users' \
                 '(id integer NOT NULL PRIMARY KEY AUTOINCREMENT,' \
                 'login text,' \
                 'password text)'
    s.execute(init_query)

    init_query = 'CREATE TABLE IF NOT EXISTS events(id integer NOT NULL PRIMARY KEY AUTOINCREMENT, login text,event text,date text)'
    s.execute(init_query)

    s.execute(init_query)

    conn.commit()

app.run()
