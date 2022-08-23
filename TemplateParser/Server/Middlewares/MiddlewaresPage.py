import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.helpers import append_at_index

class MiddlewaresPage(TemplateParser):

  

  def __init__(
      self,
      project : Project
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "./middlewares_page.js"
    out_file = "./middlewares.js"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
    )
    self.parses_file()

    

  def parses_file(self):
   
    for line in self.lines:
      if "$$handler$$" in line:
        
        for middleware in self.project.middlewares:
          print(middleware.getContent())
          self.out_lines.append(middleware.getContent())
        

      elif "$$exports" in line:
          temp = ""
          for i, middleware in enumerate(self.project.middlewares):
            if (i != len(self.project.middlewares)) - 1:
              temp += "\t" + middleware.handler  + ",\n"
            else:
              temp += "\t" + middleware.handler + "\n"
          self.out_lines.append(temp)

      elif "$$" not in line:
        self.out_lines.append(line)
  


  


