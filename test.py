
import json
from generator import generator


f = open('builder_output_test1.json')
builder_data = json.load(f)

generator(builder_data)

# # print(type(eval("False")))

# res = eval("True")
# if res:
#   print("this should not happen")

# test_arr = [1, 2, 3, 4]

# str = "test_arr"
# var = "x"

# print(eval(var))
