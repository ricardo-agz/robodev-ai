import imp
from shutil import rmtree
from TemplateParser.helpers import camel_to_snake
from flask import Flask, request, send_from_directory, after_this_request
import generator
import os
import json
from flask_cors import CORS
import glob

app = Flask(__name__)
CORS(app)

@app.route("/")
def home_view():
        return json.dumps({'message': 'Welcome to Neutrino!'})

@app.route("/task", methods=["POST"])
def add_task():
  # Clean up previous project zip files
  try:
    path = os.path.dirname(os.path.realpath(__file__))
    del_paths = glob.glob(os.path.join(path, 'neutrino_project*'))
    for del_path in del_paths:
        os.remove(del_path)
  except Exception as error:
    app.logger.error("Error removing or closing downloaded file handle", error)

  if request.get_json():
    data = request.get_json()
    job = generator.generator(data)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if job == "Error":
        return "Failure, Try Again", 202
    
    attachment = send_from_directory(dir_path,"neutrino_project_"+data["project_name"] + ".zip", as_attachment=True)
    return attachment, 200
      
  return "Please pass a valid input",202

if __name__ == "__main__":
    app.run()

    
