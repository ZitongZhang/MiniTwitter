from flask import request, render_template, g, session, redirect, flash, url_for, abort

# Inevitable circular import
# See http://flask.pocoo.org/docs/0.10/patterns/packages/
from MiniTwitter import app


@app.route('/dm')  # display all users that you can chat with
def dm():
    if 'username' not in session:
        flash('Please sign in to send Direct Messages.')
        return redirect(url_for('signin'))
    userid = session['username'][0]

    cur = g.conn.execute('''SELECT username FROM users WHERE userid != %s''', userid)
    users = [user[0] for user in cur]

    categories = []
    cur = g.conn.execute('''SELECT categoryid, categoryname FROM categories''')
    c_rows = cur.fetchall()
    for c_row in c_rows:
        category = {'categoryname': c_row[1]}

        groups = []
        cur = g.conn.execute('''SELECT g.groupid, g.groupname
FROM groups g, group_belongs_to_category gc
WHERE g.groupid = gc.groupid AND gc.categoryid = %s''', c_row[0])
        g_rows = cur.fetchall()
        for g_row in g_rows:
            group = {'groupname': g_row[1]}
            cur = g.conn.execute('''SELECT u.username
FROM users u, user_member_of_group ug
WHERE u.userid != %s AND u.userid = ug.userid AND ug.groupid = %s''', (userid, g_row[0]))
            group['users'] = [user[0] for user in cur]
            groups.append(group)

        category['groups'] = groups
        categories.append(category)

    return render_template('dm.html', users=users, categories=categories)


@app.route('/dm/<path:username>')  # display chat
def chat(username):
    if 'username' not in session:
        flash('Please sign in to continue.')
        return redirect(url_for('signin'))
    senderid = session['username'][0]

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
ASC''', session['username'][0], receiverid, receiverid, session['username'][0])
    messages = []
    for row in cur:
        messages.append({'content': row[3],
                         'sending': row[0] == senderid,
                         'time': row[2].strftime('%Y-%m-%d %H:%M:%S')})
    return render_template('chat.html', messages=messages, receivername=username)


@app.route('/dm/<path:username>', methods=['POST'])  # update chat
def updatechat(username):
    if 'username' not in session:
        flash('Please sign in to continue.')
        return redirect(url_for('signin'))
    senderid = session['username'][0]

    cur = g.conn.execute('''SELECT u.userid
FROM users u
WHERE u.username = %s''', username)
    receiverid = cur.fetchone()
    if receiverid is None:
        return abort(404)
    receiverid = receiverid[0]

    message = request.form['message']
    try:
        g.conn.execute('''INSERT INTO dm (senderid, receiverid, content) VALUES (%s, %s, %s)''',
                       (senderid, receiverid, message))
    except:
        pass

    return redirect(url_for('chat', username=username))
