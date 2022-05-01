import inflect
from TemplateParser.Route import Route
from TemplateParser.helpers import camel_case, pascal_case, pluralize, singularize

inflectEngine = inflect.engine()

def val_in_dic_arr(val, dic_arr):
  val_list = [val for elem in dic_arr for val in elem.values()]
  return val in val_list or val.lower() in val_list

def val_in_tuple_arr(val, tup_arr):
  for (model_name, alias) in tup_arr:
    if val.lower() == model_name.lower():
      return True
  return False


class Model:
  """
  A class to represent a Model (i.e user, post, comment, etc.)

  ...

  A model (as in model from MVC architecture) represents a data structure
  responsible for some sort of core functionality of a web application.
  Typically this refers to simply its database schema but here, model also
  contains routes, route logic, and relationships (one-to-many, many-to-many, etc.)

  Attributes
  ----------
  name : str
    name of model
  schema : list[{'name': 'name', 'type': 'String', 'required': True}]
    all model parameters (i.e. user has name, username, etc.)
  has_many : list[(many_name, alias)]
    model relationships specifications, i.e user has many post(many_name) 
    as articles(alias)
  belongs_to : list[(parent_name, alias)]
    model relationship specifying parent model, i.e. post belongs to user
  one_to_many : list[(Model, alias)]
    parsed model relationships where modelA has many modelBs and modelB 
    belongs to modelA (ex user and post)
  many_to_many : list[(Model, alias)]
    parsed model relationship where modelA has many modelBs and modelB 
    has many modelAs (ex. user and course)
  self_many : list[str]
    list of aliases. Parsed model relationship where modelA has many of 
    itself (ex. user has many users as 'friends')
  """

  def __init__(
                self,
                name : str,
                schema,
                routes = None,
                has_many = [],
                belongs_to = [],
                auth = False
              ) -> None:

    self.name = pascal_case(name.strip())
    self.plural = pluralize(self.name)
    self.schema = schema
    self.has_many = [tuple(x) for x in has_many]
    self.belongs_to = [tuple(x) for x in belongs_to]
    self.one_to_many = []
    self.many_to_many = []
    self.self_many = self.set_self_referencing()
    self.routes = routes if routes else self.init_default_routes()
    self.auth = auth

    
  def get_display_params(self):
    out = ""
    for param in self.schema:
      if param['type'] == "String" or param['type'] == "Number" or param['type'] == "Boolean":
        out += param['name'] + " "
    return out.strip()

  def init_default_routes(self):
    index = Route("index", "get", f"/{self.plural.lower()}", self)
    show = Route("show", "get", f"/{self.name.lower()}/:id", self)
    create = Route("create", "post", f"/{self.plural.lower()}", self)
    update = Route("update", "put", f"/{self.name.lower()}/:id/edit", self)
    destroy = Route("destroy", "delete", f"/{self.name.lower()}/:id", self)

    return [index, show, create, update, destroy]

  def add_route(self, route):
    if not type(route) == Route:
      raise Exception("route is not a Route object")
    self.routes.append(route)

  def set_routes(self, routes):
    self.routes = routes

  def add_to_schema(self, param):
    """
    used to parent model parameter 
    ex. {"name": parent_name, "type": "mongoose.Schema.Types.ObjectId", "required": True, "alias": alias}
    """
    if not('name' in param and 'type' in param and 'required' in param):
      raise Exception("Invalid param: must have field 'name', 'type', and 'required'")
      
    self.schema.append(param)

  def does_belong_to(self, other_model):
    """
    returns true if model belongs to other_model 
    ex. post.does_belong_to(user) -> True
    """
    if type(other_model) is str:
      return val_in_tuple_arr(other_model, self.belongs_to)

    for (parent_name, alias) in self.belongs_to:
      if parent_name.lower() == other_model.name.lower():
        return True
        
    return False

  def does_belong_to_aliased(self, other_model, alias):
    return (other_model, alias) in self.belongs_to
    
  def does_have_many(self, other_model):
    """
    returns true if model has many of other_model 
    ex. user.does_have_many(post) -> True
    """
    if type(other_model) is str:
      return val_in_tuple_arr(other_model, self.has_many)

    for (many_name, alias) in self.has_many:
      if many_name.lower() == other_model.name.lower():
        return True

    return False

  def does_have_many_aliased(self, other_model, alias):
    pass

  # SETTERS
  def set_one_to_many(self, one_to_many_list):
    self.one_to_many = one_to_many_list

  def set_many_to_many(self, many_to_many_list):
    self.many_to_many = many_to_many_list

  def set_self_referencing(self):
    """
    initialized model's self referencing many-to-many relationship list
    ex. if user has many users as 'friends', 'friends' would be added to list
    """
    # self_referencing = [alias1, alias2, ...]
    self_referencing = []
    for (many_name, many_alias) in self.has_many:
      if many_name.lower() == self.name.lower():
        self_referencing.append(many_alias)

    return self_referencing

  # GETTERS

  def get_frontend_routes(self) -> list[Route]:
    out = []
    for route in self.routes:
      if route.name == "index" or route.name == "show" or \
        route.name == "create" or route.name == "update":
        out.append(route)
    return out

  def get_params(self):
    return self.schema

  def get_has_many(self):
    return self.has_many

  def get_belongs_to(self):
    return self.belongs_to

  def get_one_to_many(self):
    return self.one_to_many

  def get_many_to_many(self):
    return self.many_to_many

  def get_self_referencing(self):
    return self.self_many

  def get_routes(self):
    return self.routes
