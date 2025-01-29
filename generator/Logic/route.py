class Route:
  def __init__(
    self,
    controller,
    url,
    method
  ):
    self.controller = controller
    self.url = url
    self.method = method
    