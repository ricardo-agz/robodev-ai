from Logic.logic_block import LogicBlock
from Logic.error_block import ErrorBlock
from Logic.mongoose_block import MongooseBlock

class CreateBlock(MongooseBlock):
  def __init__(
    self,
    model,
    create_fields = [],
    var_name = None,
    success = [],
    error = None,
    tabs = 1
  ) -> None:

    super().__init__(
      block_type="create",
      model=model,
      create_fields=create_fields,
      var_name=var_name,
      success=success,
      error=error,
      tabs=tabs,
      recursive=True
    )


   
