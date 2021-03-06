from flask import Flask, request, render_template, g, session, redirect, flash, url_for, jsonify
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


def display_tweets(rows):
    tweets = []
    for row in rows:
        # Each tweet gets its unique id, which is a combination of time and userid
        # The id will be used to associate button with tweet
        tweet = {'content': row[0],
                 'username': row[1],
                 'time': row[2].strftime('%Y-%m-%d %H:%M:%S'),
                 'id': row[2].strftime('%Y-%m-%d %H:%M:%S.%f') + ',' + str(row[3])}

        cur = g.conn.execute('''SELECT u.username
FROM user_likes_tweet ut, users u
WHERE ut.t_time = %s AND ut.t_userid = %s AND ut.userid = u.userid''', (row[2], row[3]))
        tweet['likes'] = [like[0] for like in cur]  # username of users who like this tweet

        cur = g.conn.execute('''SELECT t.tagname
FROM tweet_mentions_tag tt, tags t
WHERE tt.t_time = %s AND tt.t_userid = %s AND tt.tagid = t.tagid''', (row[2], row[3]))
        tweet['tags'] = [tag[0] for tag in cur]

        cur = g.conn.execute('''SELECT c.content, u.username, c.time
FROM comments c, users u
WHERE c.t_time = %s AND c.t_userid = %s AND c.userid = u.userid''', (row[2], row[3]))
        tweet['comments'] = [{'content': comment[0],
                              'username': comment[1],
                              'time': comment[2].strftime('%Y-%m-%d %H:%M:%S')} for comment in cur]
        tweets.append(tweet)
    return render_template('home.html', tweets=tweets)


@app.route('/')
def home():
    cur = g.conn.execute('''SELECT t.content, u.username, t.time, t.userid
FROM tweets t, users u
WHERE t.userid = u.userid
ORDER BY t.time
DESC''')
    rows = cur.fetchall()  # assuming there aren't too many tweets for now
    return display_tweets(rows)


# We didn't check for slashes in the username, so we have to allow them here
@app.route('/user/<path:username>')
def user(username):
    cur = g.conn.execute('''SELECT t.content, u.username, t.time, t.userid
FROM tweets t, users u
WHERE t.userid = u.userid AND u.username = %s
ORDER BY t.time
DESC''', username)
    rows = cur.fetchall()
    return display_tweets(rows)


@app.route('/tag/<path:tagname>')
def tag(tagname):
    cur = g.conn.execute('''SELECT t.content, u.username, t.time, t.userid
FROM tweets t, users u, tweet_mentions_tag tt, tags
WHERE t.userid = u.userid AND t.userid = tt.t_userid AND t.time = tt.t_time
AND tt.tagid = tags.tagid AND tags.tagname = %s
ORDER BY t.time
DESC''', tagname)
    rows = cur.fetchall()
    return display_tweets(rows)


@app.route('/_like')
def _like():
    try:
        if 'username' not in session:
            return redirect(url_for('signin'))  # not logged in
        userid = session['username'][0]

        # Example t_id: '2016-11-11 01:14:07.000000+2'
        t_id = request.args.get('t_id')
        liking = request.args.get('liking') == 'true'

        t_time, t_userid = t_id[:26], t_id[27:]
        cur = g.conn.execute('''SELECT *
FROM user_likes_tweet
WHERE userid = %s AND t_userid = %s AND t_time = %s''', (userid, t_userid, t_time))
        # Whether already liked
        liked = cur.fetchone() is not None

        if liking and not liked:
            g.conn.execute('''INSERT INTO user_likes_tweet (userid, t_userid, t_time)
VALUES (%s, %s, %s)''', (userid, t_userid, t_time))

        if not liking and liked:
            g.conn.execute('''DELETE FROM user_likes_tweet
WHERE userid = %s AND t_userid = %s AND t_time = %s''', (userid, t_userid, t_time))

        return jsonify(liked=liking)
    except:
        pass


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if 'username' in session:
        flash('You have already signed in as <b>{0}</b>.'.format(session['username'][1]))
        return redirect(url_for('home'))

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = g.conn.execute('''SELECT userid FROM users WHERE username = %s AND password = %s''',
                             (username, password))
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
            g.conn.execute('''INSERT INTO users (username, password) VALUES (%s, %s)''', (username, password))
            flash('Thank you for signing up! Please sign in using your username and password.')
            # clear the current login information
            session.pop('username', None)
            return redirect(url_for('signin'))
        except Exception as e:
            error = str(e)
    return render_template('signup.html', error=error)
