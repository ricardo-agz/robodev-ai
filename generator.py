from distutils.command.build import build
import os
import shutil
from TemplateParser.Mailer import Mailer
from TemplateParser.MailerTemplate import MailerTemplate
from TemplateParser.Model import Model
from TemplateParser.Project import Project
from TemplateParser.Relation import Relation
from TemplateParser.Route import Route
from TemplateParser.Middleware import Middleware
from TemplateParser.Server.Database.DatabasePage import DatabasePage
from TemplateParser.Server.DotEnv.DotEnvPage import DotEnvPage
from TemplateParser.Server.Index.ServerIndexPage import ServerIndexPage
from TemplateParser.Server.Controller.Controller import ControllerPage
from TemplateParser.Server.Model.ModelPage import ModelPage
from TemplateParser.Server.Middlewares.MiddlewaresPage import MiddlewaresPage
from TemplateParser.Server.PackageJSON.PackageJSONPage import PackageJSONPage
from TemplateParser.Server.Readme.ReadmePage import ReadmePage
from TemplateParser.Server.Routes.RoutesPage import RoutesPage
from TemplateParser.helpers import camel_case, camel_to_snake, pascal_case
from TemplateParser.Controller import Controller
from TemplateParser.Server.MailerTransporter.MailerTransporterPage import MailerTransporterPage


def get_method_from_route(route: str) -> str:
    """
    Given route name (index, show, create update, delete), returns appropriate HTTP method
    ex. "index" -> "get"
    """
    if route == "index":
        return "get"
    elif route == "show":
        return "get"
    elif route == "create":
        return "post"
    elif route == "update":
        return "put"
    elif route == "delete" or route == "destroy":
        return "delete"
    else:
        return ""


def get_path_from_route(route: str, model: Model) -> str:
    """
    Given route name (index, show, create update, delete) and model object, returns appropriate route path
    ex. "/users/:id"
    """
    if route == "index":
        return f"/{model.plural.lower()}"
    elif route == "show":
        return f"/{model.plural.lower()}/:id"
    elif route == "create":
        return f"/{model.plural.lower()}"
    elif route == "update":
        return f"/{model.plural.lower()}/:id/edit"
    elif route == "delete" or route == "destroy":
        return f"/{model.plural.lower()}/:id"
    else:
        return ""


def create_directories(
        PROJECT_ROOT: str,
        SERVER_PATH: str,
        CLIENT_PATH: str,
        project: Project) -> None:
    """
    Creates client folder (public and src subfolders) and server folder
    (controllers and models subfolders)
    """

    os.mkdir(f"./{project.project_name}")  # Create main project folder
    os.chdir(PROJECT_ROOT)  # Navigate to project folder
    os.mkdir("./server")  # Create server folder

    """ SERVER """
    os.chdir(SERVER_PATH)  # navigate to server folder
    os.mkdir("./controllers")  # Create controllers folder
    os.mkdir("./models")  # Create models folder
    os.mkdir("./config")  # Create config folder
    os.mkdir("./routes")  # Create routes folder
    if len(project.mailers) > 0:
        os.mkdir("./mailers")  # Create mailers folder


# Why does project_from_builder_data exist. What is its purpose. Please provide documentation
def project_from_builder_data(builder_data):
    project_name = camel_to_snake(builder_data['project_name'])
    db_params = builder_data['db_params']
    auth_model_name = pascal_case(builder_data['auth_object'])
    mongostr = builder_data['mongostr']
    config = builder_data['config']
    server_port = builder_data['server_port']
    email = builder_data['email']
    controllers = builder_data["controllers"]
    routes = builder_data["routes"]
    middlewares = builder_data["middlewares"]
    relations = builder_data["relations"]
    mailers = builder_data["mailers"]

    # PARSING MODELS
    models = []

    print(builder_data)

    for model in db_params:
        model_obj = Model(
            id=model["id"],
            name=model['model_name'],
            schema=model['schema'],
            # has_many=model['has_many'],
            # belongs_to=model['belongs_to'],
            auth=model['auth'] if 'auth' in model else False
        )

        # model_obj.set_routes(routes)
        models.append(model_obj)

    routes_table = {}
    controller_map = {}
    middleware_map = {}

    middlewares_array = []
    for controller in controllers:
        controller_map[controller["id"]] = controller["name"]

    for middleware in middlewares:
        middleware_map[middleware["id"]] = middleware["handler"]
        middlewares_array.append(Middleware(middleware["id"], middleware["handler"], middleware["logic"]))

    for route in routes:
        name_array = []

        for id in route["middleware"]:
            name_array.append(middleware_map[id])

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
        config=config, 
        styled=False,
        avoid_exceptions=True
    )

    return project


def generator(builder_data):
    # try:
    project_name = camel_to_snake(builder_data['project_name'])
    db_params = builder_data['db_params']
    auth_model_name = pascal_case(builder_data['auth_object'])
    mongostr = builder_data['mongostr']
    config = builder_data['config']
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
            has_many=model['has_many'],
            belongs_to=model['belongs_to'],
            auth=model['auth'] if 'auth' in model else False
        )

        # model_obj.set_routes(routes)
        models.append(model_obj)

    middlewares_array = []
    routes_table = {}
    controller_map = {}
    middleware_map = {}

    for controller in controllers:
        controller_map[controller["id"]] = controller["name"]

    for middleware in middlewares:
        middleware_map[middleware["id"]] = middleware["handler"]
        middlewares_array.append(Middleware(middleware["id"], middleware["handler"], middleware["logic"]))

    for route in routes:
        name_array = []

        for id in route["middleware"]:
            name_array.append(middleware_map[id])

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

    # CREATE PROJECT
    project = Project(
        project_name=project_name,
        models=models,
        controllers=controllers_objects,
        relations=relations_arr,
        mailers=mailers_arr,
        auth_object=auth_model_name,
        email=email,
        middlewares=middlewares_array,
        server_port=server_port,
        mongostr=mongostr,
        config=config, 
        styled=False
    )

    # CREATING DIRECTORIES
    ROOT_DIR = os.path.abspath(os.curdir)
    PROJECT_ROOT = f"{ROOT_DIR}/{project_name}"
    SERVER_PATH = f"{PROJECT_ROOT}/server"
    CLIENT_PATH = f"{PROJECT_ROOT}/client"
    create_directories(PROJECT_ROOT, SERVER_PATH, CLIENT_PATH, project)

    """ 
    ----- SERVER -----
    """

    # BUILD SERVER INDEX PAGE
    os.chdir(SERVER_PATH)
    server_index = ServerIndexPage(project)
    server_index.write_out_file()
    server_index.close_files()

    package = PackageJSONPage(project)
    package.write_out_file()
    package.close_files()

    env = DotEnvPage(project)
    env.write_out_file()
    env.close_files()

    readme = ReadmePage(project)
    readme.write_out_file()
    readme.close_files()

    # BUILD DB CONNECTION PAGE
    os.chdir('./config')
    db_page = DatabasePage(project)
    db_page.write_out_file()
    db_page.close_files()
    os.chdir(SERVER_PATH)

    # BUILD CONTROLLER FILES
    os.chdir('./controllers')
    for controller in project.controllers:
        model_controler = ControllerPage(project, controller)
        model_controler.write_out_file()
        model_controler.close_files()
    os.chdir(SERVER_PATH)

    # BUILD MODEL FILES
    os.chdir('./models')
    for model in project.models:
        model_page = ModelPage(project, model)
        model_page.write_out_file()
        model_page.close_files()
    os.chdir(SERVER_PATH)

    # BUILD MAILER FILES
    os.chdir('./mailers')
    transporter_page = MailerTransporterPage(project)
    transporter_page.write_out_file()
    transporter_page.close_files()
    for mailer in project.mailers:
        pass
        # mailer_page = ModelPage(project, model)
        # mailer_page.write_out_file()
        # mailer_page.close_files()
    os.chdir(SERVER_PATH)

    # BUILD ROUTE FILES
    os.chdir('./routes')
    routes = RoutesPage(project)
    routes.write_out_file()
    routes.close_files()

    # BUILD MIDDLEWARE FILES
    if len(middlewares_array) != 0:
        middlewares = MiddlewaresPage(project)

        middlewares.write_out_file()
        middlewares.close_files()
    os.chdir(SERVER_PATH)


    # """ 
    # ----- CLIENT -----
    # """
    # os.chdir(CLIENT_PATH)
    # client_package = ClientPackagePage(project)
    # client_package.write_out_file()
    # client_package.close_files()

    # os.chdir('./public')
    # index_html = IndexHtmlPage(project)
    # index_html.write_out_file()
    # index_html.close_files()

    # manifest = ManifestPage(project)
    # manifest.write_out_file()
    # manifest.close_files()
    # os.chdir(CLIENT_PATH)

    # os.chdir('./src')
    # app_page = AppPage(project)
    # app_page.write_out_file()
    # app_page.close_files()

    # home_page = HomePage(project)
    # home_page.write_out_file()
    # home_page.close_files()

    # json_config = ConfigJsonPage(project)
    # json_config.write_out_file()
    # json_config.close_files()

    # src_index = SrcIndexPage(project)
    # src_index.write_out_file()
    # src_index.close_files()

    # index_css = SrcIndexCss(project)
    # index_css.write_out_file()
    # index_css.close_files()

    # app_css = AppCss(project)
    # app_css.write_out_file()
    # app_css.close_files()

    # if project.auth_object:
    #   os.chdir('./auth')
    #   private_route = PrivateRoutePage(project, project.auth_object)
    #   private_route.write_out_file()
    #   private_route.close_files()

    #   login_page = LoginPage(project)
    #   login_page.write_out_file()
    #   login_page.close_files()

    #   os.chdir(CLIENT_PATH)
    #   os.chdir('./src/hooks')
    #   use_auth = UseAuthPage(project, project.auth_object)
    #   use_auth.write_out_file()
    #   use_auth.close_files()

    #   use_find = UseFindPage(project, project.auth_object)
    #   use_find.write_out_file()
    #   use_find.close_files()

    #   auth_context = AuthContextPage(project, project.auth_object)
    #   auth_context.write_out_file()
    #   auth_context.close_files()

    #   os.chdir(CLIENT_PATH)
    #   os.chdir('./src/components')
    #   nav_page = NavPage(project, project.auth_object)
    #   nav_page.write_out_file()
    #   nav_page.close_files()

    #   os.chdir(CLIENT_PATH)
    #   os.chdir('./src/services')
    #   auth_header = AuthHeaderPage(project)
    #   auth_header.write_out_file()
    #   auth_header.close_files()

    # os.chdir(CLIENT_PATH)

    # os.chdir('./src/hooks')
    # use_api = UseApiPage(project)
    # use_api.write_out_file()
    # use_api.close_files()

    # os.chdir(CLIENT_PATH)
    # os.chdir('./src/pages')
    # for model in project.models:
    #   os.chdir(f'./{camel_case(model.name)}')
    #   show_one = ShowOnePage(project, model)
    #   show_one.write_out_file()
    #   show_one.close_files()

    #   show_all = ShowAllPage(project, model)
    #   show_all.write_out_file()
    #   show_all.close_files()

    #   show_edit = ShowEditPage(project, model)
    #   show_edit.write_out_file()
    #   show_edit.close_files()

    #   show_new = ShowNewPage(project, model)
    #   show_new.write_out_file()
    #   show_new.close_files()

    #   form_page = ValidatedFormPage(project, model)
    #   form_page.write_out_file()
    #   form_page.close_files()

    #   export_index = ExportIndexPage(project, model)
    #   export_index.write_out_file()
    #   export_index.close_files()
    #   os.chdir('..')

    os.chdir(ROOT_DIR)
    shutil.make_archive(f"neutrino_project_{project_name}", 'zip', project_name)
    shutil.rmtree(project_name)

    print(f"Neutrino Task: {project_name}")
    return {"succeeded": True, "project": project_name}


# except Exception as e:
#   return { "succeeded": False, "error": e }

json_input = {
    "project_name": "hello",
    "db_params": [
        {
            "model_name": "Model",
            "auth": "True",
            "id": ":r2: 4890",
            "schema": [
                {
                    "name": "username",
                    "required": "True",
                    "type": "String"
                },
                {
                    "name": "email",
                    "required": "True",
                    "type": "String"
                },
                {
                    "name": "password",
                    "required": "True",
                    "type": "String"
                }
            ],
            "has_many": [],
            "belongs_to": [],
            "routes": [
                {
                    "route": "index",
                    "middleware": "",
                    "logic": ""
                },
                {
                    "route": "show",
                    "middleware": "",
                    "logic": ""
                },
                {
                    "route": "create",
                    "middleware": "",
                    "logic": ""
                },
                {
                    "route": "update",
                    "middleware": "",
                    "logic": ""
                },
                {
                    "route": "delete",
                    "middleware": "",
                    "logic": ""
                }
            ]
        }
    ],
    "controllers": [
        {
            "name": "Model",
            "affiliation": ":r2: 4890",
            "id": ":r2: 118"
        }
    ],
    "routes": [
        {
            "controller": ":r2: 118",
            "id": ":r2: 7303",
            "middleware": [
                "verifyJWT"
            ],
            "logic": [
                {
                    "id": ":r2: 73038452",
                    "blockVariant": "query",
                    "varName": "data",
                    "params": "{}",
                    "model": "Model",
                    "multiple": "True"
                },
                {
                    "id": ":r8: 360",
                    "blockVariant": "create",
                    "success": [],
                    "error": []
                },
                {
                    "id": ":r2: 73039554",
                    "blockVariant": "return",
                    "status": 200,
                    "data": "True",
                    "returnContent": "data"
                }
            ],
            "url": "/models",
            "handler": "index",
            "verb": "get"
        },
        {
            "controller": ":r2: 118",
            "id": ":r2: 5317",
            "middleware": [],
            "logic": [
                {
                    "id": ":r2: 53171585",
                    "blockVariant": "query",
                    "varName": "data",
                    "params": "{ _id: id}",
                    "model": "Model",
                    "multiple": "False"
                },
                {
                    "id": ":r2: 53177102",
                    "blockVariant": "return",
                    "status": 200,
                    "data": "True",
                    "returnContent": "data"
                }
            ],
            "url": "/models/:id",
            "handler": "show",
            "verb": "get"
        },
        {
            "controller": ":r2: 118",
            "id": ":r2: 5480",
            "middleware": [],
            "logic": [
                {
                    "id": ":r2: 54805104",
                    "blockVariant": "create",
                    "varName": "newData",
                    "model": "Model",
                    "fields": "{}",
                    "success": [
                        {
                            "id": ":r2: 54806671",
                            "blockVariant": "return",
                            "status": 200,
                            "data": "False",
                            "returnContent": "New Model was successfully created!"
                        }
                    ],
                    "error": [
                        {
                            "id": ":r2: 54805999",
                            "blockVariant": "error",
                            "status": 500,
                            "returnContent": "Error creating new Model"
                        }
                    ]
                }
            ],
            "url": "/models",
            "handler": "create",
            "verb": "post"
        },
        {
            "controller": ":r2: 118",
            "id": ":r2: 5867",
            "middleware": [],
            "logic": [
                {
                    "id": ":r2: 58675504",
                    "blockVariant": "update",
                    "varName": "newData",
                    "params": "{ _id: id}",
                    "updateParams": "{}",
                    "model": "Model",
                    "multiple": "False",
                    "success": [
                        {
                            "id": ":r2: 58673735",
                            "blockVariant": "return",
                            "status": 200,
                            "data": "False",
                            "returnContent": "Model was successfully updated!"
                        }
                    ],
                    "error": [
                        {
                            "id": ":r2: 58675694",
                            "blockVariant": "error",
                            "status": 500,
                            "returnContent": "Error updating Model"
                        }
                    ]
                }
            ],
            "url": "/models/:id",
            "handler": "update",
            "verb": "put"
        },
        {
            "controller": ":r2: 118",
            "id": ":r2: 9303",
            "middleware": [],
            "logic": [
                {
                    "id": ":r2: 9303512",
                    "blockVariant": "delete",
                    "varName": "data",
                    "params": "{ _id: id}",
                    "model": "Model",
                    "multiple": "False",
                    "success": [
                        {
                            "id": ":r2: 93031456",
                            "blockVariant": "return",
                            "status": 200,
                            "data": "False",
                            "returnContent": "Model was successfully deleted"
                        }
                    ],
                    "error": [
                        {
                            "id": ":r2: 93036257",
                            "blockVariant": "error",
                            "status": 500,
                            "returnContent": "Error deleting Model"
                        }
                    ]
                }
            ],
            "url": "/models/:id",
            "handler": "delete",
            "verb": "delete"
        }
    ],
    "auth_object": "Model",
    "server_port": 8080,
    "mongostr": "",
    "email": "mominayaan71@gmail.com"
}