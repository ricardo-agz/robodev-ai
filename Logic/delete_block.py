from Logic.logic_block import LogicBlock
from Logic.error_block import ErrorBlock
from Logic.mongoose_block import MongooseBlock

class DeleteBlock(MongooseBlock):
  def __init__(
    self,
    model,
    params,
    var_name = None,
    variant = "one",
    success = [],
    error = None,
  ) -> None:

    super().__init__(
      block_type="delete",
      model=model,
      params="{ }" if not params else params,
      var_name=var_name,
      variant=variant,
      success=success,
      error=error,
      recursive=True
    )

    
