import os
import json
import urllib.request
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from .data_process.data_validate import DataValidate
from .artifactory_api.artifactory_get import GetArtifactory

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
    get_artifactory_api = GetArtifactory()
    uuaa_list = get_artifactory_api.get_uuaa()
    output = {"data":uuaa_list}
    response = jsonify(output)
    response = add_headers(response)
    return response

#get UUAA Tables for artifactory
@schema_end.route('/uuaa_tables/<uuaa>', methods=['GET'])
def get_table_uuaa(uuaa):
    get_artifactory_api = GetArtifactory()
    table_list = get_artifactory_api.get_table_uuaa(uuaa)
    output = {"tables":table_list}
    response = jsonify(output)
    response = add_headers(response)
    return response

@schema_end.route('/validate', methods=['POST'])
def validate():
    if 'data' not in request.files and 'schema' not in request.files:
        response = jsonify({'message' : 'data file or schema file part in the request'})
        response.status_code = 400
        response = add_headers(response)
        return response
    file_d = request.files['data']
    file_s = request.files['schema']
    if file_d.filename == '':
        response = jsonify({'message' : 'No file selected for uploading'})
        response.status_code = 400
        response = add_headers(response)
        return response
    if file_d and allowed_file(file_d.filename):
        filename_data = secure_filename(file_d.filename)
        filename_schema = secure_filename(file_s.filename)
        path_data = os.path.join("/Users/alfonsocaro/developer/code/validate_schema/files/data", filename_data)
        path_schema = os.path.join("/Users/alfonsocaro/developer/code/validate_schema/files/schema", filename_schema)
        file_d.save(path_data)
        file_s.save(path_schema)
        dv =  DataValidate()
        result, error_descrip, result_validate = dv.read_schema(path_data, path_schema) 
        response = jsonify({"result":result_validate, "example": result, "errors": f"{error_descrip}"})
        response.status_code = 200
        response = add_headers(response)
        return response
    else:
        response = jsonify({'message' : 'Allowed file types are txt, csv, json, schema'})
        response.status_code = 400
        response = add_headers(response)
        return response

@schema_end.route('/validateartifactory', methods=['POST'])
def validate_artifactory():
    uuaa = ""
    table_name = "" 
    table_env = ""

    try:
        print(request.form['vars'])
        vars_f = json.loads(request.form['vars'])
        uuaa = vars_f["uuaa"]
        table_name = vars_f["table"]
        table_env = vars_f["table_env"]
    except Exception as e:
        response = jsonify({'message' : 'vars not content in the request'})
        response.status_code = 400
        response = add_headers(response)
        return response

    if 'data' not in request.files in request.files:
        response = jsonify({'message' : 'data file part in the request'})
        response.status_code = 400
        response = add_headers(response)
        return response

    file_d = request.files['data']
    if file_d.filename == '':
        response = jsonify({'message' : 'No file selected for uploading'})
        response.status_code = 400
        response = add_headers(response)
        return response

    if file_d and allowed_file(file_d.filename):
        filename_data = secure_filename(file_d.filename)

        get_artifactory_api = GetArtifactory()
        filename_schema = get_artifactory_api.get_schema_table_uuaa(
            uuaa,
            table_name,
            table_env,
            "/Users/alfonsocaro/developer/code/validate_schema/files/schema"
        )
        path_data = os.path.join("/Users/alfonsocaro/developer/code/validate_schema/files/data", filename_data)
        path_schema = os.path.join("/Users/alfonsocaro/developer/code/validate_schema/files/schema", filename_schema)
        file_d.save(path_data)
        dv =  DataValidate()
        result, error_descrip, result_validate = dv.read_schema(path_data, path_schema) 
        response = jsonify({"result":result_validate, "example": result, "errors": f"{error_descrip}"})
        response.status_code = 200
        response = add_headers(response)
        return response

    else:
        response = jsonify({'message' : 'Allowed file types are txt, csv, json, schema'})
        response.status_code = 400
        response = add_headers(response)
        return response

def add_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response


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
