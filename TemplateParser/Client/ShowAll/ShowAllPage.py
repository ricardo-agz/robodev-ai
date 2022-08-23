import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.helpers import append_at_index, camel_case

class ShowAllPage(TemplateParser):
  def __init__(
      self,
      project : Project,
      model : Model
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "./show_all_page.js"
    out_file = f"./{model.plural}.js"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
      model
    )

    self.parse_file()

  def parse_file(self):
    for line in self.lines:

      if "$$AUTH_IMPORTS$$" in line and self.project.auth_object:
        self.out_lines.append("import authHeader from '../../services/auth-header';\n")

      elif "$$DYNAMIC_PARAMS$$" in line and self.project.auth_object:
        self.out_lines.append(f"\t\t\t\t\t\t<li key={{i}}>{{{camel_case(self.model.name)}.{self.model.schema[0]['name']}}}</li>\n")

      else:
        self.out_lines.append(line)
        