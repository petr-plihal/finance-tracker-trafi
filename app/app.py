from flask import Flask
from flask import render_template # Working with Jinja2/basic html files from /templates folder

####################
###### CONFIG ######
####################

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://admin-dev:password123@database:3306/trafi-dev"

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
    uploads_list: list = os.listdir("uploads")
    return render_template("uploads.html", uploads_list=uploads_list)

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


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