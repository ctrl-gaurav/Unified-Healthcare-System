from flask import Flask, render_template, url_for, redirect,request, session,flash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask import g
import os


#import yaml

app = Flask(__name__)
Bootstrap(app)

#conn = sqlite3.connect('database1.db')
#conn = sqlite3.connect('database1.sqlite')

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('database1.sqlite')
        #cursor = conn.execute("select * from users")
        #print(cursor)
    except sqlite3.error as e:
        print(e)
    return conn

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#conn = db_connection()
#curr = conn.cursor()
#curr = conn.execute("select * from users")
#curr.execute("INSERT INTO users(username) VALUES ('hello')")
#conn.commit()

@app.route("/")
def index():
    return render_template('index.html')
    session.pop('user', None)
    #return redirect(url_for('about'))

@app.route("/sqllite")
def sqllite():
    cur = get_db().cursor()
    return '<h1> hello </h1>'

app.secret_key = os.urandom(24)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.pop('user',None)

        userDetails = request.form
        username = userDetails['email']

        conn = db_connection()
        curr = conn.cursor()
        resultvalue = curr.execute("SELECT * FROM users WHERE username = ?", ([username]))
        if resultvalue is None:
            user = curr.fetchone()
            print(user[2])
            if userDetails['password'] == user[2]:
                session['user'] = str(request.form['email'])
                return redirect(url_for('protected'))
        else:
            curr.close()
            flash('User not found', 'danger')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/protected')
def protected():
    if g.user:
        return render_template('dashboard.html',user=session['user'])
    return redirect(url_for('login'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/loginDoc')
def loginDoc():
    return render_template('loginDoc.html')

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userDetails = request.form
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match! Try again.', 'danger')
            return render_template('register.html')
        conn = db_connection()
        curr = conn.cursor()
        curr.execute("insert into users(id, location,name ,username , passsword )" "VALUES(?,?,?,?,?)", ("1", userDetails['location'],userDetails['first_name'], userDetails['email'], userDetails['password']))
        conn.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')





@app.route("/about")
def about():
    return "<p>Hello, World!</p>"

@app.route("/add")
def add():
    if g.user:
        return render_template('add.html')

    return redirect(url_for('login'))

@app.route("/uploadP")
def uploadP():
    if g.user:
        return render_template('uploadP.html')

    return redirect(url_for('login'))


if  __name__ == '__main__':
    app.run(debug = True, port = 5001)