import os
import shutil
import traceback

from TemplateParser.Mailer import Mailer
from TemplateParser.MailerTemplate import MailerTemplate
from TemplateParser.Model import Model
from TemplateParser.Project import Project
from TemplateParser.Relation import Relation
from TemplateParser.Route import Route
from TemplateParser.Middleware import Middleware
from TemplateParser.helpers import camel_to_snake, pascal_case
from TemplateParser.Controller import Controller
from page_builder import build_controller_page, build_db_page, build_middlewares_page, build_model_page, \
    build_routes_page, build_server_page, build_transporter_page, build_mailer_page, build_base_mailer_page, \
    build_default_layout_page, build_mailer_template_page, build_dotenv_page, build_package_json_page


def call_function_by_name(function_name, *args, **kwargs):
    # Get the function object
    function = globals().get(function_name)

    # Check if the function exists
    if function is None:
        raise ValueError(f"Function '{function_name}' not found")

    # Call the function and return the result
    return function(*args, **kwargs)


def create_directories(
        project_root: str,
        server_path: str,
        project: Project) -> None:
    """
    Creates appropriate project export directories
    """
    os.mkdir(f"./{project.project_name}")
    os.chdir(project_root)
    os.mkdir("./server")

    os.chdir(server_path)
    os.mkdir("./controllers")
    os.mkdir("./models")
    os.mkdir("./config")
    os.mkdir("./routes")
    if len(project.mailers) > 0:
        os.mkdir("./mailers")


def project_from_builder_data(builder_data, exportable=False) -> tuple:
    """
    Parses the Buildfile and creates a project object with all the necessary project specifications in builder_data.
    Returns (Project, Exception) tuple where Project is null if there is an error and Exception is null if the project
    build succeeded
    """
    try:
        project_name = camel_to_snake(builder_data['project_name'])
        db_params = builder_data['db_params']
        auth_model_name = pascal_case(builder_data['auth_object'])
        mongostr = builder_data['mongostr']
        server_port = builder_data['server_port']
        email = builder_data['email']
        controllers = builder_data["controllers"]
        routes = builder_data["routes"]
        middlewares = builder_data["middlewares"]
        relations = builder_data["relations"]
        mailers = builder_data["mailers"]

        # PARSING MODELS
        models = []
        for model in db_params:
            model_obj = Model(
                id=model["id"],
                name=model['model_name'],
                schema=model['schema'],
                auth=model['auth'] if 'auth' in model else False
            )
            models.append(model_obj)

        controller_map = {}
        for controller in controllers:
            controller_map[controller["id"]] = controller["name"]

        middlewares_array = []
        middleware_map = {}
        for middleware in middlewares:
            middleware_map[middleware["id"]] = middleware["handler"]
            middlewares_array.append(Middleware(middleware["id"], middleware["handler"], middleware["logic"]))

        routes_table = {}
        for route in routes:
            name_array = []

            for _id in route["middleware"]:
                name_array.append(middleware_map[_id])

            route_obj = Route(
                controller_id=route["controller"],
                controller_name=controller_map[route["controller"]],
                id=route["id"],
                url=route["url"],
                handler=route["handler"],
                verb=route["verb"],
                logic=route["logic"],
                middleware=name_array
            )
            if route_obj.controller_id in routes_table:
                routes_table[route_obj.controller_id].append(route_obj)
            else:
                routes_table[route_obj.controller_id] = []
                routes_table[route_obj.controller_id].append(route_obj)

        # Convert relations array into an array of Relation objects
        relations_arr = []
        for rel in relations:
            rel_obj = Relation(
                _id=rel['id'],
                model_a=rel['model_a'],
                model_b=rel['model_b'],
                field_a=rel['field_a'],
                field_b=rel['field_b'],
                relation_name=rel['relation_name'],
                relation_type=rel['relation_type'],
            )
            relations_arr.append(rel_obj)

        # convert mailers json into array of Mailer objects
        mailers_arr = []
        for mailer in mailers:
            templates_arr = []
            for temp in mailer["templates"]:
                temp_obj = MailerTemplate(
                    _id=temp["id"],
                    name=temp["name"],
                    content=temp["content"],
                )
                templates_arr.append(temp_obj)

            mailer_obj = Mailer(
                _id=mailer["id"],
                name=mailer["name"],
                templates=templates_arr
            )
            mailers_arr.append(mailer_obj)

        # Create array of controller objects
        controllers_objects = []
        for controller in controllers:
            controller_obj = Controller(
                name=controller["name"],
                id=controller["id"],
                model_affiliation=controller["affiliation"],
            )
            for temp_route in routes_table[controller["id"]]:
                controller_obj.addRoutes(temp_route)

            controllers_objects.append(controller_obj)

        # CREATE PROJECT
        project = Project(
            project_name=project_name,
            models=models,
            controllers=controllers_objects,
            auth_object=auth_model_name,
            email=email,
            middlewares=middlewares_array,
            relations=relations_arr,
            mailers=mailers_arr,
            server_port=server_port,
            mongostr=mongostr,
            styled=False,
            avoid_exceptions=not exportable
        )

        return project, None
    except Exception as e:
        traceback.print_exc()
        return None, e


def get_query_string(node_id, query):
    # Split the string by the '&' character
    items = node_id.split("&")

    # Iterate through the items and find the one that starts with "controller="
    for item in items:
        if item.startswith(f"{query}="):
            # Split the item by the '=' character and return the second part (the value)
            return item.split("=")[1]

    # If no item was found, return None
    return None


def process_tree(structure, project):
    # Iterate through the children of the root node
    for node in structure["children"]:
        # Check if the node is a folder
        if node["type"] == "folder":
            # Call os.mkdir() to create the folder
            os.mkdir(node["name"])
            os.chdir(node["name"])

            # Recursively process the children of the folder
            process_tree(node, project)
            os.chdir("..")
        else:
            # The node is a file, so call the build_*_page() function
            node_id = node["id"]
            model_name = get_query_string(node_id, "model")
            controller_name = get_query_string(node_id, "controller")
            mailer_name = get_query_string(node_id, "mailer")
            template_name = get_query_string(node_id, "template")

            model = project.model_from_name(model_name)
            controller = project.controller_from_name(controller_name)
            mailer = project.mailer_from_name(mailer_name)
            mailer_template = project.mailer_template_from_name(mailer_name, template_name)

            if model:
                call_function_by_name(node["function"], project, model, is_preview=False)
            elif controller:
                call_function_by_name(node["function"], project, controller, is_preview=False)
            elif mailer and not mailer_template:
                call_function_by_name(node["function"], project, mailer, is_preview=False)
            elif mailer and mailer_template:
                call_function_by_name(node["function"], project, mailer_template, is_preview=False)
            else:
                call_function_by_name(node["function"], project, is_preview=False)


def generator(builder_data) -> tuple:
    project, error = project_from_builder_data(builder_data, exportable=True)
    if error:
        return None, error

    try:
        # CREATING DIRECTORIES
        project_structure = project.build_directory()

        root_dir = os.path.abspath(os.curdir)
        project_root = f"{root_dir}/{project.project_name}"
        server_path = f"{project_root}/server"

        os.mkdir(f"./{project.project_name}")
        os.chdir(project_root)

        process_tree(project_structure, project)

        os.chdir(root_dir)
        shutil.make_archive(f"neutrino_project_{project.project_name}", 'zip', project.project_name)
        shutil.rmtree(project.project_name)

        print(f"Neutrino Task: {project.project_name}")
        return project.project_name, None

    except Exception as e:
        traceback.print_exc()
        return None, e


def generator_old(builder_data) -> tuple:
    project, error = project_from_builder_data(builder_data, exportable=True)
    if error:
        return None, error

    try:
        # CREATING DIRECTORIES
        root_dir = os.path.abspath(os.curdir)
        project_root = f"{root_dir}/{project.project_name}"
        server_path = f"{project_root}/server"
        create_directories(project_root, server_path, project)

        # Files in root folder
        os.chdir(server_path)
        build_server_page(project, is_preview=False)
        build_package_json_page(project, is_preview=False)
        build_dotenv_page(project, is_preview=False)
        build_readme_page(project, is_preview=False)

        # Db connection and other config files
        os.chdir('./config')
        build_db_page(project, is_preview=False)
        os.chdir(server_path)

        # Controller files
        os.chdir('./controllers')
        for controller in project.controllers:
            build_controller_page(project, controller, is_preview=False)
        os.chdir(server_path)

        # Model files
        os.chdir('./models')
        for model in project.models:
            build_model_page(project, model, is_preview=False)
        os.chdir(server_path)

        # Mailer files
        os.chdir('./mailers')
        build_transporter_page(project, is_preview=False)
        build_base_mailer_page(project, is_preview=False)
        for mailer in project.mailers:
            build_mailer_page(project, mailer, is_preview=False)
        os.chdir(server_path)

        # Route files
        os.chdir('./routes')
        build_routes_page(project, is_preview=False)

        # BUILD MIDDLEWARE FILES
        if len(project.middlewares) != 0:
            build_middlewares_page(project, is_preview=False)
        os.chdir(server_path)

        os.chdir(root_dir)
        shutil.make_archive(f"neutrino_project_{project.project_name}", 'zip', project.project_name)
        shutil.rmtree(project.project_name)

        print(f"Neutrino Task: {project.project_name}")
        return project.project_name, None

    except Exception as e:
        traceback.print_exc()
        return None, e
