import os
import time
import openai
from dotenv import load_dotenv
from rq import get_current_job

# from prompt_parser import PromptParser
from NeutrinoAI.logger import FileLogger
from NeutrinoAI.NeutrinoGPT.prompt_parser import PromptParser
from NeutrinoAI.NeutrinoGPT.response_parser import ModelsResponseParser, RelationsResponseParser, SchemaResponseParser, \
    relations_to_readable_string, ControllersResponseParser, format_schema_list_to_str, RoutesResponseParser

from generator.Config.logger import logger as flask_logger
from generator.Config.redis_store import get_redis_queue

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

APP_DESCRIPTION = """
Uber style ride sharing app but for truck owners to deliver shipments for clients
"""

logger = FileLogger()
q = get_redis_queue()

__location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))


def multi_logger(message, decor=False):
    """Logs the internal logger and the flask logger"""
    flask_logger.info(message)
    if decor:
        logger.log("====================")
    logger.log(message)
    if decor:
        logger.log("====================\n")


def status_tracker(status):
    """Sets the current status of the redis-queued job"""
    job_id = get_current_job().id
    job = q.fetch_job(job_id)

    # Set the initial status of the job
    job.meta['status'] = status
    job.save_meta()


def call_gpt_api(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=[" Human:", " AI:"]
    )

    return response


def mock_openai(filepath):
    """Simulates a call to OpenAI's API and returns the appropriate response from the specified filepath"""
    mock_reply_path = os.path.join(os.path.join(__location__, f"./mock_replies/{filepath}.txt"))
    with open(mock_reply_path, "r") as file:
        response = file.read()
    time.sleep(1)
    return response


def multiple_attempts(api_call, n=2):
    """
    Attempts to call the function multiple times if it fails the first time, stops after n attempts
    """
    for i in range(n):
        try:
            response = api_call()
            return response
        except Exception as e:
            if i == n - 1:
                raise ValueError(f"API call failed after {n} attempts: {e}")
            else:
                flask_logger.info(f"Failed to query API: {e}, trying again...")
    return None


class NeutrinoGPT:

    def __init__(self, app_description: str, mock: bool = False):
        self.app_description = app_description
        self.prompt_parser = PromptParser(app_description=app_description)
        self.mock = mock

    def generate_db_tables(self):
        multi_logger("Generating models...", decor=True)
        logger.log(self.prompt_parser.tables_prompt, "models_prompt.txt")
        status_tracker("Designing database schema...")

        if self.mock:
            response = mock_openai("db_reply")
        else:
            # automatically retry if call fails the first time
            response = multiple_attempts(lambda: call_gpt_api(self.prompt_parser.tables_prompt), n=3)

        db_tables_str = response.choices[0].text
        logger.log("Models Pre Parsed:")
        logger.log(db_tables_str)

        parser = ModelsResponseParser(db_tables_str)
        parsed_models, error = parser.parse_models()

        logger.log("Models Parsed:")
        logger.log(parsed_models)

        if error:
            logger.log(f"ERROR PARSING MODELS: {error}")

        logger.log("\n")
        return parsed_models

    def generate_relations(self, models: list[str]):
        multi_logger("Generating model relationships...", decor=True)
        status_tracker("Designing database relationships...")

        self.prompt_parser.parse_relations_prompt(models)
        logger.log(self.prompt_parser.relations_prompt, "relations_prompt.txt")

        if self.mock:
            response = mock_openai("relations_reply")
        else:
            # automatically retry if call fails the first time
            response = multiple_attempts(lambda: call_gpt_api(self.prompt_parser.relations_prompt), n=3)

        relations_str = response.choices[0].text
        logger.log("Relations Pre Parsed:")
        logger.log(relations_str)

        parser = RelationsResponseParser(relations_str)
        parsed, errors = parser.parse_relations()

        logger.log("Relations Parsed:")
        logger.log(parsed)

        if errors:
            logger.log("ERRORS PARSING RELATIONS:")
            for x in errors:
                logger.log(x)

        logger.log("\n")
        return parsed

    def generate_schema(
            self,
            models: list[str],
            relations: list[tuple[str, str, str, str, str, str]]
    ):
        multi_logger("Generating models' schema...", decor=True)
        status_tracker("Finalizing database schema...")

        rels_str = relations_to_readable_string(relations)
        self.prompt_parser.parse_schema_prompt(models, rels_str)

        logger.log(self.prompt_parser.schema_prompt, "schema_prompt.txt")

        if self.mock:
            response = mock_openai("schema_reply")
        else:
            # automatically retry if call fails the first time
            response = multiple_attempts(lambda: call_gpt_api(self.prompt_parser.schema_prompt), n=3)

        schema_str = response.choices[0].text
        logger.log("Schema Pre Parsed:")
        logger.log(schema_str)

        parser = SchemaResponseParser(schema_str)
        parsed, errors = parser.parse_schema()

        logger.log("Schema Parsed:")
        logger.log(parsed)

        if errors:
            logger.log("ERRORS PARSING SCHEMA:")
            for x in errors:
                logger.log(x)

        logger.log("\n")
        return parsed

    def generate_controllers(
            self,
            models: list[str],
            relations: list[tuple[str, str, str, str, str, str]]
    ):
        multi_logger("Generating controllers...", decor=True)
        status_tracker("Designing API controllers...")

        rels_str = relations_to_readable_string(relations)

        # remove joint tables so controllers for them don't get created
        models_no_joint = [x for x in models if "*" not in x]

        self.prompt_parser.parse_controllers_prompt(models_no_joint, rels_str)
        logger.log(self.prompt_parser.controllers_prompt, "controllers_prompt.txt")

        if self.mock:
            response = mock_openai("controllers_reply")
        else:
            # automatically retry if call fails the first time
            response = multiple_attempts(lambda: call_gpt_api(self.prompt_parser.controllers_prompt), n=3)

        controllers_str = response.choices[0].text
        logger.log("Controllers Pre Parsed:")
        logger.log(controllers_str)

        parser = ControllersResponseParser(controllers_str)
        parsed, errors = parser.parse_controllers()

        logger.log("Controllers Parsed:")
        logger.log(parsed)

        # remove controllers that were generated for joint tables in many-to-many relationships
        cleaned_output = []
        for controller in parsed:
            joint_table = False
            for model in models:
                if f"{controller.lower()}*" == model.lower():
                    joint_table = True
            if not joint_table:
                cleaned_output.append(controller)

        if errors:
            logger.log("ERRORS PARSING CONTROLLERS:")
            for x in errors:
                logger.log(x)

        logger.log("\n")
        return cleaned_output

    def generate_routes(
            self,
            models: list,
            schema: list,
            relations: list[tuple[str, str, str, str, str, str]],
            controllers: list[str]
    ):
        multi_logger("Generating API routes...", decor=True)
        status_tracker("Designing API routes...")

        models_str = ", ".join(models)
        rels_str = relations_to_readable_string(relations)
        schema_str = format_schema_list_to_str(schema)
        controllers_str = ", ".join(controllers)

        self.prompt_parser.parse_routes_prompt(models_str, schema_str, rels_str, controllers_str)
        logger.log(self.prompt_parser.routes_prompt, "routes_prompt.txt")

        if self.mock:
            response = mock_openai("routes_reply")
        else:
            # automatically retry if call fails the first time
            response = multiple_attempts(lambda: call_gpt_api(self.prompt_parser.routes_prompt), n=3)

        routes_str = response.choices[0].text
        logger.log("Routes Pre Parsed:")
        logger.log(routes_str)

        parser = RoutesResponseParser(routes_str)
        parsed, errors = parser.parse_routes()

        logger.log("Routes Parsed:")
        logger.log(parsed)

        if errors:
            logger.log("ERRORS PARSING ROUTES:")
            for x in errors:
                logger.log(x)

        logger.log("\n")
        return parsed

    def generate_route_logic(
            self,
            schema: list,
            method: str,
            url: str,
            description: str
    ):
        multi_logger(f"Generating route logic for {method.upper()} {url} {description}...", decor=False)
        status_tracker(f"Coding the logic for the following route: {method.upper()} {url} {description}...")

        schema_str = format_schema_list_to_str(schema)
        prompt = self.prompt_parser.route_logic_prompt

        api_str = f"{method.upper()} {url}"
        prompt = prompt.replace("$$SCHEMA$$", schema_str)
        prompt = prompt.replace("$$API_ROUTE$$", api_str)
        prompt = prompt.replace("$$ROUTE_DESCRIPTION$$", description)

        logger.log("ROUTE PROMPT:", "route_logic_prompt.txt")
        logger.log(f"{method.upper()} {url} {description}", "route_logic_prompt.txt")
        logger.log(self.prompt_parser.relations_prompt, "route_logic_prompt.txt")
        logger.log("\n\n--------------------\n\n", "route_logic_prompt.txt")

        if self.mock:
            response = mock_openai("route_logic_reply")
        else:
            # automatically retry if call fails the first time
            response = multiple_attempts(lambda: call_gpt_api(prompt), n=3)

        # here we don't need to parse, this will be handled by the gpt pseudocode compiler
        logic_str = response.choices[0].text
        logger.log(logic_str)

        return method, url, logic_str

    def generate_database_architecture(self):
        models = self.generate_db_tables()
        relations = self.generate_relations(models)
        schema = self.generate_schema(models, relations)
        controllers = self.generate_controllers(models, relations)
        routes = self.generate_routes(models, schema, relations, controllers)
        route_logic = []

        flask_logger.info("Generating route logic...")
        logger.log("====================")
        logger.log("Generating route logic...")
        logger.log("====================\n")
        for controller, route in routes:
            if len(route) > 1:
                method, url, handler, description = route
                method, url, logic_str = self.generate_route_logic(schema, method, url, description)
                route_logic.append((method, url, logic_str))

        logger.log("\n==========")
        logger.log(f"Models:\n{models}")
        logger.log(f"Relations:\n{relations}")
        logger.log(f"Schema:\n{schema}")
        logger.log(f"Controllers:\n{controllers}")
        logger.log(f"Routes:\n{routes}")
        for logic in route_logic:
            logger.log(f"{logic[0]} {logic[1]}\n{logic[2]}\n")
        logger.log("==========")

        return models, relations, schema, controllers, routes, route_logic


if __name__ == "__main__":
    schema_str = """
User:
username:string

Post:
title:string
content:string
    """

    parser = PromptParser("twitter-like blog app")
    parser.parse_route_logic_prompt(schema_str, "GET", "/users/:id", "get user with that id")
    # print(parser.route_logic_prompt)

    # generator = NeutrinoGPT(app_description=APP_DESCRIPTION)
    #
    # models_str, relations_str, schema_str = generator.generate_database_architecture()
    #
    # print("=====")
    # print(models_str)
    # print("-----")
    # print(relations_str)
    # print("-----")
    # print(schema_str)
    # print("=====")
    pass
