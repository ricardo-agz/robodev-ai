from TemplateParser.Model import Model


class Relation:
    def __init__(
            self,
            _id: str,
            model_a: Model,
            model_b: Model,
            field_a: str,   # field name for model B's relationship to model A, i.e. User has many Posts (articles)
            field_b: str,   # field name for model A's relationship to model B, i.e. Post has one User (author)
            relation_type: str,
            relation_name: str,
    ) -> None:
        self.id = _id
        self.model_a = model_a
        self.model_b = model_b
        self.field_a = field_a
        self.field_b = field_b
        self.relation_type = relation_type
        self.relation_name = relation_name
