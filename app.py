from TemplateParser.helpers import camel_to_snake
from flask import Flask, request, send_from_directory, after_this_request
import generator
import os
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home_view():
        return json.dumps({'message': 'Welcome to Neutrino!'})

@app.route("/task", methods=["POST"])
def add_task():
  if request.get_json():
    data = request.get_json()
    job = generator.generator(data)
    print(job)
    if job == "Error":
        return "Failure, Try Again", 202
    dir_path = os.path.dirname(os.path.realpath(__file__))
    attachment = send_from_directory(dir_path, data["project_name"] + ".zip", as_attachment=True)

    print("mde it here mate")
    # os.remove(dir_path+"/" + camel_to_snake(data["project_name"])+".zip")
    print(dir_path+"/" + camel_to_snake(data["project_name"])+".zip")
    print(data["project_name"])

    @after_this_request
    def remove_file(response):
      try:
        os.remove(dir_path+"/" + camel_to_snake(data["project_name"])+".zip")
      except Exception as error:
        app.logger.error("Error removing or closing downloaded file handle", error)
      return response

    return attachment, 200
      
  return "Please pass a valid input",202

if __name__ == "__main__":
    app.run()

    
