import os
import urllib.request
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from .data_process.data_validate import DataValidate

# define the blueprint
schema_end = Blueprint(name="schemas_end", import_name=__name__)

# note: global variables can be accessed from view functions
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'json', 'schema'])
x = 100

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# add view function to the blueprint
@schema_end.route('/test', methods=['GET'])
def test():
    output = {"msg": "I'm the test endpoint from schema_end."}
    return jsonify(output)

#get UUAA's name for artifactory
@schema_end.route('/uuaa', methods=['GET'])
def get_uuaa():
    output = {"UUAA's":["BIAC", "BIDA", "BIFI", "..."]}
    return jsonify(output)

@schema_end.route('/validate', methods=['POST'])
def validate():
    if 'data' not in request.files and 'schema' not in request.files:
        resp = jsonify({'message' : 'data file or schema file part in the request'})
        resp.status_code = 400
        return resp
    file_d = request.files['data']
    file_s = request.files['schema']
    if file_d.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file_d and allowed_file(file_d.filename):
        filename_data = secure_filename(file_d.filename)
        filename_schema = secure_filename(file_s.filename)
        path_data = os.path.join("/Users/alfonsocaro/developer/code/col_validate_data_schema/files/data", filename_data)
        path_schema = os.path.join("/Users/alfonsocaro/developer/code/col_validate_data_schema/files/schema", filename_schema)
        file_d.save(path_data)
        file_s.save(path_schema)
        dv =  DataValidate()
        result, error_descrip, result_validate = dv.read_schema(path_data, path_schema) 
        resp = jsonify({"result":result_validate, "example": f"{result}", "errors": f"{error_descrip}"})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, csv, json, schema'})
        resp.status_code = 400
        return resp


# add view function to the blueprint
@schema_end.route('/plus', methods=['POST'])
def plus_x():
    # retrieve body data from input JSON
    data = request.get_json()
    in_val = data['number']
    # compute result and output as JSON
    result = in_val + x
    output = {"msg": f"tu numero es '{in_val}' y el resultado es: '{result}'"}
    return jsonify(output)