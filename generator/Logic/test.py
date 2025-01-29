from Logic.conditional_block import ConditionalBlock
from Logic.query_block import QueryBlock
from Logic.error_block import ErrorBlock
from Logic.return_block import ReturnBlock
from Logic.delete_block import DeleteBlock
from Logic.update_block import UpdateBlock
from Logic.create_block import CreateBlock

query = QueryBlock(model="User", params="{ name: 'ricky', age: { $gte: 18 } }", var_name="user", variant="many", tabs=0)
query2 = QueryBlock(model="Post", params="{ name: 'ricky', age: { $gte: 18 } }", var_name="post", variant="many", tabs=0)
error = ErrorBlock(status=401, message="this is an error" )
ret = ReturnBlock(status=201, variant="message", data="user", message="Successfully updated user's info",tabs=0)
del_block = DeleteBlock(model="User", params="{ _id: id }", tabs=0)
update = UpdateBlock(
  model="Post", 
  var_name="newPost",
  params="{name: name, _id: id}", 
  update_fields=[["name", "newName"], ["age", "newAge"]], 
  variant="one", 
  success=[del_block, ret], 
  error=None, 
  tabs=0)

create = CreateBlock(
  model="User",
  create_fields=[["name", "ricky"], ["age", 21]],
  var_name="newUser",
  success=[ret]
)

q1 = QueryBlock(model="User", params="_id", var_name="user")
print(q1.print_block())

cond = ConditionalBlock(condition="user.name == 'ricky'", success=[update, ret])
print(cond.print_block())

# print(query.print_block())
# print(error.print_block())
# print(ret.print_block())
# print(del_block.print_block())
# print(update.print_block())
# print(create.print_block())
