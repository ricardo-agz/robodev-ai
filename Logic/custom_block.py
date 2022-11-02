from Logic.logic_block import LogicBlock

class CustomBlock(LogicBlock):
  def __init__(
    self,
    code=None,
  ) -> None:
    self.code = "console.log('custom block');" if not code else code

    super().__init__(
      block_type="conditional",
      recursive=False
    )

  def print_block(self, tabs=None):
    tabs = self.tabs if not tabs else tabs

    code_split = self.code.split('\n')
    code_split = [f"{self.TAB_CHAR*tabs}" + x for x in code_split]

    return "\n".join(code_split) + "\n"

    
