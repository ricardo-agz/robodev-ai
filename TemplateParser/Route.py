from Logic.interact import json_to_formatted_code

class Route:
  #  controller_id = route["controller"],
  #       id = route["id"],
  #       url = route["url"],
  #       handler = route["handler"],
  #       verb = route["verb"],
  #       logic = route["logic"],
  #       middleware=route["middleware"]
  def __init__(
      self,
      controller_id = None,
      controller_name=None,
      id = None,
      url = None,
      handler = None,
      verb = None,
      logic = [],
      middleware = None,
      disabled = False,
      protected = False,
      pagination = False,
      alias = None
    ) -> None:

      self.controller_id = controller_id
      self.controller_name = controller_name
      self.id = id
      self.url = url
      self.handler = handler
      self.verb = verb
      self.middleware = middleware
      self.disabled = disabled
      self.protected = protected
      self.logic = logic
      self.pagination = pagination
      self.alias = alias

      if self.logic != "":
        print(f"THIS ROUTE HAS LOGIC: {self.logic}")

  def get_logic(self):
    return self.logic

  def get_route_call(self):
    """
    router.get('/users/:id', verifyJWT, UserController.find)
    """
    middleware = f", {self.middleware}" if self.middleware else ""
    return f"router.{self.verb.lower()}('{self.url}'{middleware}, {self.controller_name}Controller.{self.handler});\n"

  def get_handler_function(self):
    func = f'\t{self.handler}: async (req, res)' + "=> {\n"
    logic = json_to_formatted_code(self.logic)
    for line in logic.split("\n"):
      if (line != ""):
        func += "\t" + line + "\n"
    func += "\t},\n"
    return func




  # def get_frontend_page_name(self) -> list[str]:
  #   if self.name == "index":
  #     return f"{self.model.plural}"
  #   elif self.name == "show":
  #     return f"{self.model.name}Show"
  #   elif self.name == "create":
  #     return f"{self.model.name}New"
  #   elif self.name == "update":
  #     return f"{self.model.name}Edit"

  # def get_frontend_page_component(self, model) -> list[str]:
  #   out = []
  #   tabs = "\t\t\t\t"
  #   if self.protected:
  #     out.append(f"{tabs}<Route\n")
  #     if self.name == "index":
  #       out.append(f"{tabs}\tpath='/{model.plural.lower()}'\n")
  #       out.append(f"{tabs}\telement={{ <PrivateRoute component={{<{model.plural} />}} />}}\n")
  #       out.append(f"{tabs}/>\n")
  #     elif self.name == "show":
  #       out.append(f"{tabs}\tpath='/{model.plural.lower()}/:id'\n")
  #       out.append(f"{tabs}\telement={{ <PrivateRoute component={{<{model.name}Show />}} />}}\n")
  #       out.append(f"{tabs}/>\n")
  #     elif self.name == "create":
  #       out.append(f"{tabs}\tpath='/{model.plural.lower()}/new'\n")
  #       out.append(f"{tabs}\telement={{ <PrivateRoute component={{<{model.name}New />}} />}}\n")
  #       out.append(f"{tabs}/>\n")
  #     elif self.name == "update":
  #       out.append(f"{tabs}\tpath='/{model.plural.lower()}/:id/edit'\n")
  #       out.append(f"{tabs}\telement={{ <PrivateRoute component={{<{model.name}Edit />}} />}}\n")
  #       out.append(f"{tabs}/>\n")

  #   else:
  #     if self.name == "index":
  #       out.append(f"{tabs}<Route path='/{model.plural.lower()}' element={{<{model.plural} />}} />\n")
  #     elif self.name == "show":
  #       out.append(f"{tabs}<Route path='/{model.plural.lower()}/:id' element={{<{model.name}Show />}} />\n")
  #     elif self.name == "create":
  #       out.append(f"{tabs}<Route path='/{model.plural.lower()}/new' element={{<{model.name}New />}} />\n")
  #     elif self.name == "update":
  #       out.append(f"{tabs}<Route path='/{model.plural.lower()}/:id/edit' element={{<{model.name}Edit />}} />\n")

  #   return out
