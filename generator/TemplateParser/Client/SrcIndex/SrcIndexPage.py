import os
from generator.TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project


class SrcIndexPage(TemplateParser):
  def __init__(
      self,
      project : Project,
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "src_index_page.js"
    out_file = f"./index.js"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
    )

    self.parse_file()