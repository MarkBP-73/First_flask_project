# Import the Flask class form the flask module
from flask import Flask, render_template, redirect,url_for, request, session,flash,g
from functools import wraps
import sqlite3



# create the application object based on Flask class
app= Flask(__name__)


# Add secret key required for using sessions, used as a key for session encryption. secret key is a variable of the Flask class
app.secret_key="my_secret_key"
# adds a variable to the app object which stores the database path.
app.database = "C:/sqlitedbs/disabilitysupport.db"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('You need to log in.')
            return redirect(url_for('login'))
    return wrap

def query_database(studyArea):
    g.db = connect_db()
    curs = g.db.execute('select Support_tool, Summary, Features.feature_id from Features inner join Supports_study on Features.feature_id=Supports_study.feature_id where Supports_study.Study_difficulty_id= "%s"' % studyArea)
    results = [dict(tool=row[0],summary=row[1],id=row[2]) for row in curs.fetchall()]
    g.db.close()
    return results


# use app.route decorator function to link path endpoint to a URL
@app.route('/')
@login_required
def home():
# Creates a connection to the database
#     g.db = connect_db()
#     cur = g.db.execute('select * from Study_area')
#     posts = [dict(index=row[0], area=row[1]) for row in cur.fetchall()]
#     g.db.close()
     return render_template('index.html')

#Creates a list of recommendations for research.
# Creates a connection to the database
@app.route('/research')
@login_required
def getresearch():
    posts = query_database('Research')
    return render_template('Main(Research).html', posts=posts)

@app.route('/writing')
@login_required
def getwriting():
# Creates a list of recommendations for writing.

    posts = query_database('Academic_writing')
    return render_template('Main(Writing).html', posts=posts)

@app.route('/notes')
@login_required
def getnotes():
# Creates a list of recommendations for research.
    posts = query_database('Note_taking')
    return render_template('Main(Notes).html', posts=posts)

@app.route('/selected')
@login_required
def showsummary():
    return render_template('summary.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html') #returns a template based on html

# create decorator to link URL endpoint to login page.
@app.route('/login', methods=['GET','POST'] ) #Adds the post method as well as get method to the decorator.
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials, please try again'
        else:
            session['logged_in'] = True
            flash("You were just logged in")
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash("You were just logged out")
    return redirect(url_for('welcome'))

def connect_db():
    return sqlite3.connect(app.database)

# start the server with the run() method
if __name__ =='__main__':
    app.run(debug=True)
