from TemplateParser.Middleware import Middleware
from TemplateParser.MailerTemplate import MailerTemplate
from TemplateParser.Model import Model
from TemplateParser.Relation import Relation
from TemplateParser.Mailer import Mailer
from TemplateParser.Route import Route
from TemplateParser.Controller import Controller
from TemplateParser.helpers import camel_case, camel_to_dash, pascal_case, singularize, camel_to_snake
import yaml


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
        return init_project_structure(self)

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
                    warning_type = "Unnecessary param"
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

        return None

    def controller_from_name(self, controller_name: str) -> Model:
        """
        Returns matching Model object (if any) from given model_name
        """
        if not controller_name:
            return None

        for controller in self.controllers:
            if controller.name.lower() == controller_name.strip().lower():
                return controller

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

    def mailer_template_from_name(self, mailer_name: str, template_name: str) -> MailerTemplate:
        """
        Returns matching Template object (if any) from given mailer_name and template_name
        """
        if not mailer_name or not template_name:
            return None

        for mailer in self.mailers:
            if mailer.name.lower() == mailer_name.strip().lower():
                for template in mailer.templates:
                    if template.name.lower() == template_name.strip().lower():
                        return template

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


def append_to_project_structure(structure, key, value):
    # Find the correct folder in the structure
    folder = rec_find_node(structure, key)
    if folder is not None:
        # Append the value to the folder
        if not folder["children"]:
            folder["children"] = []
        folder["children"] = folder["children"] + value


def remove_from_project_structure(structure, key):
    folder = rec_find_parent(structure, key)
    if not folder or "children" not in folder:
        return False
    folder['children'] = [child for child in folder['children'] if child['id'] != key]
    return True


def find_node(structure, node_id):
    return rec_find_node(structure, node_id)


def rec_find_parent(nodes, node_id):
    if "children" in nodes and nodes["children"]:
        for child in nodes["children"]:
            if child["id"] == node_id:
                return nodes
            out = rec_find_parent(child, node_id)
            if out:
                return out
    return None


def rec_find_node(nodes, node_id):
    if nodes["id"] == node_id:
        return nodes
    if "children" in nodes and nodes["children"]:
        for child in nodes["children"]:
            out = rec_find_node(child, node_id)
            if out:
                return out
    return None


def init_project_structure(project):
    with open("project_structure.yaml", "r") as f:
        structure = yaml.safe_load(f)

    structure = structure["server"]
    structure["name"] = project.project_name

    # Insert model files
    model_files = []
    for model in project.models:
        model_files.append({
            "id": f"model-page&model={model.name}",
            "filename": f"{camel_case(model.name)}.js",
            "type": "file",
            "function": "build_model_page"
        })
    append_to_project_structure(structure, "models-folder", model_files)

    # Insert controller files
    controller_files = []
    for controller in project.controllers:
        controller_files.append({
            "id": f"controller-page&controller={controller.name}",
            "filename": f"{camel_case(controller.name)}Controller.js",
            "type": "file",
            "function": "build_controller_page"
        })
    append_to_project_structure(structure, "controllers-folder", controller_files)

    # Insert mailer files
    if len(project.mailers) > 0:
        mailer_files = []
        template_files = []
        for mailer in project.mailers:
            mailer_files.append({
                "id": f"mailer-page&mailer={mailer.name}",
                "filename": f"{camel_case(mailer.name)}Mailer.js",
                "type": "file",
                "function": "build_mailer_page"
            })
            # Insert mailer template files
            for template in mailer.templates:
                template_files.append({
                    "id": f"template-page&mailer={mailer.name}&template={template.name}",
                    "filename": f"{camel_case(template.name)}.hbs",
                    "type": "file",
                    "function": "build_mailer_template_page"
                })
        append_to_project_structure(structure, "mailers-folder", mailer_files)
        append_to_project_structure(structure, "templates-folder", template_files)
    else:
        remove_from_project_structure(structure, "mailers-folder")

    if len(project.middlewares) == 0:
        remove_from_project_structure(structure, "middlewares-file")

    return structure
