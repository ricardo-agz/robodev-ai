import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.helpers import camel_case, pascal_case


class ModelPage(TemplateParser):
  def __init__(
      self,
      project : Project,
<<<<<<< HEAD
      model : Model
=======
      model : Model,
      is_preview = False
>>>>>>> 63078ef11eced2c8e9b33e15177acfc21c71c6f3
    ) -> None:

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    """ CONSTANTS """
    in_file = "./server_model.js"
    out_file = f"./{camel_case(model.name)}.js"

    super().__init__(
      in_file, 
      out_file,
      __location__,
      project,
<<<<<<< HEAD
      model
=======
      model,
      is_preview = is_preview
>>>>>>> 63078ef11eced2c8e9b33e15177acfc21c71c6f3
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
    complement_alias = camel_case(self.project.get_one_to_many_complement_alias(self.model, alias))
    insert = [
      f"{self.model.name}Schema.virtual('{camel_case(alias)}', {{\n",
      f"\tref: '{many_model.name}',\n",
      f"\tlocalField: '_id',\n",
      f"\tforeignField: '{complement_alias}'\n",
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

      elif "$$DYNAMIC_PARAMS$$" in line:
        for param in self.model.schema:
          p_name = param["name"]
          p_type = param["type"]
          req = param["required"]
          alias = param['alias'] if 'alias' in param else None
          
          """
          username: {
            type: String,
            required: true
          },
          """
          self.out_lines.append(f"\t{alias if alias else p_name}: {{\n")
          if p_type == "Text":
            self.out_lines.append(f"\t\ttype: String,\n")
          else:
            self.out_lines.append(f"\t\ttype: {p_type},\n")

          """
          user: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'User',
            required: true
          },
          """
          parent = self.project.model_from_name(p_name)
          if len(self.model.belongs_to) > 0 and parent:
            self.out_lines.append(f"\t\tref: '{parent.name}',\n")
          self.out_lines.append(f"\t\trequired: {str(req).lower()}\n")
          self.out_lines.append(f"\t}},\n")

      elif "$$MANY_ARRAY$$" in line:
        i = 0
        for many_model, alias in self.model.many_to_many:
          """
          courses: [
            {
              type: mongoose.Schema.Types.ObjectId,
              ref: "Course"
            }
          ]
          """
          self.out_lines.append(f"\t{camel_case(alias)}: [\n")
          self.out_lines.append(f"\t\t{{\n")
          self.out_lines.append(f"\t\t\ttype: mongoose.Schema.Types.ObjectId,\n")
          self.out_lines.append(f"\t\t\tref: '{many_model.name}'\n")
          self.out_lines.append(f"\t\t}}\n")
          self.out_lines.append(f"\t]{',' if i < len(self.model.many_to_many)-1 else ''}\n")
          i += 1
      
      else:
        self.out_lines.append(line)


  