import os
import re

from TemplateParser.Mailer import Mailer
from generator.TemplateParser.TemplateParser import TemplateParser
from TemplateParser.Project import Project
from TemplateParser.helpers import camel_case, pascal_case


def destructure_content_params(content):
    # Use a regular expression to find all words surrounded by ${}
    matches = re.findall(r"\${([^}]*)}", content)

    # Split each word at the first period and return the first part
    words = [word.split(".")[0] for word in matches]

    # Return the list of words
    return words


class MailerPage(TemplateParser):
    def __init__(
            self,
            project: Project,
            mailer: Mailer,
            is_preview=False
    ) -> None:

        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        """ CONSTANTS """
        in_file = "mailer_page.js"
        out_file = f"./{camel_case(mailer.name)}.js"

        self.mailer = mailer

        super().__init__(
            in_file,
            out_file,
            __location__,
            project,
            mailer=mailer,
            is_preview=is_preview
        )
        self.parse_file()

    def parse_file(self):
        for line in self.lines:
            if "$$DOTENV$$" in line:
                req = False
                for t in self.mailer.templates:
                    if "process.env" in t.content:
                        req = True
                if req:
                    self.out_lines.append("require('dotenv').config();\n")

            elif "$$TEMPLATES$$" in line:
                for i, template in enumerate(self.mailer.templates):
                    """                
                    sendWelcomeMail(recipient, subject, templateData, callback) {
                        const email = {
                            from: this.sender,
                            to: recipient,
                            subject: subject,
                            context: templateData
                            template: 'welcome-email'
                        }
                
                        transporter.sendMail(email, callback);
                    }
                    """
                    params = destructure_content_params(template.content)
                    params_str = ""
                    if len(params) > 0:
                        params_str = "{"
                        for j, p in enumerate(params):
                            params_str += p
                            if j < len(params) - 1:
                                params_str += ", "
                        params_str += "}"

                    self.out_lines.append(
                        f"\tsend{pascal_case(template.name)}(recipient, subject, templateData, callback) {{\n")
                    self.out_lines.append(f"\t\tconst email = {{\n")
                    self.out_lines.append(f"\t\t\tfrom: this.sender,\n")
                    self.out_lines.append(f"\t\t\tto: recipient,\n")
                    self.out_lines.append(f"\t\t\tsubject: subject,\n")
                    self.out_lines.append(f"\t\t\tcontext: templateData,\n")
                    self.out_lines.append(f"\t\t\ttemplate: {camel_case(template.name)},\n")
                    self.out_lines.append(f"\t\t}}\n\n")
                    self.out_lines.append(f"\t\tthis.transporter.sendMail(email, callback);\n")
                    self.out_lines.append(f"\t}}\n")
                    if i < len(self.mailer.templates) - 1:
                        self.out_lines.append(f"\n")

            else:
                self.out_lines.append(line)
