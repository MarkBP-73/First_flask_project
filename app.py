# Import the Flask class form the flask module
from flask import Flask, render_template

# create the application object based on Flask class
app= Flask(__name__)

# use decorators to link the function to a URL
@app.route('/')
def home():
      return "Hello, World!" # returns the string Hello World

@app.route('/welcome')
def welcome():
    return render_template('welcome.html') #returns a template based on html

# start the server with the run() method
if __name__ =='__main__':
    app.run(debug=True)
