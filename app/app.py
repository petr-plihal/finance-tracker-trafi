from flask import Flask

# For working with Jinja2/basic html files from /templates folder
from flask import render_template

# For accessing data sent by the user
from flask import request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/load_csv")
def load_csv():
    return render_template("load.html")