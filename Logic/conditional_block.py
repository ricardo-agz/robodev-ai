from Logic.logic_block import LogicBlock

class ConditionalBlock(LogicBlock):
  def __init__(
    self,
    condition=None,
    success = [],
    error = [],
  ) -> None:
    self.condition = "true" if not condition else condition
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

    out_str += success_str + f"{self.TAB_CHAR*tabs}}}"
    if len(self.error) > 0:
      out_str +=  " else {\n" + error_str + f"{self.TAB_CHAR*tabs}}};\n"
    else:
      out_str += "\n"

    return out_str

    
