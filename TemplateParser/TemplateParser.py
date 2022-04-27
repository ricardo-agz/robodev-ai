import os
from TemplateParser.Project import Project
from TemplateParser.helpers import camel_case, pascal_case, singularize

class TemplateParser:

  def __init__(
                self, 
                in_file, 
                out_file,
                __location__,
                project,
                model=None,
                alias=None,
                many_model=None
              ):
    self.in_f = open(os.path.join(__location__, in_file), "r")
    self.out_f = open(out_file, "w")
    self.__location__ = __location__
    self.lines = self.in_f.readlines()
    self.out_lines = []
    self.project = project
    self.model = model
    self.alias = alias
    self.many_model = many_model
    self.init_parse_lines()


  def close_files(self):
    self.in_f.close()
    self.out_f.close()


  def init_parse_lines(self):
    self.lines = [self.insert_var_in_line(line) for line in self.lines]


  def add_snip_dynamic(self, in_file, many_model=None, alias=None):
    in_file = open(os.path.join(self.__location__, in_file), "r")
    lines = in_file.readlines()
    in_file.close()
    return [self.insert_var_in_line(line, many_model, alias) for line in lines]
    
    
  def insert_var_in_line(self, line, many_model=None, alias=None):
    if self.model:
      name = self.model.name
    if many_model:
      many_name = many_model.name
    out = False

    if "$$name$$" in line:
      line = line.replace("$$name$$", name.lower())
      out = True
    if "$$Name$$" in line:
      line = line.replace("$$Name$$", name)
      out = True
    if "$$ManyName$$" in line:
      line = line.replace("$$ManyName$$", many_name)
      out = True
    if "$$manyname$$" in line:
      line = line.replace("$$manyname$$", many_name.lower())
      out = True
    if "$$Alias$$" in line:
      line = line.replace("$$Alias$$", pascal_case(alias) if alias else many_name)
      out = True
    if "$$alias$$" in line:
      line = line.replace("$$alias$$", alias.lower() if alias else many_name.lower())
      out = True
    if "$$SingleAlias$$" in line:
      line = line.replace("$$SingleAlias$$", pascal_case(singularize(alias)) if alias else many_name)
      out = True
    if "$$singleAlias$$" in line:
      line = line.replace("$$singleAlias$$", singularize(alias).lower() if alias else many_name.lower())
      out = True
    if "$$header$$" in line:
      if self.project.auth_object:
        line = line.replace("$$header$$", ", { headers: authHeader() }")
        out = True
      else:
        line = line.replace("$$header$$", "")
        out=True
    if "$$mmheader$$" in line:
      if self.project.auth_object:
        line = line.replace("$$mmheader$$", ",\n\t\t\t\t{}, { headers: authHeader() }")
        out = True
      else:
        line = line.replace("$$mmheader$$", "")
        out=True
    if "$$LINK$$" in line:
      line = line.replace("$$LINK$$", self.project.link)
      out = True
    if "$$PORT$$" in line:
      line = line.replace("$$PORT$$", str(self.project.server_port))
      out = True
    if "$$MONGOSTR$$" in line:
      line = line.replace("$$MONGOSTR$$", self.project.mongostr)
      out = True

    return line


  def parse_file(self):
    self.out_lines = [line for line in self.lines]

  def write_out_file(self):
    for line in self.out_lines:
      if "$$" not in line:
        self.out_f.write(line)
