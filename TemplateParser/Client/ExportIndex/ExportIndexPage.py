import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.helpers import append_at_index, camel_case

class ExportIndexPage(TemplateParser):
  def __init__(
      self,
      project : Project,
      model : Model
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "./export_index_page.js.enp"
    out_file = f"./index.js"

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

      if "$$EXPORTS$$" in line:
        for route in self.model.get_frontend_routes():
          self.out_lines.append(f"export {{ default as {route.get_frontend_page_name()} }} from './{route.get_frontend_page_name()}';\n")

      else:
        self.out_lines.append(line)
        