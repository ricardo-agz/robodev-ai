import os
from TemplateParser.Project import Project
from TemplateParser.helpers import camel_case, pascal_case, singularize, title_space_case, pluralize

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

        elif "for " in func_str and " in " in func_str:
          var_name = line[line.find("for ")+4 : line.find(" in")].strip()
          array = line[line.find(" in ")+4 : line.find("$>")].strip()

          if len(stack) > 0 and stack[-1] == "for":
            raise Exception("Nested for loops not yet supported")
          if not var_name.isalnum() and "," not in var_name:
            raise Exception("Invalid iterable name")
          try:
            eval(array)
          except:
            raise Exception("Invalid array declaration")

          stack.append("for")

        elif "end" in func_str:
          stack.pop()

    if len(stack) != 0:
      raise Exception("Unequal number of open and close statements")


  def parse_embedded_code(self):
    new_lines = []
    toggle_block = False
    conditional_met = True
    stack = []
    skip_lines = []

    for i in range(len(self.lines)):
      line = self.lines[i]
      is_open_close = False

      # if <$ begin $>
      if "<$" in line and "$>" in line:
        func_str = line[line.find("<$")+2 : line.find("$>")].strip()

        # is opening or closing statement
        if "begin" in func_str or "end" in func_str or ("for " in func_str and " in " in func_str):
          is_open_close = True

        if "begin" in func_str:
          stack.append("begin")
          toggle_block = True

          # if conditional
          if "if" in func_str:
            temp_line = func_str.split("if")
            condition = temp_line[1]
            conditional_met = eval(condition)

        # embedded for loop
        if "for " in func_str and " in " in func_str:
          stack.append("for")
          toggle_block = True
          var_name = line[line.find("for ")+4 : line.find(" in")].strip()
          array = line[line.find(" in ")+4 : line.find("$>")].strip()
          eval_arr = eval(array)
          block = []
          split_name = False

          # for one, two in array
          if "," in var_name:
            temp = var_name.split(",")
            var1 = temp[0].strip()
            var2 = temp[1].strip()
            split_name = True

          # add line to block until reaching <$ end $>
          j = i+1
          line_j = self.lines[j]
          while not ("<$" in line_j and "end" in line_j and "$>" in line_j):
            # replace variable names with array at index
            if split_name:
              line_j = line_j.replace(var1, f"{array}[i][0]").replace(var2, f"{array}[i][1]")
            else:
              line_j = line_j.replace(var_name, f"{array}[i]")
            block.append(line_j)
            skip_lines.append(j)
            j+=1
            line_j = self.lines[j]

          # must replace [i] index with actual index
          for x in range(len(eval_arr)):
            new_block = [block_line
                          .replace("[i]", f"[{x}]")
                          .replace("_index_", f"{x}")
                          .replace("_len_", f"{len(eval_arr)}") 
                          for block_line in block]

            # insert in-line python injections 
            for b_index in range(len(new_block)):
              block_line = new_block[b_index]
              # injection block
              if "<$=" in block_line and "$>" in block_line:
                func_str = block_line[block_line.find("<$=")+3 : block_line.find("$>")].strip()
                # evaluate and replace
                evaluated = eval(func_str)
                temp_line =  block_line[:block_line.find("<$=")+3] + evaluated + block_line[block_line.find("$>") :]
                temp_line = temp_line.replace("<$=", "").replace("$>", "")
                new_block[b_index] = temp_line

            new_lines = new_lines + new_block
                    
        elif "end" in func_str:
          toggle_block = False
          conditional_met = True

      if not toggle_block or (toggle_block and conditional_met):
        if not is_open_close and i not in skip_lines:
          new_lines.append(line)

    self.lines = new_lines



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

    # python injection block
    if "<$=" in line and "$>" in line:
      func_str = line[line.find("<$=")+3 : line.find("$>")].strip()
      evaluated = eval(func_str)
      new_line =  line[:line.find("<$=")+3] + evaluated + line[line.find("$>") :]
      new_line = new_line.replace("<$=", "").replace("$>", "")
      line = new_line
      
    if "<$#" in line and "$>" in line:
      return ""

    if "<!--" in line and "-->" in line:
      return ""

    if "$$name$$" in line:
      line = line.replace("$$name$$", name.lower())
      out = True
    if "$$nameCamel$$" in line:
      line = line.replace("$$nameCamel$$", camel_case(name))
      out = True
    if "$$pluralname$$" in line:
      line = line.replace("$$pluralname$$", self.model.plural.lower())
      out = True
    if "$$names$$" in line:
      line = line.replace("$$names$$", self.model.plural.lower())
      out = True
    if "$$PluralName$$" in line:
      line = line.replace("$$PluralName$$", self.model.plural)
      out = True
    if "$$pluralName$$" in line:
      line = line.replace("$$pluralName$$", camel_case(self.model.plural))
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

  def to_string(self):
    out_str = ""
    for line in self.out_lines:
      if "$$" not in line:
        out_str += line.replace("\t", "  ")
    return out_str
