import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.helpers import append_at_index, camel_case, pascal_case, singularize

class ValidatedFormPage(TemplateParser):
  def __init__(
      self,
      project : Project,
      model : Model,
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "./validated_form_page.js.enp"
    out_file = f"./ValidatedForm.js"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
      model
    )

    self.parse_file()

  def parse_file(self):
    for line in self.lines:

      if "$$PARENT_MODEL_ID$$" in line and len(self.model.belongs_to) > 0:
        self.out_lines.append(f"\tconst {{ id }} = useParams();	\n")

      if "$$USE_STATES$$" in line:
        for param in self.model.schema:
          p_name = param["name"]
          p_type = param["type"]

          if p_type == "mongoose.Schema.Types.ObjectId":
            self.out_lines.append(f"\tconst [{p_name}, set{pascal_case(p_name)}] = useState(id ? id : '');\n")
          elif p_type == "String" or p_type == "Text":
            self.out_lines.append(f"\tconst [{p_name}, set{pascal_case(p_name)}] = useState('');\n")
          elif p_type == "Number":
            self.out_lines.append(f"\tconst [{p_name}, set{pascal_case(p_name)}] = useState(0);\n")
          elif p_type == "Boolean":
            self.out_lines.append(f"\tconst [{p_name}, set{pascal_case(p_name)}] = useState(false);\n")
          else:
            self.out_lines.append(f"\tconst [{p_name}, set{pascal_case(p_name)}] = useState(null);\n")

      if "$$VALIDATION$$" in line:
        check_str = ""
        submit_str = ""
        for i, param in enumerate(self.model.schema):
          p_name = param["name"]
          req = param["required"]
          if req:
            check_str += f"{' && ' if i != 0 else ''}{p_name} !== ''"
          submit_str += f"{', ' if i != 0 else ''}{p_name}"

      if "$$FORM_FIELDS$$" in line:
        for param in self.model.schema:
          p_name = param["name"]
          p_type = param["type"]
          if p_type == "mongoose.Schema.Types.ObjectId":
            p_type = "String"

          if p_type == "Boolean":
            """
            <div className='row'>
              <label>bool: </label>
              <Checkbox 
                defaultChecked 
                checked={bool}
                onChange={(e) => setBool(e.target.type === 'checkbox' ? e.target.checked : e.target.value)}
              />
            </div>
            """
            self.out_lines.append(f"\t\t\t\t<div className='row'>\n")
            self.out_lines.append(f"\t\t\t\t\t<label>{p_name}:</label>\n")
            self.out_lines.append(f"\t\t\t\t\t<Checkbox \n")
            self.out_lines.append(f"\t\t\t\t\t\tchecked={{{p_name}}}\n")
            self.out_lines.append(f"\t\t\t\t\t\tdefaultChecked \n")
            self.out_lines.append(f"\t\t\t\t\t\tonChange={{(e) => set{pascal_case(p_name)}(e.target.type === 'checkbox' ? e.target.checked : e.target.value)}}\n")
            self.out_lines.append(f"\t\t\t\t\t/>\n")
            self.out_lines.append(f"\t\t\t\t</div>\n")
          elif p_type == "Text":
            self.out_lines.append(f"\t\t\t\t<TextField\n")
            self.out_lines.append(f"\t\t\t\t\tlabel='{p_name}' size='small' multiline\n")
            self.out_lines.append(f"\t\t\t\t\tvalue={{{p_name}}}\n")
            self.out_lines.append(f"\t\t\t\t\tonChange={{(e) => set{pascal_case(p_name)}(e.target.value)}}\n")
            self.out_lines.append(f"\t\t\t\t/>\n")
          else:
            """
            <TextField
              label="username" size="small" type="Number"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            """
            self.out_lines.append(f"\t\t\t\t<TextField\n")
            self.out_lines.append(
              f"\t\t\t\t\tlabel='{p_name}' size='small' type='{'password' if p_name.lower() == 'password' else p_type}'\n")
            self.out_lines.append(f"\t\t\t\t\tvalue={{{p_name}}}\n")
            self.out_lines.append(f"\t\t\t\t\tonChange={{(e) => set{pascal_case(p_name)}(e.target.value)}}\n")
            self.out_lines.append(f"\t\t\t\t/>\n")

      if "$$VALIDATIONS$$" in line:
        check_str = ""
        submit_str = ""
        for i, param in enumerate(self.model.schema):
          p_name = param["name"]
          req = param["required"]
          if req:
            if i == 0:
              check_str += f"{p_name} !== ''"
            else:
              check_str += f" && {p_name} !== ''"

          if i == 0:
              submit_str += f"{p_name}"
          else:
            submit_str += f", {p_name}"
        """
        if (name !== "" && username !== "") {
          props.submit(name, username)
        } else {
          if (name === "") {
            setErr("name cannot be left blank")
          } 
          else if (username === "") {
            setErr("username cannot be left blank")
          }
        """
        self.out_lines.append(f"\t\tif ({check_str}) {{\n")
        self.out_lines.append(f"\t\t\tprops.submit({submit_str})\n")
        self.out_lines.append(f"\t\t}} else {{\n")

        for i, param in enumerate(self.model.schema):
          p_name = param["name"]
          req = param["required"]
          if req:
            if i == 0:
              self.out_lines.append(f"\t\t\tif ({p_name} === '') {{\n")
            else:
              self.out_lines.append(f"\t\t\telse if ({p_name} === '') {{\n")
            self.out_lines.append(f"\t\t\t\tsetErr('{p_name} cannot be left blank')\n")
            self.out_lines.append(f"\t\t\t}}\n")
          
      else:
        self.out_lines.append(line)