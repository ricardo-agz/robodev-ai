from TemplateParser.Model import Model
from TemplateParser.Route import Route
from TemplateParser.helpers import camel_case, camel_to_dash, singularize

def val_in_tuple_arr(val, tup_arr):
  for (model_name, alias) in tup_arr:
    if val.lower() == model_name.lower():
      return True
  return False

class Project:
  """
  A class to represent a Neutrino project

  ...

  A project object holds a list of all Model objects 
  and is responsible for parsing their one-to-many and many-to-many relationships

  Attributes
  ----------
  project_name : str
    name of the project
  models : list[Model]
    list of all Model objects in project
  auth_object : Model
    model responsible for authenticaion (typically user)
  email : str
    email of user creating project
  server_port : int
    port to be used by express server
  mongostr : str
    mongoDB connection string
  styled : bool
    will the frontend be built with Material UI?
  """

  def __init__(
      self,
      project_name : str,
      models : list[Model],
      auth_object : str,
      email : str,
      server_port : int = 8080,
      mongostr : str = "<MONGO_CONNECTION_STRING>",
      styled : bool = True
    ) -> None:

    self.project_name = project_name
    self.models = models
    self.auth_object = self.model_from_name(auth_object)
    self.server_port = server_port
    self.link = f"http://localhost:3000/{server_port}"
    self.mongostr = mongostr
    self.email = email
    self.styled = styled
    self.set_relations()
    self.add_many_to_many_routes()


  def model_from_name(self, model_name):
    '''
    Returns matching Model object (if any) from given model_name
    '''
    for model in self.models:
      if model.name.lower() == model_name.strip().lower():
        return model

    raise Exception(f"{model_name} does not exist")

  def get_one_to_many_complement_alias(self, model, alias):
    """
    Returns compementary alias in one-to-many relationship
    ex. User has_many Post as "posts", Post belongs_to User as "author"
        get_complement_alias(user, "posts") -> "author"
    """
    # model passed is parent
    for child, a in model.one_to_many:
      if alias.lower() == a.lower():
        for parent_name, a2 in child.belongs_to:
          if parent_name.lower() == model.name.lower():
            return a2

    # model passed is child
    for parent_name, a in model.belongs_to:
      parent = self.model_from_name(parent_name)
      if alias.lower() == a.lower():
        for child, a2 in parent.one_to_many:
          if child.name.lower() == model.name.lower():
            return a2

    # relationship does not exist
    return None      

  def set_relations(self):
    '''
    Iterates through list of Models and updates their one_to_many and many_to_many lists
    '''

    '''
    Adding parent to model schema if it belongs to another model
    '''
    for model in self.models:
      if len(model.get_belongs_to()) > 0:
        for parent in model.get_belongs_to():
          parent_name = parent[0]
          alias = parent[1]
          new_param = {"name": parent_name, "type": "mongoose.Schema.Types.ObjectId", "required": True, "alias": alias}
          model.add_to_schema(new_param)

    for model in self.models:
      model_one_to_many = []
      model_many_to_many = []
      for (many_name, many_alias) in model.get_has_many():
        many_model = self.model_from_name(many_name)
        if not many_model:
          raise Exception(f"model: '{many_name}' does not exist")

        '''
        If model has many many_model and many_model belongs to model
        '''
        if many_model and model.does_have_many(many_model) and many_model.does_belong_to(model):
          model_one_to_many.append((many_model, many_alias))

        '''
        If model has many many_model and many_model has many model
        '''
        if model.does_have_many(many_model) and many_model.does_have_many(model):
          model_many_to_many.append((many_model, many_alias))

      model.set_one_to_many(model_one_to_many)
      model.set_many_to_many(model_many_to_many)

  def add_many_to_many_routes(self):
    for model in self.models:
      for (many_model, alias) in model.many_to_many:
        add_route_name = f"add{singularize(alias.title())}" if alias else f"add{many_model.name}"
        drop_route_name = f"drop{singularize(alias.title())}" if alias else f"add{many_model.name}"
        many_id = f"{camel_case(many_model.name)}Id"
        add_route = Route(
          name=add_route_name, 
          method="post", 
          path=f"/{model.plural.lower()}/:id/{camel_to_dash(add_route_name)}/:{many_id}",
          model=model
        )
        drop_route = Route(
          name=drop_route_name, 
          method="post", 
          path=f"/{model.plural.lower()}/:id/{camel_to_dash(drop_route_name)}/:{many_id}",
          model=model
        )
        model.add_route(add_route)
        model.add_route(drop_route)
