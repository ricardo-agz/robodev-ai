import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.helpers import append_at_index, camel_case

class UseAuthPage(TemplateParser):
  def __init__(
      self,
      project : Project,
      auth_model : Model
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "./use_auth_page.js"
    out_file = "./useAuth.js"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
      model = auth_model
    )

    self.parse_file()

  def parse_file(self):
    for line in self.lines:

      if "$$DECLARE_REGISTER_DATA$$" in line:
        post_str = "\t\tconst { "
        for i, param in enumerate(self.model.schema):
          post_str += f"{param['name']}{', ' if i < len(self.model.schema)-1 else ''}"
        post_str += " } = data;\n"
        self.out_lines.append(post_str)

      if "$$REGISTER_DATA$$" in line:
        post_str = "\t\t\t"
        for i, param in enumerate(self.model.schema):
          post_str += f"{param['name']}{', ' if i < len(self.model.schema)-1 else ''}"
        post_str += "\n"
        self.out_lines.append(post_str)

      else:
        self.out_lines.append(line)
        

  