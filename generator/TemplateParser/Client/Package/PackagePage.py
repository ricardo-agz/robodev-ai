import os
from generator.TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.helpers import camel_case, pascal_case


class ClientPackagePage(TemplateParser):
  def __init__(
      self,
      project : Project
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "package_page.json"
    out_file = f"./package.json"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project
    )

    self.parse_file()



  