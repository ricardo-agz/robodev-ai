from Logic.logic_block import LogicBlock
from Logic.error_block import ErrorBlock
from Logic.mongoose_block import MongooseBlock

class UpdateBlock(MongooseBlock):
  def __init__(
    self,
    model,
    params,
    update_fields = [],
    var_name = None,
    variant = "one",
    success = [],
    error = None,
    tabs = 1
  ) -> None:

    super().__init__(
      block_type="update",
      model=model,
      params=params,
      update_fields=update_fields,
      var_name=var_name,
      variant=variant,
      success=success,
      error=error,
      tabs=tabs,
      recursive=True
    )