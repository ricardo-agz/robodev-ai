import os
import shutil
from TemplateParser.Model import Model
from TemplateParser.Project import Project
from TemplateParser.Route import Route
from TemplateParser.Client.App.AppPage import AppPage
from TemplateParser.Client.AppCss.AppCss import AppCss
from TemplateParser.Client.AuthContext.AuthContextPage import AuthContextPage
from TemplateParser.Client.AuthHeader.AuthHeaderPage import AuthHeaderPage
from TemplateParser.Client.ConfigJson.ConfigJsonPage import ConfigJsonPage
from TemplateParser.Client.ExportIndex.ExportIndexPage import ExportIndexPage
from TemplateParser.Client.Home.HomePage import HomePage
from TemplateParser.Client.IndexCss.SrcIndexCss import SrcIndexCss
from TemplateParser.Client.IndexHtml.IndexHtmlPage import IndexHtmlPage
from TemplateParser.Client.LoginPage.LoginPage import LoginPage
from TemplateParser.Client.Manifest.ManifestPage import ManifestPage
from TemplateParser.Client.Nav.NavPage import NavPage
from TemplateParser.Client.Package.PackagePage import ClientPackagePage
from TemplateParser.Client.PrivateRoute.PrivateRoute import PrivateRoutePage
from TemplateParser.Client.ShowAll.ShowAllPage import ShowAllPage
from TemplateParser.Client.ShowEdit.ShowEditPage import ShowEditPage
from TemplateParser.Client.ShowNew.ShowNewPage import ShowNewPage
from TemplateParser.Client.ShowOne.ShowOnePage import ShowOnePage
from TemplateParser.Client.SrcIndex.SrcIndexPage import SrcIndexPage
from TemplateParser.Client.UseApi.UseApiPage import UseApiPage
from TemplateParser.Client.UseAuth.UseAuthPage import UseAuthPage
from TemplateParser.Client.UseFind.UseFindPage import UseFindPage
from TemplateParser.Client.ValidatedForm.ValidatedFormPage import ValidatedFormPage
from TemplateParser.Server.Database.DatabasePage import DatabasePage
from TemplateParser.Server.DotEnv.DotEnvPage import DotEnvPage
from TemplateParser.Server.Index.ServerIndexPage import ServerIndexPage
from TemplateParser.Server.Controller.Controller import ControllerPage
from TemplateParser.Server.Model.ModelPage import ModelPage
from TemplateParser.Server.Middlewares.MiddlewaresPage import MiddlewaresPage
from TemplateParser.Server.PackageJSON.PackageJSONPage import PackageJSONPage
from TemplateParser.Server.Readme.ReadmePage import ReadmePage
from TemplateParser.Server.Routes.RoutesPage import RoutesPage
from TemplateParser.helpers import camel_case, camel_to_snake

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
    return f"/{model.plural.lower()}/:id"
  elif route == "create":
    return  f"/{model.plural.lower()}"
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
    project: Project ) -> None:
  """
  Creates client folder (public and src subfolders) and server folder
  (controllers and models subfolders)
  """

  os.mkdir(f"./{project.project_name}") # Create main project folder
  os.chdir(PROJECT_ROOT)        # Navigate to project folder
  os.mkdir("./server")          # Create server folder
  os.mkdir("./client")          # Create client folder

  """ CLIENT """
  os.chdir(CLIENT_PATH)         # navigate to client folder
  os.mkdir("./public")          # Create public folder
  os.mkdir("./src")             # Create src folder
  os.chdir("./src")
  os.mkdir("./hooks")
  if project.auth_object:
    os.mkdir("./services")
    os.mkdir("./components")
    os.mkdir("./auth")
  os.mkdir("./pages")
  os.chdir("./pages")
  for model in project.models:
    os.mkdir(f"./{camel_case(model.name)}")

  """ SERVER """
  os.chdir(SERVER_PATH)         # navigate to server folder
  os.mkdir("./controllers")     # Create controllers folder
  os.mkdir("./models")          # Create models folder
  os.mkdir("./config")          # Create config folder
  os.mkdir("./routes")          # Create routes folder


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
          middleware = route['middleware'],
          protected = True if route['middleware'].strip() == "verifyJWT" else False
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
    for model in project.models:
      model_controler = ControllerPage(project, model)
      model_controler.write_out_file()
      model_controler.close_files()
    if project.auth_object:
      auth_controler = ControllerPage(project, project.auth_object, is_auth=True)
      auth_controler.write_out_file()
      auth_controler.close_files()
    os.chdir(SERVER_PATH)

    # BUILD MODEL FILES
    os.chdir('./models')
    for model in project.models:
      model_page = ModelPage(project, model)
      model_page.write_out_file()
      model_page.close_files()
    os.chdir(SERVER_PATH)

    # BUILD ROUTE FILES
    os.chdir('./routes')
    routes = RoutesPage(project)
    routes.write_out_file()
    routes.close_files()
    if project.auth_object:
      middlewares = MiddlewaresPage(project)
      middlewares.write_out_file()
      middlewares.close_files()
    os.chdir(SERVER_PATH)

    """ 
    ----- CLIENT -----
    """
    os.chdir(CLIENT_PATH)
    client_package = ClientPackagePage(project)
    client_package.write_out_file()
    client_package.close_files()

    os.chdir('./public')
    index_html = IndexHtmlPage(project)
    index_html.write_out_file()
    index_html.close_files()

    manifest = ManifestPage(project)
    manifest.write_out_file()
    manifest.close_files()
    os.chdir(CLIENT_PATH)

    os.chdir('./src')
    app_page = AppPage(project)
    app_page.write_out_file()
    app_page.close_files()

    home_page = HomePage(project)
    home_page.write_out_file()
    home_page.close_files()

    json_config = ConfigJsonPage(project)
    json_config.write_out_file()
    json_config.close_files()

    src_index = SrcIndexPage(project)
    src_index.write_out_file()
    src_index.close_files()

    index_css = SrcIndexCss(project)
    index_css.write_out_file()
    index_css.close_files()

    app_css = AppCss(project)
    app_css.write_out_file()
    app_css.close_files()

    if project.auth_object:
      os.chdir('./auth')
      private_route = PrivateRoutePage(project, project.auth_object)
      private_route.write_out_file()
      private_route.close_files()

      login_page = LoginPage(project)
      login_page.write_out_file()
      login_page.close_files()

      os.chdir(CLIENT_PATH)
      os.chdir('./src/hooks')
      use_auth = UseAuthPage(project, project.auth_object)
      use_auth.write_out_file()
      use_auth.close_files()

      use_find = UseFindPage(project, project.auth_object)
      use_find.write_out_file()
      use_find.close_files()

      auth_context = AuthContextPage(project, project.auth_object)
      auth_context.write_out_file()
      auth_context.close_files()

      os.chdir(CLIENT_PATH)
      os.chdir('./src/components')
      nav_page = NavPage(project, project.auth_object)
      nav_page.write_out_file()
      nav_page.close_files()

      os.chdir(CLIENT_PATH)
      os.chdir('./src/services')
      auth_header = AuthHeaderPage(project)
      auth_header.write_out_file()
      auth_header.close_files()

    os.chdir(CLIENT_PATH)

    os.chdir('./src/hooks')
    use_api = UseApiPage(project)
    use_api.write_out_file()
    use_api.close_files()

    os.chdir(CLIENT_PATH)
    os.chdir('./src/pages')
    for model in project.models:
      os.chdir(f'./{camel_case(model.name)}')
      show_one = ShowOnePage(project, model)
      show_one.write_out_file()
      show_one.close_files()

      show_all = ShowAllPage(project, model)
      show_all.write_out_file()
      show_all.close_files()

      show_edit = ShowEditPage(project, model)
      show_edit.write_out_file()
      show_edit.close_files()

      show_new = ShowNewPage(project, model)
      show_new.write_out_file()
      show_new.close_files()

      form_page = ValidatedFormPage(project, model)
      form_page.write_out_file()
      form_page.close_files()

      export_index = ExportIndexPage(project, model)
      export_index.write_out_file()
      export_index.close_files()
      os.chdir('..')

    os.chdir(ROOT_DIR)
    shutil.make_archive(project_name, 'zip', project_name)
    shutil.rmtree(project_name)

    print(f"Neutrino Task: {project_name}")
    return project_name


  # except Exception as e:
  #   print("Something went wrong:/")
  #   print(e)