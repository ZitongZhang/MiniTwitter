from flask import request, render_template, g, session, redirect, flash, url_for
# inevitable circular import
# see http://flask.pocoo.org/docs/0.10/patterns/packages/
from MiniTwitter import app


@app.route('/dm')
def dm():
    return render_template('dm.html')
