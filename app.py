import os
import json
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv
from waitress import serve
from rq.job import Job
from flask import Flask, jsonify, request
from flask_cors import CORS
from Config.init import load_config
from Config.redis_store import store, get_redis_conn, get_redis_queue
from Config.logger import logger
from tasks import get_buildfile_neutrinoai, sleep

from API.routes import export_project, build_project_directory, compile_logic_code_preview, compile_project_warnings, \
    compile_page_preview, compile_single_logic_block_preview

load_dotenv()
ENV = os.getenv('ENV', 'dev')
config = load_config(ENV)

app = Flask(__name__)
CORS(app)
app.config.from_object(config)

q = get_redis_queue()


@app.route('/enqueue-ai-task', methods=["POST"])
def enqueue_task():
    description = request.json.get('description', None)  # Get the description from the request body
    user_id = request.json.get('user', None)  # Get the user id from the request body

    # error check
    if description is None:
        return jsonify({'message': 'Error: description is missing from the request JSON'}), 400
    if user_id is None:
        return jsonify({'message': 'Error: auth error, no user passed, please log out and log back in'}), 400

    # enqueue task
    job = q.enqueue(get_buildfile_neutrinoai, description)  # Enqueue the task
    # job = q.enqueue(sleep, 5)  # for testing

    # log analytics
    try:
        url = f"{config.NEUTRINO_IDENTITY_URL}/analytics/ai-project-reports"
        logger.info(url)
        data = json.dumps({
            'user': user_id,
            'prompt': description,
            'job_id': job.id,
            'started': str(datetime.today().date())
        })
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            data=data)
        logger.info(f"Request status code: {response.status_code}")
        logger.info(f"Request content: {response.content}")
    except Exception as e:
        logger.info(f"failed to create ai report: {e}")

    return jsonify({'message': 'Task enqueued', 'job_id': job.id})


@app.route('/check-ai-task/<string:job_id>')
def check_task(job_id):
    job = q.fetch_job(job_id)  # Get the job object by ID
    if job is None:
        return jsonify({'message': f'Job {job_id} not found'}), 404
    elif job.is_finished:
        buildfile = json.loads(job.result)
        # buildfile = job.result  # for testing

        # log analytics
        try:
            url = f"{config.NEUTRINO_IDENTITY_URL}/analytics/ai-project-reports/complete"
            logger.info(url)
            data = json.dumps({
                'job_id': job.id,
                'buildfile': json.dumps(buildfile),
                'failed': job.is_failed,
                'logs': None,
                'completed': str(datetime.today().date())
            })
            response = requests.put(
                url,
                headers={'Content-Type': 'application/json'},
                data=data)
            logger.info(f"Request status code: {response.status_code}")
            logger.info(f"Request content: {response.content}")
        except Exception as e:
            logger.info(f"failed to complete ai report: {e}")

        return jsonify({'buildfile': buildfile, 'message': 'successfully created project'}), 200
    else:
        # Get the current status of the job
        status = job.meta.get('status', 'working on your app...')
        # Return the status as a JSON response
        return jsonify({'message': status}), 202


@app.route('/jobs')
def list_jobs():
    job_ids = q.job_ids  # Get a list of all job IDs in the default queue
    jobs = [Job.fetch(id, connection=get_redis_conn()) for id in job_ids]  # Fetch the job objects
    job_data = [{'id': job.id, 'status': job.get_status()} for job in jobs]  # Get the ID and status of each job
    return jsonify(job_data)


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
    # getting logs to show up on heroku
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    logger.info(f'This is a {"PRODUCTION" if config.ENV == "prod" else "DEVELOPMENT"} environment')
    logger.info(f"Listening on http://localhost:{config.FLASK_PORT}...")
    logger.info(f"Connected to Neutrino Identity Server at {config.NEUTRINO_IDENTITY_URL}...")

    if ENV == 'prod':
        serve(app, host='0.0.0.0', port=config.FLASK_PORT)
    else:
        app.run(host='0.0.0.0', port=config.FLASK_PORT)
