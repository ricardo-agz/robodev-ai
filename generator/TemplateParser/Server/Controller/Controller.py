import os
from TemplateParser.Controller import Controller
from generator.TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.helpers import append_at_index, camel_case, pascal_case, import_generator


class ControllerPage(TemplateParser):
    def __init__(
            self,
            project: Project,
            controller: Controller,

            is_auth: bool = False,
            is_preview=False,
    ) -> None:
        self.controller = controller

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        """ CONSTANTS """
        if is_auth:
            in_file = "auth_controller.js"
            out_file = f"./authController.js"
        else:
            in_file = "server_controller.js"
            out_file = f"./{camel_case(controller.name)}Controller.js"

        super().__init__(
            in_file,
            out_file,
            __location__,
            project,
            model=controller,
            is_preview=is_preview
        )

        self.is_auth = is_auth
        self.parse_file()

    def add_populate(self):
        out = []
        for many_name, alias in self.model.get_has_many():
            many_model = self.project.model_from_name(many_name)
            many_params = many_model.get_display_params()
            out.append(f"\t\t\t\t.populate({{ path: '{camel_case(alias)}', select: '{many_params}' }})\n")
        return out

    def get_route(self, name: str):
        for route in self.model.routes:
            if route.name.lower() == name.lower():
                return route
        return None

    def parse_file(self):
        for line in self.lines:

            if "$$imports$$" in line:
                # const $$Name$$ = require('../models/$$nameCamel$$');
                logic_lines = []
                for route in self.controller.routes:
                    logic_lines += route.logic
                self.out_lines.append(import_generator(logic_lines))

            elif "$$handler$$" in line:
                for route in self.controller.routes:
                    self.out_lines += route.get_handler_function() + "\n"

            else:
                self.out_lines.append(line)

    def add_controller_declarations(self):
        """
        const UserController = require('./controllers/UserController');
        const CourseController = require('./controllers/CourseController');
        """
        out = []
        for controller in self.project.controllers:
            out.append(f"const {controller.name}Controller = require('./controllers/{controller.name}Controller');\n")
        return out

    def write_routes(self):
        """
        app.get('/users', UserController.all)
        app.get('/users/:id', verifyJWT, UserController.find)
        app.post('/users', verifyJWT, UserController.create)
        app.put('/users/:id/edit', UserController.update)
        app.delete('/users/:id', UserController.delete)
        """
        out = []
        for controller in self.project.controllers:
            for route in controller.routes:
                out.append(route.get_route_call())
            out.append("\n")
        return out
