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
    self.error_check_template()
    self.parse_embedded_code()
    self.init_parse_lines()


  def error_check_template(self):
    stack = []
    for line in self.lines:
      if "<$" in line and "$>" in line:
        func_str = line[line.find("<$")+2 : line.find("$>")].strip()

        if "begin" in func_str:
          if len(stack) != 0:
            raise Exception("<$ begin $> statement must be followed by an <$ end $>")
          
          if "if" in func_str:
            temp_line = func_str.split("if")
            condition = temp_line[1]
            try:
              eval(condition)
            except:
              raise Exception("Invalid conditional in <$ begin $> statement")

          stack.append("begin")

        elif "end" in func_str:
          if len(stack) != 1:
            raise Exception("Out of order <$ end $> statement")
          stack.pop()

    if len(stack) != 0:
      raise Exception("Unequal number of <$ begin $> and <$ end $> statements")


  def parse_embedded_code(self):
    blocks = []
    new_lines = []
    toggle_block = False
    conditional_met = True

    for i in range(len(self.lines)):
      line = self.lines[i]
      is_open_close = False

      # if <$ begin $>
      if "<$" in line and "$>" in line:
        func_str = line[line.find("<$")+2 : line.find("$>")].strip()

        # is opening or closing statement
        if "begin" in func_str or "end" in func_str:
          is_open_close = True

        if "begin" in func_str:
          toggle_block = True

          # if conditional
          if "if" in func_str:
            temp_line = func_str.split("if")
            condition = temp_line[1]
            conditional_met = eval(condition)

        elif "end" in func_str:
          toggle_block = False
          conditional_met = True

      if not toggle_block or (toggle_block and conditional_met):
        if not is_open_close:
          new_lines.append(line)

    self.lines = new_lines
    
    '''
    for i in range(len(self.lines)):
      line_i = self.lines[i]
      toggle_block = False

      # if <$ begin $>
      if "<$" in line_i and "$>" in line_i:
        func_str_i = line_i[line_i.find("<$")+2 : line_i.find("$>")].strip()
        if "begin" in func_str_i:
          toggle_block = True
          if "if" in func_str_i:
            temp_line = func_str_i.split("if")
            condition = temp_line[1]
          temp = []
          # continue until <$ end $>
          for j in range(i+1, len(self.lines)):
            line_j = self.lines[j]
            if "<$" in line_j and "$>" in line_j:
              func_str_j = line_j[line_j.find("<$")+2 : line_j.find("$>")].strip()
              if func_str_j == "end":
                toggle_block = False
                i = j
                break
            temp.append(line_j)
          blocks.append(temp)
    '''

    # print("end print embedded:")
    # print(blocks)
    # print("-----")



    # for i, line in enumerate(self.lines):
    #   if "<$=" in line and "$>" in line:
    #     func_str = line[line.find("<$=")+3 : line.find("$>")].strip()
    #     if func_str == "begin":
    #       for j in range()





  def close_files(self):
    self.in_f.close()
    self.out_f.close()


  def init_parse_lines(self):
    self.lines = [self.insert_var_in_line(line) for line in self.lines]


  def add_snip_dynamic(self, in_file, many_model=None, alias=None, custom_replacement:list[tuple]=None):
    in_file = open(os.path.join(self.__location__, in_file), "r")
    lines = in_file.readlines()
    in_file.close()

    # if custom replacement
    if custom_replacement:
      for custom, replacement in custom_replacement:
        for i in range(len(lines)):
          line = lines[i]
          if custom in line:
            line = line.replace(custom, replacement)
            # print(f"custom: {custom}, replacement: {replacement}")
            lines[i] = line
            # print(f"new line: {line}")

    return [self.insert_var_in_line(line, many_model, alias) for line in lines]
    
    
  def insert_var_in_line(self, line, many_model=None, alias=None):
    if self.model:
      name = self.model.name
    if many_model:
      many_name = many_model.name
    out = False

    if "$$EVAL=" in line:
      # print("eval here")
      func_str = line[line.find("$$EVAL=")+7:line.find("END$$")].strip()
      # print(eval(func_str))

    if "<$=" in line and "$>" in line:
      # print("new eval here")
      func_str = line[line.find("<$=")+3 : line.find("$>")].strip()
      evaluated = eval(func_str)
      # print(eval(func_str))
      new_line =  line[:line.find("<$=")+3] + evaluated + line[line.find("$>") :]
      new_line = new_line.replace("<$=", "").replace("$>", "")
      line = new_line

    if "$$name$$" in line:
      line = line.replace("$$name$$", name.lower())
      out = True
    if "$$nameCamel$$" in line:
      line = line.replace("$$nameCamel$$", camel_case(name))
      out = True
    if "$$pluralname$$" in line:
      line = line.replace("$$pluralname$$", self.model.plural.lower())
      out = True
    if "$$PluralName$$" in line:
      line = line.replace("$$PluralName$$", self.model.plural)
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
    if "$$manynames$$" in line:
      line = line.replace("$$manynames$$", many_model.plural.lower())
      out = True
    if "$$Alias$$" in line:
      line = line.replace("$$Alias$$", pascal_case(alias) if alias else many_name)
      out = True
    if "$$alias$$" in line:
      line = line.replace("$$alias$$", alias.lower() if alias else many_name.lower())
      out = True
    if "$$aliasCamel$$" in line:
      line = line.replace("$$aliasCamel$$", camel_case(alias) if alias else camel_case(many_name))
      out = True
    if "$$SingleAlias$$" in line:
      line = line.replace("$$SingleAlias$$", pascal_case(singularize(alias)) if alias else many_name)
      out = True
    if "$$singleAlias$$" in line:
      line = line.replace("$$singleAlias$$", singularize(alias).lower() if alias else many_name.lower())
      out = True
    if "$$singleAliasCamel$$" in line:
      line = line.replace("$$singleAliasCamel$$", camel_case(singularize(alias)) if alias else camel_case(many_name))
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
