from flask import Flask
from flask import render_template # Working with Jinja2/basic html files from /templates folder
from flask import redirect # To avoid request re-submissions and allow clean history after POST requests
from flask import url_for # Decoupling the internal function name from the external URL path

####################
###### CONFIG ######
####################

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://admin-dev:password123@database:3306/trafi-dev"

app.config["SELECTED_FILENAME"] = "" # TODO: Very bad, this means all users share the same file (after the first user defines this variable) ew

####################
##### MAIN PAGE ####
####################

@app.route("/")
def home():
    return render_template("index.html")

####################
### FILE UPLOADS ###
####################

# For accessing data sent to the app
import os
from flask import request, send_from_directory
from werkzeug.utils import secure_filename

if not os.path.exists("uploads"): os.makedirs("uploads")
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "csv"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # Max size of uploaded files is 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/load_csv", methods=["POST", "GET"])
def load_csv():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'bank-statement-csv' not in request.files:
            print("No file part")
        file = request.files['bank-statement-csv']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            print('No selected file')
        
        # If the file has valid name and extension server saves it in dedicated folder for later use
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template("load.html")

@app.route("/uploads", methods=["GET"])
def uploads():
    uploads_list: list = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("uploads.html", uploads_list=uploads_list)

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

####################
# SELECT INPUT DATA
####################

import pandas as pd
app.config['ANALYSIS_DATAFRAME'] = None

from app.scripts.loading.csv_loader import CSVLoader

@app.route("/select_input", methods=["GET", "POST"])
def select_input():
    if request.method == "GET":
        uploads_list: list = os.listdir(app.config["UPLOAD_FOLDER"])
        return render_template("select_input.html", uploads_list=uploads_list, selected_filename=app.config["SELECTED_FILENAME"])
    if request.method == "POST":
        selected_filename = request.form.get('filename')
        
        if selected_filename:
            # NOTE: A session might be used instead
            app.config["SELECTED_FILENAME"] = selected_filename
            # NOTE: There should be a) validate file exists, b) logger
            print(f"User selected: {selected_filename} file as an input")

            app.config['ANALYSIS_DATAFRAME'] = CSVLoader(app.config["UPLOAD_FOLDER"]+"/"+app.config["SELECTED_FILENAME"]).get_dataframe()
        
        return redirect(url_for('select_input'))

####################
######## API #######
####################
from flask import abort, jsonify

@app.route("/api/records", methods=["GET"])
def get_records():
    # Get arguments from URL
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 100))
    except ValueError:
        abort(400, description="Page and size must be valid integers.")

    if page < 1 or size < 1: 
        abort(400, description="Size and page arguments for record request endpoint cannot be less than 1.")

    # Load data from dataframe into dictionary and convert to json
    app_dataframe = app.config['ANALYSIS_DATAFRAME']
    selected_rows: pd.DataFrame = pd.DataFrame()
    if app_dataframe is not None:
        app_dataframe: pd.DataFrame
        start_index = (page - 1) * size + 1
        end_index = page * size
        selected_rows = app_dataframe.iloc[start_index:end_index]
    else:
        abort(400, description="No source file data present, to use this endpoint you must select source data.")

    json_data = selected_rows.to_json(orient='records')

    # Get metadata
    # TODO: This should be done when getting the arguments, to avoid accessing index not present in dataframe
    total_rows = len(app_dataframe)
    total_pages = int(total_rows / size) + int(total_rows % size > 0)

    # TODO: Build HATEOAS links
    links = {}

    response_data = {
        "data": json_data,
        "metadata": {
            "page": page,
            "size": size,
            "total_rows": total_rows,
            "total_pages": total_pages
        },
        "links": links
    }

    return jsonify(response_data)

####################
#### CALCULATORS ###
####################

from app.scripts.calculators.employment_type_comparison.calculator import Comparer 
from app.models.salary import NetSalaryInfo, ComparedEmploymentTypes

@app.route('/calculators/employment_type_comparison', methods=["GET", "POST"])
def employment_type_comparison():
    result = None

    # Only trigger calculation if form is submitted, not even when it gets loaded without posting
    if request.method == "POST":

        salary_gross_employee = request.values.get("salary_gross_employee")
        salary_gross_self_employed = request.values.get("salary_gross_self_employed")

        # TODO: These type of things could be logged? Figure out if it would be useful. Not necessarily for the type, but input values and result might be good to know.
        # print(f"salary_gross_self_employed is '{salary_gross_self_employed}' of type {type(salary_gross_self_employed)}")

        result = Comparer.compare(float(salary_gross_employee), float(salary_gross_self_employed))

    return render_template("calculators/employment_type_comparison/index.html", result=result)