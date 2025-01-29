from Logic.logic_block import LogicBlock

class NextBlock(LogicBlock):
  def __init__(
    self,
  ) -> None:
    super().__init__(
      block_type="next",
      recursive=False
    )

  def print_block(self, tabs=None):
    tabs = self.tabs if not tabs else tabs
    out = f"{self.TAB_CHAR*tabs}" + "next();";
    
    return out + "\n"

    
