import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.helpers import append_at_index, camel_case

class RoutesPage(TemplateParser):
  def __init__(
      self,
      project : Project
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "./routes_page.js"
    out_file = "./routes.js"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
    )

    self.parse_file()

  def parse_file(self):
    for line in self.lines:

      if "$$CONTROLLERS$$" in line:
        insert = self.add_controller_declarations()
        self.out_lines = self.out_lines + insert

      elif "$$AUTH_CONTROLLER$$" in line and self.project.auth_object:
        self.out_lines.append("const AuthController = require('../controllers/authController');\n")

      elif "$$ROUTES$$" in line:
        insert = self.write_routes()
        self.out_lines = self.out_lines + insert

      elif "$$MIDDLEWARE_IMPORT$$" in line and self.project.auth_object:
        self.out_lines.append("const { verifyJWT } = require('./middlewares');\n")

      elif "$$AUTH_ROUTES$$" in line and self.project.auth_object:
        self.out_lines.append("// Auth\n")
        self.out_lines.append("router.post('/auth/login', AuthController.login);\n")
        self.out_lines.append("router.post('/auth/register', AuthController.register);\n\n")

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


  