"""
"bcrypt": "^5.0.1",
"jsonwebtoken": "^8.5.1",
"""
import os

from TemplateParser.Project import Project
from TemplateParser.TemplateParser import TemplateParser


class PackageJSONPage(TemplateParser):
    def __init__(
            self,
            project: Project,
            is_preview=False
    ) -> None:
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        """ CONSTANTS """
        in_file = "./package_json_page.json"
        out_file = "./package.json"

        super().__init__(
            in_file,
            out_file,
            __location__,
            project,
            is_preview=is_preview
        )

        self.parse_file()
