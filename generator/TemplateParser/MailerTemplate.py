
class MailerTemplate:
    def __init__(
            self,
            _id: str,
            name: str,
            content: str,
    ) -> None:
        self.id = _id
        self.name = name
        self.content = content