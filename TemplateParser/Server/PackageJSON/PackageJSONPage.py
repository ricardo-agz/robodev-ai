"""
"bcrypt": "^5.0.1",
"jsonwebtoken": "^8.5.1",
"""
import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.helpers import camel_case, pascal_case


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

  
  def get_auth_imports(self):
    """
    "bcrypt": "^5.0.1",
    "jsonwebtoken": "^8.5.1",
    """
    insert = [
      f'\t\t"bcrypt": "^5.0.1",\n',
      f'\t\t"jsonwebtoken": "^8.5.1",\n',
    ]
    return insert


  def parse_file(self):
    for line in self.lines:
      if "$$AUTH_IMPORTS" in line:
        insert = self.get_auth_imports()
        self.out_lines = self.out_lines + insert
      
      else:
        self.out_lines.append(line)
