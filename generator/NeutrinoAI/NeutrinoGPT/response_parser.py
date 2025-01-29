import ast


class ModelsResponseParser:
    def __init__(self, models_str):
        self.models_str = models_str.strip()
        self.parsed = []

    def parse_models(self) -> (list[str], Exception):
        parsed, error = parse_string_to_list(self.models_str)
        self.parsed = parsed
        return parsed, error


class ControllersResponseParser:
    def __init__(self, controllers_str: str):
        self.controllers_str = controllers_str.strip()
        self.parsed = []

    def parse_controllers(self) -> (list[str], Exception):
        parsed, error = parse_string_to_list(self.controllers_str)
        self.parsed = parsed
        return parsed, error


class RoutesResponseParser:
    def __init__(self, routes_str: str):
        self.routes_str = routes_str.strip()
        self.parsed = []

    def parse_routes(self) -> (list[str], Exception):
        parsed, error = parse_controller_routes_str(self.routes_str)
        self.parsed = parsed
        return parsed, error


class RelationsResponseParser:
    def __init__(self, rels_str):
        self.relations_str = rels_str.strip()
        self.parsed = []

    def parse_relations(self) -> (list[str], Exception):
        parsed, errors = parse_relationships_str(self.relations_str)
        self.parsed = parsed
        return parsed, errors


class SchemaResponseParser:
    def __init__(self, models_str: str):
        self.schema_str = models_str.strip()
        self.parsed = []

    def parse_schema(self) -> (list[str], Exception):
        parsed, errors = parse_schema_str(self.schema_str)
        self.parsed = parsed
        return parsed, errors


def relations_to_readable_string(
        parsed: list[tuple[str, str, str, str, str, str]]
) -> str:
    """
    Given list of relationships, returns a readable string version
    """
    rel_str = ""
    for rel in parsed:
        relation_name, model_a, model_b, rel_type, rel_a, rel_b, joint_table = rel
        rel_str += f"{relation_name},{model_a},{model_b},{rel_type},{rel_a},{model_b},{rel_b}"
        if joint_table:
            rel_str += f",{joint_table}"
        rel_str += ";\n"
    return rel_str


def parse_string_to_list(string) -> (list[str], Exception):
    """
    Parses a string representation of a list and returns an actual list
    """
    parsed_list = string.split(",")
    parsed_list = [x.strip() for x in parsed_list]

    if len(parsed_list) == 0:
        return [], ValueError("Invalid string format")

    return parsed_list, None


def parse_relationships_str(relationships_str) -> (tuple[str, str, str, str, str, str, str], list[Exception]):
    """
    Returns list representation of relationships and a list of errors for logging (if any)
    """
    relationships = []
    errors = []
    for relationship in relationships_str.strip().split("\n"):
        relationship = relationship.rstrip(";")
        relationship_parts = relationship.split(",")
        if len(relationship_parts) not in (6, 7):
            errors.append(ValueError(f"Invalid number of parts in relationship string: {relationship}"))
            continue

        relation_name, model_a, model_b, rel_type, rel_a, rel_b = relationship_parts[:6]
        joint_table = relationship_parts[6] if len(relationship_parts) == 7 else None
        rel = (relation_name.strip(), model_a.strip(), model_b.strip(), rel_type.strip(), rel_a.strip(), rel_b.strip(),
               joint_table)
        relationships.append(rel)

    return relationships, errors


def parse_schema_str(models_str) -> (list[list[str]], list[Exception]):
    """
    Parses a string of models and their fields and returns a list of tuples representing the models and their fields.
    Each tuple consists of a model name and a list of field tuples, where each field tuple consists of a field name and a field type.

    :param models_str: string representation of models and their fields
    :return: a list of model tuples and a list of error messages
    """
    lines = models_str.strip().split('\n')
    models = []
    model_name = None
    fields = []
    errors = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if ': ' in line:
            try:
                field_name, field_type = line.split(': ')
                fields.append((field_name.strip(), field_type.strip()))
            except ValueError:
                errors.append(f"Invalid field definition: {line}")
        else:
            if model_name is not None:
                models.append((model_name, fields))
                fields = []
            model_name = line
    if model_name is not None and fields:
        models.append((model_name, fields))
    return models, errors


def parse_controller_routes_str(routes_str: str) -> (list[(str, (str, str, str, str))], list[ValueError]):
    """
    :return is a list of routes and a list of errors
    routes are in following format: (controller_name, (verb, path, handler, description))
    """
    routes = []
    errors = []
    current_controller = None
    standard_crud = ["index", "show", "create", "update", "delete"]
    for line in routes_str.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.endswith(':'):
            current_controller = line[:-1].strip()
        elif line.lower() in standard_crud:
            routes.append((current_controller, [line.lower()]))
        else:
            try:
                verb, path, handler, description = line.split(' | ')
                routes.append((current_controller, [verb.lower(), path, handler, description]))
            except Exception as e:
                errors.append(ValueError(f"Error processing routes line '{line}': {str(e)}"))

    return routes, errors


def format_routes_list_to_string(routes):
    result = []
    for route in routes:
        controller, actions = route
        result.append(f"{controller}:")
        for action in actions:
            if isinstance(action, list):
                result.append(f"{action[0].upper()} | {action[1]} | {action[2]} | {action[3]}")
            else:
                result.append(action)
        result.append("")
    return "\n".join(result)


def format_relationships_list_to_string(
        relationships_list: list[(str, str, str, str, str, str, str)]
) -> str:
    """
    Given list of relationships, returns a readable string version
    """
    rel_str = ""
    for rel in relationships_list:
        relation_name, model_a, model_b, rel_type, rel_a, rel_b, joint_table = rel
        rel_str += f"{relation_name},{model_a},{model_b},{rel_type},{rel_a},{model_b},{rel_b}"
        if joint_table:
            rel_str += f",{joint_table}"
        rel_str += ";\n"
    return rel_str


def format_schema_list_to_str(schema_list: list[(str, list[(str, str)])]) -> str:
    """
    Converts a list of models and their fields back into a string representation.

    :param schema_list: A list of tuples, where each tuple represents a model and its fields.
    The first item in the tuple is the model name as a string. The second item is a list
    of tuples, where each tuple represents a field and its type. The first item in each
    field tuple is the field name as a string. The second item is the field type as a string.
    :return: A string representation of the models and their fields. Each model is separated by
    a newline character. Each field is separated by a newline character within each model.
    """
    result = []
    for model in schema_list:
        name, fields = model
        result.append(f"{name}:")
        for field in fields:
            result.append(f"{field[0]}: {field[1]}")
        result.append("")
    return "\n".join(result)


if __name__ == "__main__":
    routes_str = """
    AuthController:
POST | /auth/login | Logs in a user
POST | /auth/login | Registers a new user

UserController:
index
show

PostController:
index
show
create
update
delete
POST | /api/posts/:id/retweet | Create a retweet for a specific post

CommentController:
index
show
create
update
delete
"""

    parsed_routes, errors = parse_controller_routes_str(routes_str)

    #     models_str = '["User", "Post", "Comment"]'
    #     models_parser = ModelsResponseParser(models_str)
    #     parsed_models, error = models_parser.parse_models()
    #
    #     print(parsed_models)
    #
    #     relations_str = """
    # AuthorshipHandler,User,Post,one-to-many,posts,author;
    # CommentHandler,Post,Comment,one-to-many,comments,post;
    # GroupMembershipHandler,User,Group,many-to-many,groups,members,Membership;
    # LikeHandler,User,Post,many-to-many,liked_posts,liked_by,Like;
    #     """
    #
    #     rels_parser = RelationsResponseParser(relations_str)
    #     parsed_rels, errors = rels_parser.parse_relations()
    #
    #     print(parsed_rels)
    #
    schema_str = """
User
username: string
email: string
password: string

Post
title: string
content: string

Comment
content: string

Group
name: string
description: string
    """

    schema_parser = SchemaResponseParser(schema_str)
    parsed_schema, errors = schema_parser.parse_schema()

    print(parsed_schema)
