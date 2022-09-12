from Logic.logic_block import LogicBlock

class JWTBlock(LogicBlock):
  def __init__(
    self,
    model,
    jwt_variant,
    payload,
    secret,
    token,
    expiration,
    success = [],
    error = [],
    tabs = 1
  ) -> None:
    self.model = model
    self.jwt_variant = jwt_variant
    self.payload = payload
    self.secret = secret
    self.token = token
    self.expiration = expiration
    self.tabs = tabs
    self.success = success
    self.error = error

    super().__init__(
      block_type="jwt_block",
      recursive=True
    )



  def print_block(self, tabs=None):
    
    tabs = self.tabs if not tabs else tabs
    out_str = f"jwt.sign( {self.payload}, {self.secret}, " + "{expiresIn: " + f"{self.expiration}" + "},\n" if self.jwt_variant== "sign" else f"jwt.verify( {self.token}, {self.secret},\n"
    out_str += f"{self.TAB_CHAR*tabs}"+"(err, token) => " + "{\n" if self.jwt_variant == "sign" else f"{self.TAB_CHAR*tabs}" + "(err, decoded)" + "=>" + "{\n"
    
    success_str = self.recurse_success(tabs)
    error_str = self.recurse_error(tabs)

    if (len(error_str) > 0):
      out_str += self.TAB_CHAR*(tabs+2)  + f"if (err)" + "{\n"
      out_str += self.TAB_CHAR*(tabs+2) + error_str 
      out_str += self.TAB_CHAR*(tabs+2) +"}\n"
    
    out_str += success_str

    out_str += f"{self.TAB_CHAR*tabs}" + "})\n"

    code_split = out_str.split('\n')
    
    code_split = [f"{self.TAB_CHAR*tabs}" + x for x in code_split]

    
    return "\n".join(code_split).rstrip(self.TAB_CHAR) 
  

    
