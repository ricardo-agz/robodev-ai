from TemplateParser.MailerTemplate import MailerTemplate


class Mailer:
    def __init__(
            self,
            _id: str,
            name: str,
            templates: list[MailerTemplate]
    ) -> None:
        self.id = _id
        self.name = name
        self.templates = templates
