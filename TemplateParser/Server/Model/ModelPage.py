import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.helpers import append_at_index

class ModelPage(TemplateParser):
  def __init__(
      self,
      project : Project,
      model : Model
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "./server_model.js"
    out_file = f"./{model.name}.js"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
      model
    )

    self.parse_file()

  
  def add_virtuals(self, many_model, alias):
    """
    UserSchema.virtual('posts', {
      ref: 'Post',
      localField: '_id',
      foreignField: 'user'
    });
    """
    insert = [
      f"{self.model.name}Schema.virtual('{alias.lower()}', {{\n",
      f"\tref: '{many_model.name}',\n",
      f"\tlocalField: '_id',\n",
      f"\tforeignField: '{self.project.get_one_to_many_complement_alias(self.model, alias)}'\n",
      f"}});\n\n",
    ]
    return insert


  def parse_file(self):
    for line in self.lines:

      #----- MODEL RELATIONSHIPS -----
      if "$$ONE_TO_MANY:ONE" in line:
        for many_model, alias in self.model.one_to_many:
          insert = self.add_virtuals(many_model, alias)
          self.out_lines = self.out_lines + insert

        self.out_lines.append(f"{self.model.name}Schema.set('toObject', {{ virtuals: true }});\n")
        self.out_lines.append(f"{self.model.name}Schema.set('toJSON', {{ virtuals: true }});\n")

      else:
        self.out_lines.append(line)


  