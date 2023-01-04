import os

from TemplateParser.Project import Project
from TemplateParser.TemplateParser import TemplateParser


class MediaConfigPage(TemplateParser):
    def __init__(
            self,
            project: Project,
            is_preview=False,
    ) -> None:

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        """ CONSTANTS """
        in_file = "./media_config_page.js"
        out_file = "./media_config.js"

        super().__init__(
            in_file,
            out_file,
            __location__,
            project,
            is_preview=is_preview,
        )
        self.parse_file()

    def parse_file(self):
        for line in self.lines:
            if "$$DYNAMIC_PAGE_CONTENT$$" in line:
                pass
                # TODO: check upper, lowercase?
                # if self.project.config["media-config"]["database-type"] == "aws":
                #   self.out_lines.append("const AWS = require('aws-sdk');")
                #   self.out_lines.append("AWS.config.update({")
                #   self.out_lines.append(" accessKeyId: 'YOUR_ACCESS_KEY_ID',")
                #   self.out_lines.append(" secretAccessKey: 'YOUR_SECRET_ACCESS_KEY',")
                #   self.out_lines.append(" region: 'REGION',")
                #   self.out_lines.append("});")
                # elif self.project.mediaConfig["database-type"] == "firebase":
                #   self.out_lines.append("TODO: firebase stuff")
            elif "$$OTHER_STUFF$$" in line:
                # self.out_lines.append("// other stuff\n")
                pass
            else:
                self.out_lines.append(line)
