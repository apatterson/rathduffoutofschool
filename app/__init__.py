from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('hello.html')

@app.route("/pay")
def pay():
    return render_template('pay.html)')

