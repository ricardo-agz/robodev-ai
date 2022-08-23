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
    self.model = model,
    self.jwt_variant = jwt_variant,
    self.payload = payload,
    self.secret = secret,
    self.token = token,
    self.expiration = expiration,
    self.tabs = tabs
    self.success = success
    self.error = error

    super().__init__(
      block_type="jwt_block",
      recursive=True
    )



  def print_block(self, tabs=None):
    tabs = self.tabs if not tabs else tabs

    out_str = f"{self.TAB_CHAR*tabs}" + "jwt.sign( {self.payload}, {self.secret}," + "{expiresIn: " + f"{self.expiration}" + "}," if self.jwt_variant== "sign" else "jwt.verify( {self.token}, {self.secret},\n"
    out_str += f"{self.TAB_CHAR*(tabs+1)}{"(err, token)" if self.jwt_variant == "sign" else "(err, decoded)"} => "+"{\n"

    success_str = self.recurse_success(tabs+1)
    error_str = self.recurse_error(tabs+1)

    if (len(error_str) > 0) {
      out_str += f"{self.TAB_CHAR*(tabs+1)}if (err)" + "{\n"
      out_str += error_str 
    } 
    out_str += success_str
    return out_str

    
