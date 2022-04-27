import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.helpers import append_at_index

class ControllerPage(TemplateParser):
  def __init__(
      self,
      project : Project,
      model
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "./server_controller.js"
    out_file = f"./{model.name}Controller.js"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
      model
    )

    self.parse_file()

  def add_populate(self):
    out = []
    for many_name, alias in self.model.get_has_many():
      many_model = self.project.model_from_name(many_name)
      many_params = many_model.get_display_params()
      out.append(f"\t\t\t\t.populate({{ path: '{alias.lower()}', select: '{many_params}' }})\n")
    return out


  def parse_file(self):
    for line in self.lines:

      #----- MODEL RELATIONSHIPS -----
      if "$$ONE_TO_MANY" in line:
        new_l = line.split(":")
        if new_l[1].strip() == "ONE" and len(self.model.has_many) > 0:
          insert = self.add_populate()
          self.out_lines = self.out_lines + insert

      elif "$$MANY_TO_MANY" in line:
        if len(self.model.get_many_to_many()) > 0:
          for many_model, alias in self.model.get_many_to_many():
            sub_in_f = "add_drop_many.txt"
            insert = self.add_snip_dynamic(sub_in_f, many_model, alias)
            self.out_lines = self.out_lines + insert

      #----- AUTH -----
      elif "$$AUTH$$:0" in line:
        if self.model.auth:
          insert = [
            'const jwt = require("jsonwebtoken");\n',
            'const bcrypt = require("bcrypt");\n',
            "require('dotenv').config();\n"
          ]
          self.out_lines = self.out_lines + insert
          
      elif "$$AUTH$$:1" in line:
        if self.model.auth:
          auth_f = "server_auth.txt"
          insert = self.add_snip_dynamic(auth_f)
          self.out_lines = self.out_lines + insert

      else:
        self.out_lines.append(line)


  '''
  def parse_file(self):
    new_lines = [x for x in self.lines]
    j = 0
    for i in range(len(self.lines)):
      line = self.lines[i]

      #----- MODEL RELATIONSHIPS -----
      if "$$ONE_TO_MANY" in line:
        new_l = line.split(":")
        if new_l[1].strip() == "ONE" and len(self.model.has_many) > 0:
          insert = self.add_populate()
          new_lines = append_at_index(new_lines, insert, j)
          j += len(insert)

      elif "$$MANY_TO_MANY" in line:
        if len(self.model.get_many_to_many()) > 0:
          for many_model, alias in self.model.get_many_to_many():
            sub_in_f = "add_drop_many.txt"
            insert = self.add_snip_dynamic(sub_in_f, many_model, alias)
            new_lines = append_at_index(new_lines, insert, j)
            j += len(insert)

      #----- AUTH -----
      elif "$$AUTH$$:0" in line:
        if self.model.auth:
          insert = [
            'const jwt = require("jsonwebtoken");\n',
            'const bcrypt = require("bcrypt");\n',
            "require('dotenv').config();\n"
          ]
          new_lines = append_at_index(new_lines, insert, j)
          j += len(insert)
          
      elif "$$AUTH$$:1" in line:
        if self.model.auth:
          auth_f = "server_auth.txt"
          insert = self.add_snip_dynamic(auth_f)
          new_lines = append_at_index(new_lines, insert, j)
          j += len(insert)

      #----- ROUTE LOGIC -----
      # elif "$$logic$$" in line:
      #   aroute = line.split(":")[1].strip()
      
      #   if aroute in route_dict:
      #     logic = model["route"][route_dict[aroute]]["logic"]
      #     logic = str(logic).replace("\\n", "\n").replace("\\t", "\t").split('\n')
      #     for a in logic:
      #       if "hide" in a:
      #         start = a.find("hide")
      #         substring = a[start:]
      #         substring = substring.split("=")
      #         substring = substring[1].split(",")
      #         for i, sub in enumerate(substring):
      #           if(i == 0):
      #             out_f.write("\n")
      #           out_f.write("\t\t\t"+a[0:start].replace("\n", "\n").replace('\t', "\t") + "data." + sub + " = undefined;\n")
      #       elif "error" in a:
      #         start = a.find("error")
      #         substring = a[start:].split("=")[1]
      #         # out_f.write("\n\t\t\t" + a[0:start] + "res.status(500).send('" + substring + "')\n")
      #         out_f.write("\n\t\t\t" + a[0:start] + "return res.status(500).send({ message: '" + substring + "' });\n")
      #       else:
      #         out_f.write("\t\t\t" + a)
      #   out_f.write("\n")  






      # if "$$" in line and "dyn" in line:
      #   line = line.strip().split(":")
      #   if len(line) <= 1:
      #     continue

      #   n_dyn = int(line[1])

      #   """ CONTROLLER DECLARATIONS """
      #   if n_dyn == 0:
      #     # insert = self.add_controller_declarations()
      #     # new_lines = append_at_index(new_lines, insert, i)
      #     pass
          
      #   """ ROUTE DECLARATIONS """
      #   if n_dyn == 1:
      #     # insert = self.write_routes()
      #     # new_lines = append_at_index(new_lines, insert, i)
      #     pass

      j += 1
    self.lines = new_lines
  '''

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

  