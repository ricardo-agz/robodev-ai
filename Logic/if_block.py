from Logic.logic_block import LogicBlock

class IfBlock(LogicBlock):
  def __init__(
    self,
    condition = "true",
    success = [],
    error = [],
    tabs = 1
  ) -> None:
    self.condition = condition
    self.tabs = tabs
    self.success = success
    self.error = error

    super().__init__(
      block_type="conditional",
      recursive=True
    )

  def print_block(self, tabs=None):
    tabs = self.tabs if not tabs else tabs

    out_str = f"{self.TAB_CHAR*tabs}" + f"if ({self.condition}) {{\n"
    success_str = self.recurse_success(tabs)
    error_str = self.recurse_error(tabs)

    if len(self.error) > 0:
      out_str += success_str + f"{self.TAB_CHAR*tabs}" + "} else {\n"
    out_str += error_str + f"{self.TAB_CHAR*tabs}}};"

    return out_str

    
