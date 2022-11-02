"""
"bcrypt": "^5.0.1",
"jsonwebtoken": "^8.5.1",
"""
import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
<<<<<<< HEAD
from TemplateParser.helpers import camel_case, pascal_case
=======
from TemplateParser.helpers import camel_case, pascal_case, extra_libraries_exist
>>>>>>> 63078ef11eced2c8e9b33e15177acfc21c71c6f3


class PackageJSONPage(TemplateParser):
  def __init__(
      self,
      project : Project,
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "./package_json_page.json"
    out_file = "./package.json"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
    )

    self.parse_file()
<<<<<<< HEAD
=======


>>>>>>> 63078ef11eced2c8e9b33e15177acfc21c71c6f3
