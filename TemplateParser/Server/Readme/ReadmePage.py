import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.helpers import camel_case, pascal_case


class ReadmePage(TemplateParser):
  def __init__(
      self,
      project : Project,
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "./readme.md"
    out_file = f"./README.md"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
    )

    self.parse_file()

  
  def add_auth_description(self):
    """
    """
    insert = [
      f"## Auth\n",
    ]
    return insert


  def parse_file(self):
    for line in self.lines:

      #----- MODEL RELATIONSHIPS -----
      if "$$AUTH_DESCRIPTION$$" in line and self.project.auth_object:
        insert = self.add_auth_description()
        self.out_lines = self.out_lines + insert
      
      else:
        self.out_lines.append(line)


  