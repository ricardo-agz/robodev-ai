from Logic.logic_block import LogicBlock

class ErrorBlock(LogicBlock):
  def __init__(
    self,
    status=None,
    message=None,
    tabs = 1
  ) -> None:
    self.status = 500 if not status else status
    self.message = "Server error..." if not message else message
    self.tabs = tabs

    super().__init__(
      block_type="error",
      recursive=False
    )

  def print_block(self, tabs=None):
    tabs = self.tabs if not tabs else tabs
    return f"{self.TAB_CHAR}"*tabs + f"return res.status({self.status}).send({{ message: {self.format_str(self.message)} }});\n"

    
