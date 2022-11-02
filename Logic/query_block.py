from Logic.logic_block import LogicBlock

class QueryBlock(LogicBlock):
  def __init__(
    self,
    model,
    params=None,
    var_name=None,
    populate=None,
    variant="one",
  ) -> None:
    self.model = model
    self.variant = variant
    self.populate = populate
    self.params = "{ }" if not params else params
    self.var_name = "data" if not var_name else var_name

    super().__init__(
      block_type="query",
      recursive=False
    )

#{'id': ':r2:19096531', 'blockVariant': 'query', 'varName': 'data', 'params': '{}', 'model': 'User', 'multiple': True}

  def print_block(self, tabs=None):
    tabs = self.tabs if not tabs else tabs
    populate_str = ";" if not self.populate else f"{self.TAB_CHAR * tabs+1}.populate{self.populate};\n"

    if "_id" in self.params:
      query = "findById"
      return f"{self.TAB_CHAR*tabs}" + f"const {self.var_name.lower()} = await {self.model}.{query}(id){populate_str}\n"
    elif self.variant == "many":
      query = "find"
      return f"{self.TAB_CHAR*tabs}" + f"const {self.var_name.lower()} = await {self.model}.{query}({self.params}){populate_str}\n"
    else:
      query = "findOne"
      return f"{self.TAB_CHAR*tabs}" + f"const {self.var_name.lower()} = await {self.model}.{query}({self.params}){populate_str}\n"

    
