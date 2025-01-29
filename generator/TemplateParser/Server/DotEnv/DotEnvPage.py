"""
"bcrypt": "^5.0.1",
"jsonwebtoken": "^8.5.1",
"""
import os

from TemplateParser.Project import Project
from generator.TemplateParser.TemplateParser import TemplateParser


class DotEnvPage(TemplateParser):
    def __init__(
            self,
            project: Project,
            is_preview=False,
    ) -> None:

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        """ CONSTANTS """
        in_file = "dot_env_page.txt"
        out_file = "./.env"

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
            if "$$JWT_SECRET$$" in line and self.project.auth_object:
                insert = f'JWT_SECRET = "PleaseChange"'
                self.out_lines.append(insert)

            else:
                self.out_lines.append(line)
