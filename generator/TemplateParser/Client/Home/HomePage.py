import os
from generator.TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.helpers import append_at_index, camel_case, pascal_case, singularize

class HomePage(TemplateParser):
  def __init__(
      self,
      project : Project,
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "home_page.js"
    out_file = f"./Home.js"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
    )

    self.parse_file()