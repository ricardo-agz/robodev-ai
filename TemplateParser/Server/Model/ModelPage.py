import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.Model import Model
from TemplateParser.Relation import Relation
from TemplateParser.helpers import camel_case, pascal_case


class ModelPage(TemplateParser):
    def __init__(
            self,
            project: Project,
            model: Model,
            is_preview=False
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
            model,
            is_preview=is_preview
        )

        self.parse_file()

    def add_virtuals(self, many_model: Model, rel: Relation):
        """
        UserSchema.virtual('articles', {
          ref: 'Post',
          localField: '_id',
          foreignField: 'author'
        });
        """
        self_field = rel.field_a if rel.model_a == self.model.id else rel.field_b
        foreign_field = rel.field_b if rel.model_a == self.model.id else rel.field_a

        insert = [
            f"{self.model.name}Schema.virtual('{camel_case(self_field)}', {{\n",
            f"\tref: '{many_model.name}',\n",
            f"\tlocalField: '_id',\n",
            f"\tforeignField: '{foreign_field}'\n",
            f"}});\n\n",
        ]
        return insert

    def insert_many_array(self, field: str, foreign_model: Model):
        """
        courses: [
            {
                type: mongoose.Schema.Types.ObjectId,
                ref: "Course"
            }
        ]
        """
        self.out_lines.append(f"\t{camel_case(field)}: [\n")
        self.out_lines.append(f"\t\t{{\n")
        self.out_lines.append(f"\t\t\ttype: mongoose.Schema.Types.ObjectId,\n")
        self.out_lines.append(f"\t\t\tref: '{foreign_model.name}'\n")
        self.out_lines.append(f"\t\t}}\n")
        self.out_lines.append(f"\t],\n")

    def parse_file(self):
        for line in self.lines:

            # ----- MODEL RELATIONSHIPS -----
            if "$$ONE_TO_MANY:ONE" in line:
                contains_otm = False
                for rel in self.project.relations:
                    if rel.relation_type == "one-to-many" and rel.model_a == self.model.id:
                        # a_obj has many b_model
                        b_model = self.project.model_from_id(rel.model_b)
                        insert = self.add_virtuals(b_model, rel)
                        self.out_lines = self.out_lines + insert
                        contains_otm = True

                if contains_otm:
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

                    self.out_lines.append(f"\t\trequired: {str(req).lower()}\n")
                    self.out_lines.append(f"\t}},\n")

                for rel in self.project.relations:
                    if rel.relation_type == "one-to-many" and rel.model_b == self.model.id:
                        # b_model has one a_model
                        one_model = self.project.model_from_id(rel.model_a)

                        """
                        user: {
                            type: mongoose.Schema.Types.ObjectId,
                            ref: 'User',
                            required: true
                        },
                        """
                        self.out_lines.append(f"\t{rel.field_b}: {{\n")
                        self.out_lines.append(f"\t\ttype: mongoose.Schema.Types.ObjectId,\n")
                        self.out_lines.append(f"\t\tref: '{one_model.name}',\n")
                        self.out_lines.append(f"\t\trequired: true \n")
                        self.out_lines.append(f"\t}},\n")

            elif "$$MANY_ARRAY$$" in line:
                for rel in self.project.relations:
                    if rel.relation_type == "many-to-many":
                        if self.model.id == rel.model_a or self.model.id == rel.model_b:
                            many_id = rel.model_b if rel.model_a == self.model.id else rel.model_a
                            self_field = rel.field_a if rel.model_a == self.model.id else rel.field_b
                            foreign_field = rel.field_b if rel.model_a == self.model.id else rel.field_a
                            foreign_model = self.project.model_from_id(many_id)

                            self.insert_many_array(self_field, foreign_model)
                            if rel.model_a == rel.model_b:
                                # self-referential many-to-many, must insert both fields:
                                self.insert_many_array(foreign_field, self.model)

            else:
                self.out_lines.append(line)
