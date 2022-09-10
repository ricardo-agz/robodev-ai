from Logic.logic_block import LogicBlock

class BcryptBlock(LogicBlock):
  def __init__(
    self,
    model,
    var_name,
    bcrypt_variant,
    plain_text,
    hash,
    salt_rounds,
    tabs = 1
  ) -> None:
    self.model = model
    self.var_name = var_name
    self.bcrypt_variant = bcrypt_variant
    self.plain_text = plain_text
    self.hash = hash
    self.salt_rounds = salt_rounds
    self.tabs = tabs

    super().__init__(
      block_type="bcrypt",
      recursive=False
    )

  def print_block(self, tabs=None):
    tabs = self.tabs if not tabs else tabs
    # bcrypt.compare(req.body.password, $$name$$.password);
    
    
    
    if (self.bcrypt_variant == "compare") :
      
      code = "const " +  self.var_name +  " = await bcrypt.compare(" + self.plain_text + "," + self.hash + ")"
      
    else:
      code = "const " +  self.var_name +  " = await bcrypt.hash(" + self.plain_text + "," + self.salt_rounds + ")"
    code_split = code.split('\n')
    
    code_split = [f"{self.TAB_CHAR*tabs}" + x for x in code_split]

    
    return "\n".join(code_split) + "\n"

    
