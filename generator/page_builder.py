"""
These functions are used to build individual project pages to be used
as a preview in the builder
"""
from TemplateParser.Server.DotEnv.DotEnvPage import DotEnvPage
from TemplateParser.Server.Index.ServerIndexPage import ServerIndexPage
from TemplateParser.Server.Mailer.MailerPage import MailerPage
from TemplateParser.Server.MailerTemplate.MailerTemplatePage import MailerTemplatePage
from TemplateParser.Server.MailerTransporter.MailerTransporterPage import MailerTransporterPage
from TemplateParser.Server.MediaConfig.MediaConfigPage import MediaConfigPage
from TemplateParser.Server.Middlewares.MiddlewaresPage import MiddlewaresPage
from TemplateParser.Server.Model.ModelPage import ModelPage
from TemplateParser.Server.PackageJSON.PackageJSONPage import PackageJSONPage
from TemplateParser.Server.Readme.ReadmePage import ReadmePage
from TemplateParser.Server.Routes.RoutesPage import RoutesPage
from TemplateParser.Server.BaseMailer.BaseMailerPage import BaseMailerPage
from TemplateParser.Server.Controller.Controller import ControllerPage
from TemplateParser.Server.Database.DatabasePage import DatabasePage
from TemplateParser.Server.DefaultLayout.DefaultLayoutPage import DefaultLayoutPage


def write_and_close(page, is_preview: bool):
    """
    Performs the correct write action and properly closes the files.
    If the page is in preview mode, it returns the string contents of the page,
    otherwise, writes the contents to the correct output file in the exported project
    """
    output = None
    if is_preview:
        output = page.to_string()
    else:
        page.write_out_file()
    page.close_files()

    return output


def build_controller_page(project, controller, is_preview=True):
    page = ControllerPage(project, controller, is_preview=is_preview)
    return write_and_close(page, is_preview)


def build_transporter_page(project, is_preview=True):
    page = MailerTransporterPage(project, is_preview=is_preview)
    return write_and_close(page, is_preview)


def build_base_mailer_page(project, is_preview=True):
    page = BaseMailerPage(project, is_preview=is_preview)
    return write_and_close(page, is_preview)


def build_mailer_template_page(project, template, is_preview=True):
    page = MailerTemplatePage(project, template, is_preview=is_preview)
    return write_and_close(page, is_preview)


def build_default_layout_page(project, is_preview=True):
    page = DefaultLayoutPage(project, is_preview=is_preview)
    return write_and_close(page, is_preview)


def build_mailer_page(project, mailer, is_preview=True):
    page = MailerPage(project, mailer, is_preview=is_preview)
    return write_and_close(page, is_preview)


def build_model_page(project, model, is_preview=True):
    page = ModelPage(project, model, is_preview=is_preview)
    return write_and_close(page, is_preview)


def build_db_page(project, is_preview=True):
    page = DatabasePage(project, is_preview=is_preview)
    return write_and_close(page, is_preview)


def build_server_page(project, is_preview=True):
    page = ServerIndexPage(project, is_preview=is_preview)
    return write_and_close(page, is_preview)


def build_routes_page(project, is_preview=True):
    page = RoutesPage(project, is_preview=is_preview)
    return write_and_close(page, is_preview)


def build_middlewares_page(project, is_preview=True):
    page = MiddlewaresPage(project, is_preview=is_preview)
    return write_and_close(page, is_preview)


def build_package_json_page(project, is_preview=True):
    page = PackageJSONPage(project, is_preview=is_preview)
    return write_and_close(page, is_preview)


def build_dotenv_page(project, is_preview=True):
    page = DotEnvPage(project, is_preview=is_preview)
    return write_and_close(page, is_preview)


def build_readme_page(project, is_preview=True):
    page = ReadmePage(project, is_preview=is_preview)
    return write_and_close(page, is_preview)


def build_media_config_page(project, is_preview=True):
    page = MediaConfigPage(project, is_preview=is_preview)
    return write_and_close(page, is_preview)
