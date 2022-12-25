import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project


class BaseMailerPage(TemplateParser):
    def __init__(
            self,
            project: Project,
            is_preview=False
    ) -> None:

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        """ CONSTANTS """
        in_file = "./base_mailer_page.js"
        out_file = "./baseMailer.js"

        super().__init__(
            in_file,
            out_file,
            __location__,
            project,
            is_preview=is_preview
        )

        self.parse_file()
