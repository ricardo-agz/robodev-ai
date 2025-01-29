import os
from generator.TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.helpers import append_at_index

class ServerIndexPage(TemplateParser):
  def __init__(
      self,
      project : Project,
      is_preview = False
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "server_index.js"
    out_file = "./server.js"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
      is_preview=is_preview
    )

    self.parse_file()

  def parse_file(self):
    for line in self.lines:
      if "$$" in line and "dyn" in line:
        line = line.strip().split(":")
        if len(line) <= 1:
          continue

        n_dyn = int(line[1])

        """ CONTROLLER DECLARATIONS """
        if n_dyn == 0:
          insert = self.add_controller_declarations()
          self.out_lines = self.out_lines + insert
          
        """ ROUTE DECLARATIONS """
        if n_dyn == 1:
          insert = self.write_routes()
          self.out_lines = self.out_lines + insert

      elif "$$importJWT$$" in line:
        insert = "const jwt = require('jsonwebtoken');\n"
        if self.project.auth_object:
          self.out_lines.append(insert)

      elif "$$verifyJWT$$" in line:
        insert = "const verifyJWT = require('./middlewares/verifyJWT');\n"
        if self.project.auth_object:
          self.out_lines.append(insert)

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

  