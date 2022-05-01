
import json
from generator import generator


f = open('builder_output_test1.json')
builder_data = json.load(f)

generator(builder_data)
