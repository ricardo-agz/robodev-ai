class Controller:

  def __init__(
      self,
      name,
      id,
      model_affiliation,
      routes = [],
    ) -> None:
      self.name = name
      self.id = id
      self.model_affiliation = model_affiliation
      self.routes = []
      self.models = self.list_models()

  def addRoutes(self, route):
    self.routes.append(route)
    self.models = self.models | self.list_models()
    
  def list_models(self):
    model_list = {}
    for route in self.routes:
      for block in route.logic:
        if "model" in block:
          model_list[block["model"]] = 1
    return model_list


