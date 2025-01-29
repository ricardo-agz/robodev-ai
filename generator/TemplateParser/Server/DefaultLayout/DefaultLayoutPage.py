import os
from generator.TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project


class DefaultLayoutPage(TemplateParser):
    def __init__(
            self,
            project: Project,
            is_preview=False
    ) -> None:

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        """ CONSTANTS """
        in_file = "default_layout_page.hbs"
        out_file = "./default.hbs"

        super().__init__(
            in_file,
            out_file,
            __location__,
            project,
            is_preview=is_preview
        )

        self.parse_file()
