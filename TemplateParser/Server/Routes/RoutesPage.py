import os
from TemplateParser.Middleware import Middleware
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.helpers import append_at_index, camel_case

class RoutesPage(TemplateParser):
  def __init__(
      self,
      project : Project,
      is_preview = False
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
      is_preview=is_preview
    )

    self.parse_file()

  def parse_file(self):
    for line in self.lines:

      if "$$CONTROLLERS$$" in line:
        insert = self.add_controller_declarations()
        self.out_lines = self.out_lines + insert

      elif "$$ROUTES$$" in line:
        insert = self.write_routes()
        self.out_lines = self.out_lines + insert

      elif "$$MIDDLEWARE_IMPORT$$" in line:
        import_str = ""
        for i,middleware in enumerate(self.project.middlewares):
          if i != len(self.project.middlewares) - 1:
            import_str += middleware.handler + ", "
          else:
            import_str += middleware.handler

        self.out_lines.append("const { " + import_str + " } = require('./middlewares');\n")

      else:
        self.out_lines.append(line)
        

  def add_controller_declarations(self):
      """
      Writes import statements for all controllers in project
      Ex.
      const UserController = require('./controllers/UserController');
      const CourseController = require('./controllers/CourseController');
      """
      out = []
      for controller in self.project.controllers:
        out.append(f"const {controller.name}Controller = require('../controllers/{controller.name}Controller');\n")
      return out


  def write_routes(self):
    """
    Writes route endpoints for all routes in all controllers in project
    Ex.
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


  