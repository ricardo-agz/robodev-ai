from Logic.logic_block import LogicBlock

class ReturnBlock(LogicBlock):
  def __init__(
    self,
    status=200,
    variant="message",
    message="Success",
    data="data",
    tabs = 1
  ) -> None:
    self.status = status
    self.message = message
    self.variant = variant
    self.data = data
    self.tabs = tabs

    super().__init__(
      block_type="return",
      recursive=False
    )

  def print_block(self, tabs=None):
    tabs = self.tabs if not tabs else tabs
    if self.variant == "message":
      return f"{self.TAB_CHAR}"*tabs + f"return res.status({self.status}).send({{ message: {self.format_str(self.message)} }});\n"
    else:
      return f"{self.TAB_CHAR}"*tabs + f"return res.status({self.status}).send({self.data});\n"

    
