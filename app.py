from waitress import serve
from flask import Flask, jsonify
import os
from flask_cors import CORS

from page_builder import build_controller_page, build_db_page, build_middlewares_page, build_model_page, build_routes_page, build_server_page, build_media_config_page
from Config.init import load_config

from API.routes import export_project, build_project_directory, compile_logic_code_preview, compile_project_warnings, \
    compile_page_preview, compile_single_logic_block_preview

ENV = os.environ.get('ENV') or "dev"
config = load_config(ENV)

app = Flask(__name__)
CORS(app)
app.config.from_object(config)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def home_view():
    res = jsonify({'message': 'Welcome to Neutrino!'})
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res, 200


@app.route("/test")
def test_view():
    res = jsonify({'message': 'This is a test route. Not much to see here... [edit-2]'})
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res, 200


@app.route("/previewpage", methods=["PUT"])
def preview_page():
    res, status = compile_page_preview()
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res, status


@app.route("/getwarnings", methods=["PUT"])
def get_warnings():
    res, status = compile_project_warnings()
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res, status


@app.route("/logiccodepreview", methods=["POST"])
def get_logic_code_preview():
    res, status = compile_logic_code_preview()
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res, status


@app.route("/compilelogicblock", methods=["POST"])
def compile_logic_block_preview():
    res, status = compile_single_logic_block_preview()
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res, status


@app.route("/builddirectory", methods=["PUT"])
def build_directory():
    res, status = build_project_directory()
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res, status


@app.route("/generator", methods=["POST"])
def add_task():
    res, status = export_project(app)
    res.headers.add('Access-Control-Allow-Origin', '*')
    return res, status

# TODO: figure out media config route.

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f'This is a {"PRODUCTION" if ENV == "prod" else "DEVELOPMENT"} environment')
    print(f"Listening on http://127.0.0.1:{port}...")

    if ENV == 'prod':
        serve(app, host='0.0.0.0', port=port)
    else:
        app.run(host='0.0.0.0', port=port)
