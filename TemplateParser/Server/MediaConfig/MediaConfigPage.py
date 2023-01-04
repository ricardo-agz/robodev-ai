"""
"bcrypt": "^5.0.1",
"jsonwebtoken": "^8.5.1",
"""
import os
from TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.helpers import camel_case, pascal_case


class MediaConfigPage(TemplateParser):
  def __init__(
      self,
      project : Project,
      config = None, 
      is_preview = False,
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
        # TODO: check upper, lowercase? 
        if self.project.config["media-config"]["database-type"] == "aws":
          self.out_lines.append("const AWS = require('aws-sdk');")
          self.out_lines.append("AWS.config.update({")
          self.out_lines.append(" accessKeyId: 'YOUR_ACCESS_KEY_ID',") 
          self.out_lines.append(" secretAccessKey: 'YOUR_SECRET_ACCESS_KEY',") 
          self.out_lines.append(" region: 'REGION',") 
          self.out_lines.append("});") 
        elif self.project.mediaConfig["database-type"] == "firebase":
          self.out_lines.append("TODO: firebase stuff")
          