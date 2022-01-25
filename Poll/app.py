"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
app = Flask(__name__)
app.config['SECRET_KEY'] = 'poll_key'

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM User').fetchall()
    average_rating = conn.execute('SELECT AVG(Rating) FROM User').fetchone()[0]
    num_of_ratings = conn.execute('SELECT COUNT(Rating) FROM User').fetchone()[0]
    conn.close()
    return render_template('index.html', rows = rows, average_rating = average_rating, num_of_ratings = num_of_ratings)

@app.route('/create/', methods=('GET', 'POST'))
def create():

    if request.method == 'POST':
        name = request.form['Name']
        age = request.form['Age']
        rating = request.form['Rating']

        if not name:
            flash('You must write your name.')
        elif not age:
            flash('You must write your age.')
        elif not rating:
            flash('You must write your rating.')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO User (Name, Age, Rating) VALUES (?, ?, ?)',
                         (name, age, rating))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
