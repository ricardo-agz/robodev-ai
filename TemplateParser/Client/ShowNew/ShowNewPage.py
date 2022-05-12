import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.helpers import append_at_index, camel_case, pascal_case, singularize

class ShowNewPage(TemplateParser):
  def __init__(
      self,
      project : Project,
      model : Model,
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "./show_new_page.js.enp"
    out_file = f"./{model.name}New.js"

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

      if "$$HANDLE_SUBMIT$$" in line:
        sub_str = ""
        """
        const handleSubmit = (name, username, age) => {
        """
        for i, param in enumerate(self.model.schema):
          p_name = param["name"]
          p_type = param["type"]
          if i == 0:
            sub_str += f"{p_name}"
          else:
            sub_str += f", {p_name}"
        self.out_lines.append(f"\tconst handleSubmit = ({sub_str}) => {{\n")

      elif "$$VALIDATED_FORM$$" in line:
        tabs="\t\t\t"
        sub_str = ""
        for i, param in enumerate(self.model.schema):
          p_name = param["name"]
          p_type = param["type"]
          if i == 0:
            sub_str += f"{p_name}"
          else:
            sub_str += f", {p_name}"
        """
        <ValidatedForm 
          model={user}
          submit={(name, username) => 
            handleSubmit(name, username)
          }
        />
        """
        insert = [
          f"{tabs}<ValidatedForm\n",
          f"{tabs}\tloading={{loading}}\n",
          f"{tabs}\tsubmit={{({sub_str}) =>\n",
          f"{tabs}\t\thandleSubmit({sub_str})\n",
          f"{tabs}\t}}\n",
          f"{tabs}/>\n"
        ]
        self.out_lines = self.out_lines + insert
          
      else:
        self.out_lines.append(line)