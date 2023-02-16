import os

DB_PROMPT_ACTION = \
    """What database tables would be required?"""

RELATION_PROMPT_ACTION = \
    """What would the database relationships be (if any)?"""

SCHEMA_PROMPT_ACTION = \
    """Help me come up with the database schema for a given app description."""

CONTROLLERS_PROMPT_ACTION = \
    """Which controllers would be required to implement this app in a generic MVC framework?"""

ROUTES_PROMPT_ACTION = \
    """For each controller, which API routes would be required to implement the app functionality?"""

ROUTE_LOGIC_PROMPT_ACTION = \
    """Implement the route logic in pseudocode, perform error checking when necessary"""


class PromptParser:
    """
    Used for parsing the prompts for the GPT calls
    """

    def __init__(self, app_description: str) -> None:
        self.tables_prompt = None
        self.schema_prompt = None
        self.relations_prompt = None
        self.controllers_prompt = None
        self.routes_prompt = None
        self.route_logic_prompt = None
        self.load_prompts(app_description)

    def load_prompts(self, app_description: str) -> None:
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        # path = open(os.path.join(__location__, in_file), "r")

        tables_file_path = os.path.join(os.path.join(__location__, "./prompts/db_prompt.txt"))
        relations_file_path = os.path.join(os.path.join(__location__, "./prompts/relations_prompt.txt"))
        schema_file_path = os.path.join(os.path.join(__location__, "./prompts/schema_prompt.txt"))
        controllers_file_path = os.path.join(os.path.join(__location__, "./prompts/controllers_prompt.txt"))
        routes_file_path = os.path.join(os.path.join(__location__, "./prompts/routes_prompt.txt"))
        route_logic_file_path = os.path.join(os.path.join(__location__, "./prompts/route_logic_prompt.txt"))

        with open(tables_file_path, "r") as file:
            tables_prompt = file.read()
            tables_prompt = tables_prompt.replace("$$ACTION$$", DB_PROMPT_ACTION)
            tables_prompt = tables_prompt.replace("$$APP_DESCRIPTION$$", app_description)
        with open(relations_file_path, "r") as file:
            relations_prompt = file.read()
            relations_prompt = relations_prompt.replace("$$ACTION$$", RELATION_PROMPT_ACTION)
            relations_prompt = relations_prompt.replace("$$APP_DESCRIPTION$$", app_description)
        with open(schema_file_path, "r") as file:
            schema_prompt = file.read()
            schema_prompt = schema_prompt.replace("$$ACTION$$", SCHEMA_PROMPT_ACTION)
            schema_prompt = schema_prompt.replace("$$APP_DESCRIPTION$$", app_description)
        with open(controllers_file_path, "r") as file:
            controllers_prompt = file.read()
            controllers_prompt = controllers_prompt.replace("$$ACTION$$", CONTROLLERS_PROMPT_ACTION)
            controllers_prompt = controllers_prompt.replace("$$APP_DESCRIPTION$$", app_description)
        with open(routes_file_path, "r") as file:
            routes_prompt = file.read()
            routes_prompt = routes_prompt.replace("$$ACTION$$", ROUTES_PROMPT_ACTION)
            routes_prompt = routes_prompt.replace("$$APP_DESCRIPTION$$", app_description)
        with open(route_logic_file_path, "r") as file:
            route_logic_prompt = file.read()
            route_logic_prompt = route_logic_prompt.replace("$$ACTION$$", ROUTE_LOGIC_PROMPT_ACTION)
            route_logic_prompt = route_logic_prompt.replace("$$APP_DESCRIPTION$$", app_description)

        self.tables_prompt = tables_prompt
        self.relations_prompt = relations_prompt
        self.schema_prompt = schema_prompt
        self.controllers_prompt = controllers_prompt
        self.routes_prompt = routes_prompt
        self.route_logic_prompt = route_logic_prompt

    def parse_relations_prompt(self, models: list[str]) -> None:
        models_str = ", ".join(models)
        self.relations_prompt = self.relations_prompt.replace("$$DB_TABLES$$", models_str)

    def parse_schema_prompt(self, models: list[str], relations: str) -> None:
        models_str = ", ".join(models)
        self.schema_prompt = self.schema_prompt.replace("$$DB_TABLES$$", models_str)
        self.schema_prompt = self.schema_prompt.replace("$$DB_RELATIONS$$", relations)

    def parse_controllers_prompt(self, models: list[str], relations: str) -> None:
        models_str = ", ".join(models)
        self.controllers_prompt = self.controllers_prompt.replace("$$DB_TABLES$$", models_str)
        self.controllers_prompt = self.controllers_prompt.replace("$$DB_RELATIONS$$", relations)

    def parse_routes_prompt(
            self,
            models: str,
            schema: str,
            relations: str,
            controllers: str,
    ) -> None:
        self.routes_prompt = self.routes_prompt.replace("$$DB_TABLES$$", models)
        self.routes_prompt = self.routes_prompt.replace("$$SCHEMA$$", schema)
        self.routes_prompt = self.routes_prompt.replace("$$DB_RELATIONS$$", relations)
        self.routes_prompt = self.routes_prompt.replace("$$CONTROLLERS$$", controllers)

    def parse_route_logic_prompt(
            self,
            schema: str,
            method: str,
            url: str,
            description: str,
    ) -> str:
        api_str = f"{method.upper()} {url}"
        self.route_logic_prompt = self.route_logic_prompt.replace("$$SCHEMA$$", schema)
        self.route_logic_prompt = self.route_logic_prompt.replace("$$API_ROUTE$$", api_str)
        self.route_logic_prompt = self.route_logic_prompt.replace("$$ROUTE_DESCRIPTION$$", description)

        return self.route_logic_prompt

