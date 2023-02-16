import os
import logging
from dotenv import load_dotenv
from sys import stdout
from waitress import serve
from redis import Redis
from flask import Flask, jsonify
from flask_cors import CORS
from Config.init import load_config
from Config.redis_store import store
from Config.logger import logger


from API.routes import export_project, build_project_directory, compile_logic_code_preview, compile_project_warnings, \
    compile_page_preview, compile_single_logic_block_preview

load_dotenv()
ENV = os.getenv('ENV', 'prod')
config = load_config(ENV)

app = Flask(__name__)
CORS(app)
app.config.from_object(config)


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


@app.route('/test-redis')
def hello():
    store.incr('hits')
    return 'This route has been viewed %s time(s).' % store.get('hits')


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


if __name__ == "__main__":
    logger.info(f'This is a {"PRODUCTION" if config.ENV == "prod" else "DEVELOPMENT"} environment')
    logger.info(f"Listening on http://localhost:{config.FLASK_PORT}...")

    if ENV == 'prod':
        serve(app, host='0.0.0.0', port=config.FLASK_PORT)
    else:
        app.run(host='0.0.0.0', port=config.FLASK_PORT)
