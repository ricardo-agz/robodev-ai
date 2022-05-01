import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.helpers import append_at_index, camel_case

class UseFindPage(TemplateParser):
  def __init__(
      self,
      project : Project,
      auth_model : Model
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "./use_find_page.js"
    out_file = f"./useFind{auth_model.name}.js"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
      model = auth_model
    )

    self.parse_file()
        

  