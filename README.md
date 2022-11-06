# Neutrino V3

## Running the code:
`docker-compose build`

`docker-compose up`

&nbsp;
## Structure

### /TemplateParser
This folder holds all the main logic components for generating the code

### Classes
- Model.py
    - Represents a 'class' or an object 'model'. 
- Project.py
    - Object representing the actual project. Holds information like user credentials, all models in project,
    auth configuration, etc.
- Route.py
    - Object representing a route in the project. Stored by each model. Holds information like whether or not its 
    protected, who it belongs, to the HTTP method, logic, etc. 
- TemplateParer.py
    - Abstract class that all project Pages inherit from.
    Ex. Server's server.js is its own class inheriting from TemplateParser

Example Usage: (snip from `test_project.py`)
```
user_schema = [
  {'name': 'username', 'type': 'String', 'required': True},
  {'name': 'email', 'type': 'String', 'required': True},
  {'name': 'password', 'type': 'String', 'required': True},
]
post_schema = [
  {'name': 'title', 'type': 'String', 'required': True},
  {'name': 'content', 'type': 'Text', 'required': True},
]
user = \
  Model(
    name='user', 
    schema=user_schema, 
    has_many=[('user', 'friends'), ('post', 'posts'), ('user', 'blocked')]
  )
post = \
  Model(
    name='post', 
    schema=post_schema, 
    has_many=[('user', 'friends'), ('post', 'posts')],
    belongs_to=[('user', 'author')]
  )
project = \
  Project(
    "test_project",
    models=[user, post],
    auth_object='user',
    email="test@email.co"
  )

expected = [(post, "posts")]
actual = user.get_one_to_many()
self.assertEqual(expected, actual)
```

Client and Server
- These folders are just for organization, they divide each page by which sub project they belong to
  i.e. Frontend's App.js file could be found under './Client/App'

### Page Classes
ex. ShowEdit
- ShowEditPage.py
  - Class inherits from TemplateParser
  - Can be used to write out actual page
  - ex.
  ```
    show_edit = ShowEditPage(project, model)
    show_edit.write_out_file()
    show_edit.close_files()
  ```
  - wite_out_file() will automatically create file in specified directory in ShowEditPage.py
  - must always call close_files() at the end
- show_edit_page.js.enp
  - js.enp <-- custom extention for 'embedded neutrino python' (syntax highlighter in the works)
  - File is templat that will be written when writing the page
  - Can insert custom logic through two ways:
    - `$$INSERT_LOGIC_NAME_HERE$$`
      - In ShowEditPage.py, override `parse_file()` function
      ```
      def parse_file(self):
        for line in self.lines:

          if "$$SOME_LOGIC$$" in line:
            ... some logic ...
            self.out_lines.append(f"\tconsole.log('custom javascript code')\n")
      ```
    - In-line Embedded Python:
      ```
      <$= "import Login from './Login'" if self.project.auth_object else "" $>
      ```
        - This line will evaluate the ternary operator and render one of the two strings
    - Conditional Blocks:
      ```
      <$ begin if self.project.auth_object $>
      console.log('custom javascript code);
      <$= f"if ({camel_case(self.model.name)}) {{" $> // in-block python injection
      <$ end $>
      ```
    - Embedded for-loops:
      ```
      <$ for model in self.project.models $>
      console.log('custom javascript code);
      <$= f"<h1> {title_space_case(model.name)} </h1>" $> // in-block python injection
      <$ end $>
      ```
    - Template comments:
      Explicitly for template understandability. Will not get written out to code
      ```
      <!-- This is a template comment -->

      <$# This is also a template comment $>
      ```

### generator.py
Overarching function that expecutes everything and builds out the project
- Takes in `builder_data` : JSON data provided by builder frontend
  - examples in `builder_output_test1.json`
  - `builder_output_test2.json` is slightly off, don't use yet
- Creates directories
- Calls Page classes to create files

---

## Testing
### /test
- test_model.py
- test_project.py
- test_route.py
- test_template_parser.py

### Running Tests
In terminal, run: 
```
python -m unittest discover ./test -p '*.py'
```

## Testing actual generator
In test.py:
```
import json
from generator import generator

f = open('builder_output_test1.json') # or whichever custom test data you want to try 
builder_data = json.load(f)

generator(builder_data)
```

In command line run:
```
python test.py
```
This will create the project folder at the root level 