class LogicBlock:
  def __init__(
    self,
    block_type,
    recursive,
  ) -> None:
      self.block_type = block_type
      self.recursive = recursive
      self.TAB_CHAR = " "
      self.rec_id = 0

  def set_rec_id(self, id):
    self.rec_id = id

  def id_str(self):
    return self.rec_id+1 if self.rec_id > 0 else ''

  def is_quote(self, c):
    return c == '"' or c in "'`"

  def format_str(self, s):
    if type(s) == int or type(s) == float:
      return s
    elif not self.is_quote(s[0]) and not self.is_quote(s[-1]):
      s = '"' + s + '"'
    elif len(s) > 3 and s[0] == "'" and s[-1] == "'" and "'" in s[1:-1]:
      s = '"' + s[1:-1] + '"'

    return s

  def recurse_error(self, tabs, out=""):
    for block in self.error:
      if block.recursive:
        block.set_rec_id(self.rec_id+1)
        block.recurse_success(self.tabs+1, out)
        block.recurse_error(self.tabs+1, out)
      out += block.print_block(tabs+1)

    return out

  def recurse_success(self, tabs, out=""):
    for block in self.success:
      if block.recursive:
        block.set_rec_id(self.rec_id+1)
        block.recurse_success(self.tabs+1, out)
        block.recurse_error(self.tabs+1, out)
      out += block.print_block(tabs+1)

    return out

  def get_callback_str(self, tabs):
    callback_str_start = f"{self.TAB_CHAR*(tabs)}(err{self.id_str()}, data{self.id_str()}) => {{"
    callback_str_end = f"{self.TAB_CHAR*(tabs)}}}"

    """
    (err, data) => {
      if (err) {
        ...err_recurse_str
      }
    }
    """
    err_recurse_content = self.recurse_error(tabs+1).rstrip()
    err_recurse = [
      f"\n{self.TAB_CHAR*(tabs+1)}if (err{self.id_str()}) {{",
      err_recurse_content,
      f"{self.TAB_CHAR*(tabs+1)}}};\n",
    ]
    err_recurse_str = "\n".join(err_recurse)
    success_recurse_content = self.recurse_success(tabs) if self.success and len(self.success) > 0 else ''

    return callback_str_start + err_recurse_str + success_recurse_content + callback_str_end