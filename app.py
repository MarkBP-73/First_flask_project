# Import the Flask class form the flask module
from flask import Flask, render_template, redirect,url_for,request

# create the application object based on Flask class
app= Flask(__name__)

# use decorators to link the function to a URL
@app.route('/')
def home():
      return "Hello, World!" # returns the string Hello World

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
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


# start the server with the run() method
if __name__ =='__main__':
    app.run(debug=True)
