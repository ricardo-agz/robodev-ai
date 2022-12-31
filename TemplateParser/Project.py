from TemplateParser import Middleware
from TemplateParser.MailerTemplate import MailerTemplate
from TemplateParser.Model import Model
from TemplateParser.Relation import Relation
from TemplateParser.Mailer import Mailer
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
            project_name: str,
            models: list[Model],
            controllers: list[Controller],
            relations: list[Relation],
            mailers: list[Mailer],
            auth_object: str,
            email: str,
            middlewares: list[Middleware],
            server_port: int = 8080,
            mongostr: str = "<MONGO_CONNECTION_STRING>",
            styled: bool = True,
            avoid_exceptions=False
    ) -> None:

        self.project_name = project_name if project_name != "" else "untitled_project"
        self.models = models
        self.controllers = controllers
        self.auth_object = self.model_from_name(auth_object) if auth_object else None
        self.middlewares = middlewares
        self.relations = relations
        self.mailers = mailers
        self.server_port = server_port

        self.link = f"http://localhost:{server_port}"
        self.mongostr = mongostr
        self.email = email
        self.styled = styled
        self.warnings = []
        self.avoid_exceptions = avoid_exceptions
        self.build_failed = False
        self.parse_warnings()

    def build_directory(self) -> dict:
        return init_project_structure(self.project_name, self.models, self.controllers, self.middlewares, self.mailers,
                                      self.auth_object)

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

    def model_from_name(self, model_name: str) -> Model:
        """
        Returns matching Model object (if any) from given model_name
        """
        if not model_name:
            return None

        for model in self.models:
            if model.name.lower() == model_name.strip().lower():
                return model

        # raise Exception(f"{model_name} does not exist, models = {str(models_list)}")
        models_list = [model.name for model in self.models]
        # print(f"{model_name} does not exist, models = {str(models_list)}")
        return None

    def mailer_from_name(self, mailer_name: str) -> Mailer:
        """
        Returns matching Model object (if any) from given model_name
        """
        if not mailer_name:
            return None

        for mailer in self.mailers:
            if mailer.name.lower() == mailer_name.strip().lower():
                return mailer

        return None

    def model_from_id(self, model_id: str) -> Model:
        """
        Returns matching Model object (if any) from given id
        """
        if not model_id:
            return None

        for model in self.models:
            if model.id == model_id:
                return model

        print(f"model {model_id} does not exist")
        return None

    def template_from_name(self, template_name: str) -> MailerTemplate:
        """
        Returns matching template object from name
        """
        if not template_name:
            return None

        for mailer in self.mailers:
            for temp in mailer.templates:
                if temp.name.lower() == template_name.lower():
                    return temp

        print(f"model {template_name} does not exist")
        return None

    def set_model_relations(self):
        for rel in self.relations:
            a_obj = self.model_from_id(rel.model_a)
            b_obj = self.model_from_id(rel.model_b)


########## PROJECT STRUCTURE ##########
def init_project_structure(project_name, models, controllers, middlewares, mailers, auth_object=None):
    """
    Function used to create tree of directories to preview files in builder
    """
    project_structure = {
        # ROOT
        "id": camel_to_snake(project_name),
        "name": camel_to_snake(project_name),
        "type": "folder",
        "children": [
            # (client is deprecated)
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

    for controller in controllers:
        controller_files.append({
            "id": f"{controller.name}_controller",
            "name": f"{camel_case(controller.name)}Controller.js",
            "type": "file"
        })

    if len(middlewares) != 0:
        project_structure['children'][0]['children'][3]['children'].append({
            "id": "middlewares",
            "name": "middlewares.js",
            "type": "file"
        })

    if len(mailers) > 0:
        project_structure['children'][0]['children'].insert(2, {
            "id": "mailers_folder",
            "name": "mailers",
            "type": "folder",
            "children": []
        })

        for dirname in project_structure['children'][0]['children']:
            if dirname["id"] == "mailers_folder":
                dirname["children"].append({
                    "id": "templates_folder",
                    "name": "templates",
                    "type": "folder",
                    "children": [
                        {
                            "id": "layouts_folder",
                            "name": "layouts",
                            "type": "folder",
                            "children": [
                                {
                                    "id": f"default_email_layout",
                                    "name": "default.hbs",
                                    "type": "file",
                                }
                            ]
                        },
                        {
                            "id": "partials_folder",
                            "name": "partials",
                            "type": "folder",
                            "children": []
                        },
                    ]
                })

                # append mailer templates
                templates_dir = dirname["children"][0]["children"]
                for mailer in mailers:
                    for template in mailer.templates:
                        templates_dir.append({
                            "id": f"{template.name.lower()}_template",
                            "name": f"{camel_case(template.name)}.hbs",
                            "type": "file",
                        })

                dirname["children"].append({
                    "id": f"base_mailer",
                    "name": "baseMailer.js",
                    "type": "file",
                })
                for mailer in mailers:
                    dirname["children"].append({
                        "id": f"{mailer.name}_mailer",
                        "name":
                            f"{camel_case(mailer.name)}Mailer.js" if "mailer" not in mailer.name.lower() else
                            f"{camel_case(mailer.name)}.js",
                        "type": "file",
                    })
                break

        # add middlewares page to routes folder
        ## changed first ['children'][1] to ['children'][0] because we sommented out client part

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

    for folder in project_structure["children"][0]["children"]:
        if folder["id"] == "models":
            folder["children"] = model_files
        elif folder["id"] == "controllers":
            folder["children"] = controller_files

    return project_structure
