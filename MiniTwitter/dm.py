from flask import request, render_template, g, session, redirect, flash, url_for, abort
# inevitable circular import
# see http://flask.pocoo.org/docs/0.10/patterns/packages/
from MiniTwitter import app



def display_users(rows):
    users = []
    for row in rows:
        user = {'user': row[1]}

        cur = g.conn.execute('''SELECT u.username
FROM users u''')

        users.append(user)
    return render_template('dm.html', users=users)



def display_chat(rows, receiverid):
    messages = {'content': [row[3] for row in rows],
        		'targetid': receiverid}
    for row in rows:
        cur = g.conn.execute('''SELECT d.content
FROM DM d''')
    return render_template('chat.html', messages=messages)

#cur = g.conn.execute('''SELECT u.username
#FROM users u
#WHERE u.userid = receiverid''', username)
 #   receiverid = cur.fetchone()


@app.route('/dm') #display all users that you can chat with
def dm():
    cur = g.conn.execute('''SELECT t.content, u.username, t.time, t.userid
FROM tweets t, users u
WHERE t.userid = u.userid
ORDER BY t.time
DESC''')
    rows = cur.fetchall() 
    return display_users(rows)



@app.route('/dm/<path:username>') #display chat 
def chat(username):
    cur = g.conn.execute('''SELECT u.userid
FROM users u
WHERE u.username = %s''', username)
    receiverid = cur.fetchone()
    if receiverid is None:
        return abort(404)
    receiverid = receiverid[0]
    cur = g.conn.execute('''SELECT d.senderid, d.receiverid, d.time, d.content
FROM DM d
WHERE d.senderid = %s AND d.receiverid = %s OR d.senderid = %s AND d.receiverid = %s
ORDER BY d.time
DESC''', session['username'][0], receiverid, receiverid, session['username'][0])
    rows = cur.fetchall()
    return display_chat(rows, receiverid)



@app.route('/dm/<path:username>', methods=['GET','POST']) #update chat 
def updatechat(username):
    error = None
    if request.method == 'POST' or 'GET':
    	senderid = session['username'][0]
        print senderid
    	cur = g.conn.execute('''SELECT u.userid
FROM users u
WHERE u.username = %s''', username)
    	receiverid = cur.fetchone()
        print receiverid
    	if receiverid is None:
            print 'chris'
    	    return abort(404)
    	receiverid = receiverid[0]
        message = request.form['message']
        try:
            g.conn.execute('INSERT INTO DM (senderid, receiverid, content) VALUES (%s, %s, %s)', (senderid, receiverid, message))
            flash('Sent.')
            return redirect(url_for('chat', username=username))
        except Exception as e:
            pass
