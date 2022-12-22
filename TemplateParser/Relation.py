from TemplateParser.Model import Model


class Relation:
    def __int__(
            self,
            _id: str,
            model_a: Model,
            model_b: Model,
            alias_a: str,
            alias_b: str,
            relation_type: str,
    ):
        self.id = _id
        self.model_a = model_a
        self.model_b = model_b
        self.alias_a = alias_a
        self.alias_b = alias_b
        self.relation_type = relation_type
