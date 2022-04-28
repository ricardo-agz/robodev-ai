import os
from venv import create
from TemplateParser.Model import Model
from TemplateParser.Project import Project
from TemplateParser.Route import Route
from TemplateParser.Server.Index.ServerIndexPage import ServerIndexPage
from TemplateParser.Server.Controller.Controller import ControllerPage
from TemplateParser.Server.Model.ModelPage import ModelPage
from TemplateParser.helpers import camel_to_snake

def get_method_from_route(route : str) -> str:
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

def get_path_from_route(route : str, model : Model) -> str:
  """
  Given route name (index, show, create update, delete) and model object, returns appropriate route path
  ex. "/users/:id"
  """
  if route == "index":
    return f"/{model.plural.lower()}"
  elif route == "show":
    return f"/{model.name.lower()}/:id"
  elif route == "create":
    return  f"/{model.plural.lower()}"
  elif route == "update":
    return f"/{model.name.lower()}/:id/edit"
  elif route == "delete" or route == "destroy":
    return f"/{model.name.lower()}/:id"
  else:
    return ""

def create_directories(
    PROJECT_ROOT: str, 
    SERVER_PATH: str, 
    CLIENT_PATH: str,
    project_name: str ) -> None:
  """
  Creates client folder (public and src subfolders) and server folder
  (controllers and models subfolders)
  """

  os.mkdir(f"./{project_name}") # Create main project folder
  os.chdir(PROJECT_ROOT)        # Navigate to project folder
  os.mkdir("./server")          # Create server folder
  os.mkdir("./client")          # Create client folder
  os.chdir(CLIENT_PATH)         # navigate to client folder
  os.mkdir("./public")          # Create public folder
  os.mkdir("./src")             # Create src folder
  os.chdir(SERVER_PATH)         # navigate to server folder
  os.mkdir("./controllers")     # Create controllers folder
  os.mkdir("./models")          # Create models folder


def generator(builder_data):
  # try:
    project_name = camel_to_snake(builder_data['project_name'])
    db_params = builder_data['db_params']
    auth_model_name = builder_data['auth_object']
    mongostr = builder_data['mongostr']
    server_port = builder_data['server_port']
    email = builder_data['email']

    # PARSING MODELS
    models = []
    for model in db_params:
      model_obj = Model(
        name = model['model_name'],
        schema = model['schema'],
        has_many = model['has_many'],
        belongs_to = model['belongs_to'],
        auth = model['auth'] if 'auth' in model else False
      )

      # PARSING ROUTES
      routes = []
      for route in model['routes']:
        route_obj = Route(
          name = route['route'], 
          method = route['method'] if 'method' in route else get_method_from_route(route['route']), 
          path = route['path'] if 'path' in route else get_path_from_route(route['route'], model_obj), 
          model = model_obj, 
          middleware = route['middleware']
        )
        routes.append(route_obj)

      model_obj.set_routes(routes)
      models.append(model_obj)

    # CREATE PROJECT
    project = Project(
      project_name = project_name,
      models = models,
      auth_object = auth_model_name,
      email = email,
      server_port = server_port,
      mongostr = mongostr,
      styled = False
    )

    # CREATING DIRECTORIES
    ROOT_DIR = os.path.abspath(os.curdir)
    PROJECT_ROOT = f"{ROOT_DIR}/{project_name}"
    SERVER_PATH = f"{PROJECT_ROOT}/server"
    CLIENT_PATH = f"{PROJECT_ROOT}/client"
    create_directories(PROJECT_ROOT, SERVER_PATH, CLIENT_PATH, project_name)

    # BUILD SERVER INDEX PAGE
    os.chdir(SERVER_PATH)
    server_index = ServerIndexPage(project)
    server_index.write_out_file()
    server_index.close_files()

    # BUILD CONTROLLER FILES
    os.chdir('./controllers')
    for model in project.models:
      model_controler = ControllerPage(project, model)
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


  # except Exception as e:
  #   print("Something went wrong:/")
  #   print(e)