class Route:
  def __init__(
      self,
      name,
      method,
      path,
      model,
      middleware = None,
      disabled = False,
      protected = False,
      logic = "",
      pagination = False,
      alias = None
    ) -> None:

      self.name = name
      self.method = method
      self.path = path
      self.model = model
      self.middleware = middleware
      self.disabled = disabled
      self.protected = protected
      self.logic = logic
      self.pagination = pagination
      self.alias = alias

  def get_logic(self):
    return self.logic

  def get_route_call(self):
    """
    app.get('/users/:id', verifyJWT, UserController.find)
    """
    middleware = f", {middleware}" if self.middleware else ""
    return f"app.{self.method.lower()}('{self.path}'{middleware}, {self.model.name}Controller.{self.name}());\n"
