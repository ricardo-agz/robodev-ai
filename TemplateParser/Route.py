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
        pass

  def get_logic(self):
    return self.logic

  def get_route_call(self):
    """
    router.get('/users/:id', verifyJWT, UserController.find)
    """
    middleware = f", " + ",".join(self.middleware) if len(self.middleware) != 0 else ""
    return f"router.{self.verb.lower()}('{self.url}'{middleware}, {self.controller_name}Controller.{self.handler});\n"
  
  def get_params_from_url(self):
    temp = self.url.split('/')
    out = [x.replace(":", "") for x in temp if ":" in x]
    return out

  def get_param_declaration(self):
    params = self.get_params_from_url()
    param_str = ""

    for i, p in enumerate(params):
      param_str += p
      param_str += ", " if i != len(params)-1 else ""
    out = f"const {{ {param_str} }} = req.params;"

    if len(params) > 0:
    	return out			
    return ""

  def get_handler_function(self):
    # header comment
    url_params = self.get_params_from_url()
    params_comment =  f" * params: {url_params}\n\t" if len(url_params) > 0 else ""
    func = f'\t/*\n\t * {self.handler}\n\t * url: {self.url}\n\t{params_comment} */\n'
    # declaration
    func += f'\t{self.handler}: async (req, res)' + " => {\n"
    func += "\t\ttry {\n"
    func += f"\t\t\t{self.get_param_declaration()}\n" if len(url_params) > 0 else ""
    logic = json_to_formatted_code(self.logic)
    for line in logic.split("\n"):
      if (line != ""):
        func += "\t" + line + "\n"
    func += "\t\t} catch(e) {\n"
    func += f"\t\t\tres.status(500).send({{ message: `server error in {self.controller_name}Controller {self.handler}() : ${{e}}` }});\n"
    func += "\t\t};\n"
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
