
import json
from generator import generator


f = open('sample_buildfile.json')
builder_data = json.load(f)

project, error = generator(builder_data)
print("project: ", project)
print("error: ", error)



