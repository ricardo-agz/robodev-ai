from Logic.interact import json_to_formatted_code


class Middleware:

  def __init__(
      self,
       id,
      handler,
      logic
    ) -> None:
      self.id = id
      self.handler = handler
      self.logic = logic

  def getContent (self):

    out_str = 'const ' +  self.handler + " = (req, res, next) => {\n"
    code = json_to_formatted_code(self.logic)
    for line in code.split("\n"):
        out_str += "\t" + line
    out_str += "\n}"
    return out_str

      
    
 

