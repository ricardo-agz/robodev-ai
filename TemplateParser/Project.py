from TemplateParser.Model import Model
from TemplateParser.Route import Route
from TemplateParser.Controller import Controller
from TemplateParser.helpers import camel_case, camel_to_dash, pascal_case, singularize, camel_to_snake

def val_in_tuple_arr(val, tup_arr):
  for (model_name, alias) in tup_arr:
    if val.lower() == model_name.lower():
      return True
  return False

class Project:
  """
  A class to represent a Neutrino project

  ...

  A project object holds a list of all Model objects 
  and is responsible for parsing their one-to-many and many-to-many relationships

  Attributes
  ----------
  project_name : str
    name of the project
  models : list[Model]
    list of all Model objects in project
  auth_object : Model
    model responsible for authenticaion (typically user)
  email : str
    email of user creating project
  server_port : int
    port to be used by express server
  mongostr : str
    mongoDB connection string
  styled : bool
    will the frontend be built with Material UI?
  warnings : list[str]
    returns a list of warnings that may or may not cause issues
  """

  def __init__(
      self,
      project_name : str,
      models : list[Model],
      controllers: list[Controller],
      auth_object : str,
      email : str,
      middlewares,
      server_port : int = 8080,
      mongostr : str = "<MONGO_CONNECTION_STRING>",
      styled : bool = True,
      avoid_exceptions = False
    ) -> None:

    self.project_name = project_name if project_name != "" else "untitled_project"
    self.models = models
    self.controllers = controllers
    self.auth_object = self.model_from_name(auth_object) if auth_object else None
    self.middlewares = middlewares
    self.server_port = server_port
    
    self.link = f"http://localhost:{server_port}"
    self.mongostr = mongostr
    self.email = email
    self.styled = styled
    self.warnings = []
    self.avoid_exceptions = avoid_exceptions
    self.build_failed = False
    self.parse_warnings()
    if not self.build_failed:
      self.set_relations()
      self.add_many_to_many_routes()


  def build_directory(self) -> dict:
    return init_project_structure(self.project_name, self.models, self.auth_object)

  def parse_warnings(self) -> None:
    model_names = []

    for model in self.models:
      """
      Error: Model has no params
      """
      if len(model.schema) == 0:
        severity = "Error"
        warning_type = "Invalid Model"
        warning_mssg = f"{model.name} has no params"

        self.warnings.append({"type": warning_type, "message": warning_mssg, "severity": severity})

      """
      Error: Multiple models with the same name
      """
      if model.name.lower() in model_names:
        severity = "Error"
        warning_type = "Invalid Model"
        warning_mssg = f"Model names must be unique. Multiple models with the name {model.name}"

        self.warnings.append({"type": warning_type, "message": warning_mssg, "severity": severity})

      for param in model.schema:
        if param['name'].lower() == "id" or param['name'].lower() == "_id":
          warning_type = "Unneccessary param"
          warning_mssg = f"Mongoose automatically adds an _id parameter, {param['name']} may cause bugs"

          self.warnings.append({"type": warning_type, "message": warning_mssg})
      
      model_names.append(model.name.lower())

    """
    Error: relation passed with model that doesn't exist (will cause build to fail)
    """
    for model in self.models:
      for (many_name, many_alias) in model.get_has_many():
        many_model = self.model_from_name(many_name)
        if not many_model:
          self.build_failed = True
          if self.avoid_exceptions:
            severity = "Error"
            warning_type = "Model Does Not Exist"
            warning_mssg = f"Error parsing model relations, '{many_name}' does not exist"

            self.warnings.append({"type": warning_type, "message": warning_mssg, "severity": severity})
          else:
            raise Exception(f"Build Failed: '{many_name}' does not exist")


  def contains_fatal_errors(self):
    """
    Returns true if the project contains at least 1 warning with 'error' severity
    This prevents a failed build from executing
    """
    errors = []
    for warning in self.warnings:
      if "severity" in warning and warning['severity'] == "Error":
        errors.append(warning)
    if len(errors) > 0:
      return errors

    return False


  def model_from_name(self, model_name : str) -> Model:
    '''
    Returns matching Model object (if any) from given model_name
    '''
    if not model_name:
      return None

    for model in self.models:
      if model.name.lower() == model_name.strip().lower():
        return model

    # raise Exception(f"{model_name} does not exist, models = {str(models_list)}")
    models_list = [model.name for model in self.models]
    # print(f"{model_name} does not exist, models = {str(models_list)}")
    return None

  def get_one_to_many_complement_alias(self, model : Model, alias : str) -> str:
    """
    Returns compementary alias in one-to-many relationship
    ex. User has_many Post as "posts", Post belongs_to User as "author"
        get_complement_alias(user, "posts") -> "author"
    """
    # model passed is parent
    for child, a in model.one_to_many:
      if alias.lower() == a.lower():
        for parent_name, a2 in child.belongs_to:
          if parent_name.lower() == model.name.lower():
            return a2

    # model passed is child
    for parent_name, a in model.belongs_to:
      parent = self.model_from_name(parent_name)
      if alias.lower() == a.lower():
        for child, a2 in parent.one_to_many:
          if child.name.lower() == model.name.lower():
            return a2

    # relationship does not exist
    return None      

  def set_relations(self) -> None:
    '''
    Iterates through list of Models and updates their one_to_many and many_to_many lists
    '''

    '''
    Adding parent to model schema if it belongs to another model
    '''
    for model in self.models:
      if len(model.get_belongs_to()) > 0:
        for parent_name, alias in model.get_belongs_to():
          new_param = {"name": parent_name, "type": "mongoose.Schema.Types.ObjectId", "required": True, "alias": alias}
          model.add_to_schema(new_param)

    for model in self.models:
      model_one_to_many = []
      model_many_to_many = []
      for (many_name, many_alias) in model.get_has_many():
        many_model = self.model_from_name(many_name)
        '''
        Error: relation passed with model that doesn't exist (will cause build to fail)
        '''
        if not many_model:
          if self.avoid_exceptions:
            severity = "Error"
            warning_type = "Model Does Not Exist"
            warning_mssg = f"Error parsing model relations '{many_name}' does not exist"

            self.warnings.append({"type": warning_type, "message": warning_mssg, "severity": severity})
          else:
            raise Exception(f"model: '{many_name}' does not exist")

        '''
        If model has many many_model and many_model belongs to model
        '''
        if many_model and model.does_have_many(many_model) and many_model.does_belong_to(model):
          model_one_to_many.append((many_model, many_alias))

        '''
        If model has many many_model and many_model has many model
        '''
        if model.does_have_many(many_model) and many_model.does_have_many(model):
          model_many_to_many.append((many_model, many_alias))

        '''
        Warning : undefined relationship
        '''
        if many_model and model.does_have_many(many_model) and not \
          (many_model.does_belong_to(model) or many_model.does_have_many(model)):
          warning_type = "Undefined Relationship"
          warning_mssg = (f"{model.name} has a relationship with "
            f"{many_model.name} but {many_model.name} does not have a relationship with {model.name}")

          self.warnings.append({"type": warning_type, "message": warning_mssg})

      model.set_one_to_many(model_one_to_many)
      model.set_many_to_many(model_many_to_many)


  def add_many_to_many_routes(self) -> None:
    for model in self.models:
      for (many_model, alias) in model.many_to_many:
        add_route_name = f"add{singularize(pascal_case(alias))}" if alias else f"add{many_model.name}"
        drop_route_name = f"drop{singularize(pascal_case(alias))}" if alias else f"add{many_model.name}"
        many_id = f"{camel_case(many_model.name)}Id"
        add_route = Route(
          handler=add_route_name, 
          verb="post",
          url=f"/{model.plural.lower()}/:id/{camel_to_dash(add_route_name)}/:{many_id}",
        )
        drop_route = Route(
          handler=drop_route_name, 
          verb="post", 
          url=f"/{model.plural.lower()}/:id/{camel_to_dash(drop_route_name)}/:{many_id}"
        )
        
        for controller in self.controllers:
          if (controller.model_affiliation == model.id):
            add_route.controller_id = controller.id
            add_route.controller_name = controller.name
            drop_route.controller_id = controller.id
            drop_route.controller_name = controller.name
            controller.addRoutes(add_route)
            controller.addRoutes(drop_route)



########## PROJECT STRUCTURE ##########
def init_project_structure(project_name, models, auth_object=None):
  """
  Function used to create tree of directories to preview files in builder
  """
  project_structure = {
    # ROOT
    "id": camel_to_snake(project_name),
    "name": camel_to_snake(project_name),
    "type": "folder",
    "children": [
      # CLIENT
      
      # {
      #   "id": "client",
      #   "name": "client",
      #   "type": "folder",
      #   "children": [
      #     # SRC
      #     {
      #       "id": "src",
      #       "name": "src",
      #       "type": "folder",
      #       "children": [
      #         # COMPONENTS
      #         {
      #           "id": "components",
      #           "name": "components",
      #           "type": "folder",
      #           "children": []
      #         },
      #         # HOOKS
      #         {
      #           "id": "hooks",
      #           "name": "hooks",
      #           "type": "folder",
      #           "children": [
      #             {
      #               "id": "use_api",
      #               "name": "useApi.js",
      #               "type": "file",
      #             }
      #           ]
      #         },
      #         # PAGES
      #         {
      #           "id": "pages",
      #           "name": "pages",
      #           "type": "folder",
      #           "children": [

      #           ]
      #         },
      #         {
      #           "id": "client_app",
      #           "name": "App.js",
      #           "type": "file",
      #         },
      #         {
      #           "id": "client_home",
      #           "name": "Home.js",
      #           "type": "file",
      #         },
      #       ]
      #     }
      #   ]
      # },
      
      # SERVER
      {
        "id": "server",
        "name": "server",
        "type": "folder",
        "children": [
          # CONFIG
          {
            "id": "config",
            "name": "config",
            "type": "folder",
            "children": [
              {
                "id": "database",
                "name": "database.js",
                "type": "file",
              },
            ]
          },
          # CONTROLLERS
          {
            "id": "controllers",
            "name": "controllers",
            "type": "folder",
            "children": [

            ]
          },
          # MODELS
          {
            "id": "models",
            "name": "models",
            "type": "folder",
            "children": [

            ]
          },
          # ROUTES
          {
            "id": "routes_folder",
            "name": "routes",
            "type": "folder",
            "children": [
              {
                "id": "routes",
                "name": "routes.js",
                "type": "file"
              }
            ]
          },
          {
            "id": "server_index",
            "name": "server.js",
            "type": "file"
          }
        ]
      }
    ]
  }

  model_files = []
  controller_files = []
  
  for model in models:
    model_files.append({
      "id": f"{model.name}_model",
      "name": f"{camel_case(model.name)}.js",
      "type": "file"    
    })
    controller_files.append({
      "id": f"{model.name}_controller",
      "name": f"{camel_case(model.name)}Controller.js",
      "type": "file"    
    })

    show_pages = []
    """
    for route in model.get_frontend_routes():
      if route.name == "index":
        show_pages.append({
          "id": f"{model.name}_indexpage",
          "name": f"{pascal_case(model.plural)}.js",
          "type": "file"  
        })
      elif route.name == "show":
        show_pages.append({
          "id": f"{model.name}_showpage",
          "name": f"{pascal_case(model.name)}Show.js",
          "type": "file"  
        })
      elif route.name == "create":
        show_pages.append({
          "id": f"{model.name}_createpage",
          "name": f"{pascal_case(model.name)}New.js",
          "type": "file"  
        })
      elif route.name == "update":
        show_pages.append({
          "id": f"{model.name}_updatepage",
          "name": f"{pascal_case(model.name)}Edit.js",
          "type": "file"  
        })
    """

    """Frontend"""
    # project_structure['children'][0]['children'][0]['children'][2]['children'].append({
    #   "id": f"{model.name}_folder",
    #   "name": f"{camel_case(model.name)}",
    #   "type": "folder",
    #   "children": show_pages
    # })

  if auth_object:
    """ SERVER """
    # add auth controler to controllers folder
    controller_files.append({
      "id": f"{auth_object.name}_controller_auth",
      "name": f"authController.js",
      "type": "file"    
    })
    # add middlewares page to routes folder
    ## changed first ['children'][1] to ['children'][0] because we sommented out client part
    project_structure['children'][0]['children'][3]['children'].append({
      "id": "middlewares",
      "name": "middlewares.js",
      "type": "file"
    })

    """ CLIENT """
    # add Auth folder
    """
    project_structure['children'][0]['children'][0]['children'].insert(0, {
      "id": "auth_folder",
      "name": "auth",
      "type": "folder",
      "children": [
        {
          "id": "login_page",
          "name": "Login.js",
          "type": "file"
        },
        {
          "id": "private_route",
          "name": "PrivateRoute.js",
          "type": "file"
        }
      ]
    })
    # add nav to components folder
    project_structure['children'][0]['children'][0]['children'][1]['children'].append({
      "id": "navbar",
      "name": "Nav.js",
      "type": "file"
    })
    # Add auth hooks
    auth_hooks = [
      {
        "id": "use_auth",
        "name": "useAuth.js",
        "type": "file"
      },
      {
        "id": "use_find",
        "name": f"useFind{auth_object.name}.js",
        "type": "file"
      },
      {
        "id": "auth_context",
        "name": f"{camel_case(auth_object.name)}Auth.js",
        "type": "file"
      },
    ]
                               client         src            hooks
    project_structure['children'][0]['children'][0]['children'][2]['children'] += auth_hooks
    """
  
  # also changed ['children'][0] to ['children'][1]
  project_structure['children'][0]['children'][1]['children'] = controller_files  # controllers
  project_structure['children'][0]['children'][2]['children'] = model_files       # models

  return project_structure
  
