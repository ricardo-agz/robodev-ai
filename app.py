import imp
from shutil import rmtree
from TemplateParser.helpers import camel_to_snake
from flask import Flask, request, send_from_directory, after_this_request, jsonify
import generator
import os
import json
from flask_cors import CORS
import glob

from Logic.interact import json_to_formatted_code

from page_builder import build_client_app_page, build_client_auth_context, build_client_home_page, build_client_login, build_client_navbar, build_client_private_route, build_client_show_all, build_client_show_edit, build_client_show_new, build_client_show_one, build_client_use_api, build_client_use_auth, build_client_use_find, build_controller_page, build_db_page, build_middlewares_page, build_model_page, build_routes_page, build_server_page

app = Flask(__name__)
CORS(app)

@app.route("/")
def home_view():
        return json.dumps({'message': 'Welcome to Neutrino!'})


"""
Returns a string of the specified page
"""
@app.route("/previewpage", methods=["PUT"])
def preview_page():
  if request.get_json():
    # here we want to get the page and model from quey string (i.e. ?page=server_index)
    page = request.args.get('page')
    model_name = request.args.get('model')

    data = request.get_json()
    try:
      project = generator.project_from_builder_data(data)
    except Exception as e:
      return jsonify({"message": f"Error building project: {e}"}), 400

    model = project.model_from_name(model_name)
    page_output = ""

    no_model_required = ["server_index", "database", "middlewares", "routes"]
    if not page or page == "":
      return jsonify({"message": "No page passed"}), 400
    # if page not in no_model_required and (not model_name or model_name == ""):
    #   return jsonify({"message": "Model input required"}), 400


    if page == "server_index":
      page_output = build_server_page(project)
    elif page == "database":
      page_output = build_db_page(project)
    elif page == "routes":
      page_output = build_routes_page(project)
    elif page == "middlewares":
      page_output = build_middlewares_page(project)
    elif page == "client_app":
      page_output = build_client_app_page(project)
    elif page == "client_home":
      page_output = build_client_home_page(project)
    elif page == "navbar":
      page_output = build_client_navbar(project)
    elif page == "login_page":
      page_output = build_client_login(project)
    elif page == "private_route":
      page_output = build_client_private_route(project)
    elif page == "use_api":
      page_output = build_client_use_api(project)
    elif page == "use_auth":
      page_output = build_client_use_auth(project)
    elif page == "use_find":
      page_output = build_client_use_find(project)
    elif page == "auth_context":
      page_output = build_client_auth_context(project)
    elif "_" in page:
      temp = page.split("_")
      model_name = temp[0]
      model = project.model_from_name(model_name)

      
        # SERVER
      if "controller" in page:

        temp_controller = None
        check_string= page.replace("_controller", "")
        for controller in project.controllers:
          if  check_string == controller.name:
            temp_controller = controller
        page_output = build_controller_page(project, temp_controller)

      elif "model" in page:
        print("+++++++++++++++++++++")
        print(model)
        print(project)
        print("+++++++++++++++++++++")

        page_output = build_model_page(project, model)

      # CLIENT
      elif "indexpage" in page:
        page_output = build_client_show_all(project, model)
      elif "showpage" in page:
        page_output = build_client_show_one(project, model)
      elif "updatepage" in page:
        page_output = build_client_show_edit(project, model)
      elif "createpage" in page:
        page_output = build_client_show_new(project, model)
      else:
        return jsonify({"message": "Invalid page"}), 400
      

    return jsonify({"content": page_output})
      
  return jsonify({"message": "Please pass a valid input"}), 400



"""
Gets a list of warnings and errors that may or may not cause build to fail
"""
@app.route("/getwarnings", methods=["PUT"])
def get_warnings():
  if request.get_json():
    data = request.get_json()
    project = generator.project_from_builder_data(data)
    return jsonify({"warnings": project.warnings})
      
  return jsonify({"message": "Please pass a valid input"}), 400


"""
Gets formatted code returned given json
"""
@app.route("/logiccodepreview", methods=["POST"])
def get_logic_code_preview():
  if request.get_json():
    data = request.get_json()
    print(data);
    code_generated = json_to_formatted_code(data["logic"])
    return jsonify({"code": code_generated})
      
  return jsonify({"message": "Please pass a valid input"}), 400


"""
Returns a json representation of the project directory structure
"""
@app.route("/builddirectory", methods=["PUT"])
def build_directory():
  if request.get_json():
    data = request.get_json()
    # try:
    project = generator.project_from_builder_data(data)
    return jsonify(project.build_directory())
    # except Exception as e:
      # return jsonify({"message": f"Build failed, compile project to view warnings: {e}"}), 500
      
  return jsonify({"message": "Please pass a valid input"}), 400


"""
Gets a list of the one-to-many and many-to-many relationships for each model
"""
@app.route("/getrelations", methods=["PUT"])
def parse_relations():
  if request.get_json():
    data = request.get_json()
    project = generator.project_from_builder_data(data)
    output = {}

    for model in project.models:
      many_to_many = []
      one_to_many = []
      for many_model, alias in model.many_to_many:
        many_to_many.append([many_model.name, alias])
      for many_model, alias in model.one_to_many:
        one_to_many.append([many_model.name, alias])
      output[model.name] = {"many_to_many": many_to_many, "one_to_many": one_to_many}

    return jsonify(output), 200
      
  return jsonify({"message": "Please pass a valid input"}), 400


"""
Main Generator function, creates project and returns zip file
"""
@app.route("/generator", methods=["POST"])
def add_task():
  # Clean up previous project zip files
  try:
    path = os.path.dirname(os.path.realpath(__file__))
    del_paths = glob.glob(os.path.join(path, 'neutrino_project*'))
    for del_path in del_paths:
      os.remove(del_path)
  except Exception as error:
    print("Error removing or closing downloaded file handle")
    app.logger.error("Error removing or closing downloaded file handle", error)

  # CONTAINS JSON INPUT FOR PROJECT STRUCTURE
  if request.get_json():
    data = request.get_json()
    try:
      # DON'T CREATE PROJECT FOLDER IF BUILD WILL FAIL (only catches known errors)
      project = generator.project_from_builder_data(data)
      if project.contains_fatal_errors():
        print(project.contains_fatal_errors())
        return jsonify({
          "message": "Project contains errors, build will fail",
          "errors": project.contains_fatal_errors()
        }), 400

      build = generator.generator(data)
    
    # PROTECTION AGAINST UNEXPECTED ERRORS
    except Exception as error:
     print(error)
     return jsonify({"message": "Project build failed unexpectedly"}), 400

    dir_path = os.path.dirname(os.path.realpath(__file__))
    attachment = send_from_directory(dir_path,"neutrino_project_" + data["project_name"] + ".zip", as_attachment=True)

    return attachment, 200
      
  return jsonify({"message": "Please pass a valid input"}), 400




if __name__ == "__main__":
    app.run(host='127.0.0.1', threaded=True)

    
