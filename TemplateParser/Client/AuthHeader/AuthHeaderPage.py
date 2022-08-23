import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.helpers import camel_case, pascal_case


class AuthHeaderPage(TemplateParser):
  def __init__(
      self,
      project : Project
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "./auth-header.js"
    out_file = f"./auth-header.js"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project
    )

    self.parse_file()