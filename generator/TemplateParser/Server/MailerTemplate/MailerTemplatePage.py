import os

from TemplateParser.MailerTemplate import MailerTemplate
from generator.TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.helpers import camel_case, pascal_case


class MailerTemplatePage(TemplateParser):
    def __init__(
            self,
            project: Project,
            template: MailerTemplate,
            is_preview=False
    ) -> None:

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        """ CONSTANTS """
        in_file = "mailer_template_page.js"
        out_file = f"./{camel_case(template.name)}.js"

        self.template = template

        super().__init__(
            in_file,
            out_file,
            __location__,
            project,
            is_preview=is_preview
        )
        self.parse_file()

    def parse_file(self):
        for line in self.lines:
            if "$$CONTENT$$" in line:
                self.out_lines.append(self.template.content)

            else:
                self.out_lines.append(line)
