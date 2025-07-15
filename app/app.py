from flask import Flask
from flask import render_template # Working with Jinja2/basic html files from /templates folder
from flask import request # For accessing data sent to the app

from models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://admin-dev:password123@database:3306/trafi-dev"

db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/load_csv")
def load_csv():
    return render_template("load.html")