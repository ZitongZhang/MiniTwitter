from flask import Flask, request, render_template, g, session, redirect, flash, url_for
from secret import connection_string, secret_key
import sqlalchemy
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

import dm

engine = sqlalchemy.create_engine(connection_string)


@app.before_request
def before_request():
    try:
        g.conn = engine.connect()
    except:
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(_):
    try:
        g.conn.close()
    except:
        pass


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if 'username' in session:
        flash('You have already signed in as <b>{0}</b>.'.format(session['username'][1]))
        return redirect(url_for('home'))

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = g.conn.execute(
            'SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cur.fetchone()
        if user is None:
            error = 'Invalid username or password.'
        else:
            # session['username'] is a 2-tuple: (userid, username)
            session['username'] = (user[0], username)
            flash('Successfully signed in as <b>{0}</b>.'.format(username))
            return redirect(url_for('home'))
    return render_template('signin.html', error=error)


@app.route('/signout')
def signout():
    if 'username' in session:
        flash('You have successfully signed out.')
        session.pop('username')
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            g.conn.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            flash('Thank you for signing up! Please sign in using your username and password.')
            # clear the current login information
            session.pop('username')
            return redirect(url_for('signin'))
        except Exception as e:
            error = str(e)
    return render_template('signup.html', error=error)
