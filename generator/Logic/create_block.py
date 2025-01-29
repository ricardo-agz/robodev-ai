from Logic.logic_block import LogicBlock
from Logic.error_block import ErrorBlock
from Logic.mongoose_block import MongooseBlock

class CreateBlock(MongooseBlock):
  def __init__(
    self,
    model,
    create_fields = None,
    var_name = None,
    success = [],
    error = None,
  ) -> None:

    super().__init__(
      block_type="create",
      model=model,
      create_fields= "{ }" if not create_fields else create_fields,
      var_name= f"new{model}" if not var_name else var_name,
      success=success,
      error=error,
      recursive=True
    )


   
