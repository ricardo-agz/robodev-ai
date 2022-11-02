import os
<<<<<<< HEAD
=======
from TemplateParser.Middleware import Middleware
>>>>>>> 63078ef11eced2c8e9b33e15177acfc21c71c6f3
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.helpers import append_at_index, camel_case

class RoutesPage(TemplateParser):
  def __init__(
      self,
<<<<<<< HEAD
      project : Project
=======
      project : Project,
      is_preview = False
>>>>>>> 63078ef11eced2c8e9b33e15177acfc21c71c6f3
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
<<<<<<< HEAD
=======
      is_preview=is_preview
>>>>>>> 63078ef11eced2c8e9b33e15177acfc21c71c6f3
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

<<<<<<< HEAD
      elif "$$MIDDLEWARE_IMPORT$$" in line and self.project.auth_object:
        self.out_lines.append("const { verifyJWT } = require('./middlewares');\n")
=======
      elif "$$MIDDLEWARE_IMPORT$$" in line:
        import_str = ""
        for i,middleware in enumerate(self.project.middlewares):
          if i != len(self.project.middlewares) - 1:
            import_str += middleware.handler + ", "
          else:
            import_str += middleware.handler

        self.out_lines.append("const { " + import_str + " } = require('./middlewares');\n")
>>>>>>> 63078ef11eced2c8e9b33e15177acfc21c71c6f3

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
<<<<<<< HEAD
        out.append(f"const {controller.name}Controller = require('./controllers/{controller.name}Controller');\n")
=======
        out.append(f"const {controller.name}Controller = require('../controllers/{controller.name}Controller');\n")
>>>>>>> 63078ef11eced2c8e9b33e15177acfc21c71c6f3
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


  