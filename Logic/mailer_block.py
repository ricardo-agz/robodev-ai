from Logic.logic_block import LogicBlock
from TemplateParser.helpers import camel_case


class MailerBlock(LogicBlock):
    def __init__(
            self,
            mailer=None,
            recipient="",
            subject="",
            data_context="",
            template="",
    ) -> None:
        self.mailer = mailer.strip()
        self.recipient = recipient.strip()
        self.subject = subject.rstrip()
        self.data_context = data_context.strip()
        self.template = template.strip()

        super().__init__(
            block_type="mailer",
            recursive=False
        )

    def print_block(self, tabs=None):
        # add braces if user didn't
        context_str = "{}" if self.data_context == "" else self.data_context
        if not context_str[0] == "{":
            context_str = "{ " + context_str
        if not context_str[-1] == "}":
            context_str += " }"

        # add quotes if subject is obviously supposed to be a string
        subject_str = self.subject
        if " " in subject_str:
            if not subject_str[0] == '"' and not subject_str[-1] == '"':
                subject_str = '"' + subject_str + '"'

        tabs = self.tabs if not tabs else tabs
        out_str = f"{self.TAB_CHAR}" * tabs + f"{camel_case(self.mailer)}.send{self.template}({{\n"
        out_str += f"{self.TAB_CHAR}" * (tabs + 1) + f"{self.recipient},\n"
        out_str += f"{self.TAB_CHAR}" * (tabs + 1) + f"{subject_str},\n"
        out_str += f"{self.TAB_CHAR}" * (tabs + 1) + f"{context_str},\n"
        out_str += f"{self.TAB_CHAR}" * tabs + f"}})\n"

        return out_str


