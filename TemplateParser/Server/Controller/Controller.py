import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.helpers import append_at_index, camel_case, pascal_case

class ControllerPage(TemplateParser):
  def __init__(
      self,
      project : Project,
      model : Model,
      is_auth : bool = False
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    if is_auth:
      in_file = "./auth_controller.js"
      out_file = f"./authController.js"
    else:
      in_file = "./server_controller.js"
      out_file = f"./{camel_case(model.name)}Controller.js"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
      model
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


  def parse_file(self):
    for line in self.lines:

      #----- MODEL RELATIONSHIPS -----
      if "$$ONE_TO_MANY" in line:
        new_l = line.split(":")
        if new_l[1].strip() == "ONE" and len(self.model.has_many) > 0:
          insert = self.add_populate()
          self.out_lines = self.out_lines + insert

      elif "$$CREATE_DECLARATIONS$$" in line:
        """
        const { name, username, age, } = req.body;
        const user = new UserModel({ name: name, username: username, age: age, });
        """
        line_1 = "\t\tconst { "
        for param in self.model.schema:
          line_1 += f"{param['name']}, "
        line_1 += "} = req.body;\n"
        self.out_lines.append(line_1)

        line_2 = f"\t\tconst {camel_case(self.model.name)} = new {self.model.name}({{ "
        for param in self.model.schema:
          line_2 += f"{param['name']}: {param['name']}, "
        line_2 += "});\n"
        self.out_lines.append(line_2)

      elif "$$UPDATE_PARAMS$$" in line:
        """
        name: req.body.name,
        username: req.body.username,
        """
        for param in self.model.schema:
          p_name = param['name']
          self.out_lines.append(f"\t\t\t{p_name}: req.body.{p_name},\n")

      elif "$$MANY_TO_MANY" in line:
        if len(self.model.get_many_to_many()) > 0:
          for many_model, alias in self.model.get_many_to_many():
            sub_in_f = "add_drop_many.txt"
            insert = self.add_snip_dynamic(sub_in_f, many_model, alias)
            self.out_lines = self.out_lines + insert

      #----- AUTH -----
      elif "$$AUTH$$:0" in line and self.is_auth:
        if self.model.auth:
          insert = [
            'const jwt = require("jsonwebtoken");\n',
            'const bcrypt = require("bcrypt");\n',
            "require('dotenv').config();\n",
            f"\nconst {self.model.name} = require('../models/{camel_case(self.model.name)}');\n"
          ]
          self.out_lines = self.out_lines + insert
          
      elif "$$AUTH$$:1" in line and self.is_auth:
        if self.model.auth:
          auth_f = "server_auth.txt"
          insert = self.add_snip_dynamic(auth_f)
          self.out_lines = self.out_lines + insert

      else:
        self.out_lines.append(line)
        

  def add_controller_declarations(self):
    """
    const UserController = require('./controllers/UserController');
    const CourseController = require('./controllers/CourseController');
    """
    out = []
    for model in self.project.models:
      out.append(f"const {model.name}Controller = require('./controllers/{model.name}Controller');\n")
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
    for model in self.project.models:
      for route in model.get_routes():
        out.append(route.get_route_call())
      out.append("\n")
    return out

  