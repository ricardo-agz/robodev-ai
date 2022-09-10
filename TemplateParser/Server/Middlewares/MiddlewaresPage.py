import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.helpers import append_at_index, import_generator

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
      if "$$imports$$" in line:
        #const jwt = require("jsonwebtoken");
        #const User = require('../models/user');
        logic = []
        for middleware in self.project.middlewares:
          logic= logic + middleware.logic
        import_statements = import_generator(logic)
        self.out_lines.append(import_statements)
        

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
  


  


