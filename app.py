# Import the Flask class form the flask module
from flask import Flask, render_template, redirect,url_for, request, session,flash
from functools import wraps

# create the application object based on Flask class
app= Flask(__name__)

# Add secret key required for using sessions, used as a key for session encryption. secret key is a variable of the Flask class
app.secret_key="my_secret_key"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('You need to log in.')
            return redirect(url_for('login'))
    return wrap

# use app.route decorator function to link path endpoint to a URL
@app.route('/')
@login_required
def home():
     # return "Hello, World!" # returns the string Hello World
      return render_template('index.html')

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


# start the server with the run() method
if __name__ =='__main__':
    app.run(debug=True)
