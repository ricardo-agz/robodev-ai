from Logic.logic_block import LogicBlock

class NextBlock(LogicBlock):
  def __init__(
    self,
    tabs = 1
  ) -> None:
    self.tabs = tabs
    super().__init__(
      block_type="next",
      recursive=False
    )

  def print_block(self, tabs=None):
    tabs = self.tabs if not tabs else tabs
    # bcrypt.compare(req.body.password, $$name$$.password);
    
    
    
    out = f"{self.TAB_CHAR*tabs}" + "next()";

    
    return out + "\n"

    
