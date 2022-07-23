from Logic.logic_block import LogicBlock

class ErrorBlock(LogicBlock):
  def __init__(
    self,
    status=500,
    message="Server error...",
    tabs = 0
  ) -> None:
    self.status = status
    self.message = message
    self.tabs = tabs

    super().__init__(
      block_type="error",
      recursive=False
    )

  def print_block(self, tabs=None):
    tabs = self.tabs if not tabs else tabs
    return f"{self.TAB_CHAR}"*tabs + f"return res.status({self.status}).send({{ message: {self.format_str(self.message)} }});\n"

    
