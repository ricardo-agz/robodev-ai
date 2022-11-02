from Logic.logic_block import LogicBlock

class ReturnBlock(LogicBlock):
  def __init__(
    self,
    status=None,
    data=None,
    return_content=None,
  ) -> None:
    self.status = 200 if not status else status
    self.data = False if not data else data
    self.return_content = "Success!" if not return_content else return_content

    super().__init__(
      block_type="return",
      recursive=False
    )

  def print_block(self, tabs=None):
    tabs = self.tabs if not tabs else tabs
    if not self.data:
      return f"{self.TAB_CHAR}"*tabs + f"return res.status({self.status}).send({{ message: {self.format_str(self.return_content)} }});\n"
    else:
      return f"{self.TAB_CHAR}"*tabs + f"return res.status({self.status}).send({self.return_content});\n"

    
