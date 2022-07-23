from Logic.logic_block import LogicBlock

class QueryBlock(LogicBlock):
  def __init__(
    self,
    model,
    params = "{}",
    var_name = "data",
    variant = "one",
    tabs = 1
  ) -> None:
    self.model = model
    self.variant = variant
    self.params = params
    self.var_name = var_name
    self.tabs = tabs

    super().__init__(
      block_type="query",
      recursive=False
    )

#{'id': ':r2:19096531', 'blockVariant': 'query', 'varName': 'data', 'params': '{}', 'model': 'User', 'multiple': True}

  def print_block(self, tabs=None):
    tabs = self.tabs if not tabs else tabs
    if "_id" in self.params:
      query = "findById"
      return f"{self.TAB_CHAR*tabs}" + f"const {self.var_name.lower()} = await {self.model}.{query}(id);\n"
    elif self.variant == "many":
      query = "find"
      return f"{self.TAB_CHAR*tabs}" + f"const {self.var_name.lower()} = await {self.model}.{query}({self.params});\n"
    else:
      query = "findOne"
      return f"{self.TAB_CHAR*tabs}" + f"const {self.var_name.lower()} = await {self.model}.{query}({self.params});\n"

    
