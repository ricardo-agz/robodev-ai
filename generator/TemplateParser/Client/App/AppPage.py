import os
from generator.TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.helpers import append_at_index, camel_case, pascal_case

class AppPage(TemplateParser):
  def __init__(
      self,
      project : Project
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "app_page.js"
    out_file = "./App.js"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
    )

    self.parse_file()

  def parse_file(self):
    for line in self.lines:
      name = self.project.auth_object.name if self.project.auth_object else None

      if "$$DYNAMIC_IMPORTS$$" in line:
        insert = self.add_dynamic_imports()
        self.out_lines = self.out_lines + insert

      elif "$$AUTH_IMPORTS$$" in line and self.project.auth_object:
        insert = self.add_auth_imports()
        self.out_lines = self.out_lines + insert

      elif "$$USE_FIND$$" in line and self.project.auth_object:
        self.out_lines.append(\
          f"\tconst {{ {camel_case(name)}, set{name}, loading }} = useFind{name}();\n\n")

      elif "$$CONTEXT_PROVIDER$$" in line and self.project.auth_object:
        new_lines = [
          f"\t\t<{name}Context.Provider\n",
          "\t\t\tvalue={{\n",
          f"\t\t\t\tauth{name}: {camel_case(name)},\n",
          f"\t\t\t\tsetAuth{name}: set{name},\n",
          f"\t\t\t\tauthLoading: loading\n",
          "\t\t\t}}>\n"
        ]
        self.out_lines += new_lines
        # self.out_lines.append(f"\t\t<{name}Context.Provider value={{{{ auth{name}: {camel_case(name)}, setAuth{name}: set{name}, authLoading: loading }}}}>\n")
      
      elif "$$NAV$$" in line:
        self.out_lines.append("\t\t\t<Nav/>\n")

      elif "$$AUTH_ROUTES$$" in line and self.project.auth_object:
        self.out_lines.append("\n\t\t\t\t{/* AUTH */}\n")
        self.out_lines.append("\t\t\t\t<Route path='/login' element={<Login />} />\n")
        self.out_lines.append(f"\t\t\t\t<Route path='/register' element={{<{name}New />}} />\n")

      elif "$$DYNAMIC_ROUTES$$" in line:
        insert = self.add_dynamic_routes()
        self.out_lines = self.out_lines + insert

      elif "$$CLOSE_CONTEXT_PROVIDER$$" in line and self.project.auth_object:
        self.out_lines.append(f"\t\t</{self.project.auth_object.name}Context.Provider>\n")

      else:
        self.out_lines.append(line)
        

  def add_dynamic_imports(self):
    """
    import { UserEdit, UserNew, Users, UserShow } from './Pages/User/index';
    """
    out = []
    for model in self.project.models:
      out.append("import { ")

      for i, route in enumerate(model.get_frontend_routes()):
        out.append(route.get_frontend_page_name())
        if i < (len(model.get_frontend_routes())-1):
          out.append(f", ")
        
      out.append(f" }} from './pages/{camel_case(model.name)}/index';\n")
    return out

  def add_auth_imports(self):
    insert = [
      f"import {{ {self.project.auth_object.name}Context }} from './hooks/{self.project.auth_object.name}Context';\n",
      f"import useFind{self.project.auth_object.name} from './hooks/useFind{self.project.auth_object.name}';\n",
      "import PrivateRoute from './auth/PrivateRoute';\n",
      "import Login from './auth/Login';\n",
      "import Nav from './components/Nav'\n"
    ]
    return insert

  def add_dynamic_routes(self):
    out = []
    for model in self.project.models:
      out.append(f"\n\t\t\t\t{{/* {model.name} */}}\n")
      for route in model.get_frontend_routes():
        out = out + route.get_frontend_page_component(model)

      for child_model, alias in model.one_to_many:
        out += f"\t\t\t\t<Route path='/{model.plural.lower()}/:id/{alias.lower()}/new' element={{<{child_model.name}New />}} />"
    return out

  