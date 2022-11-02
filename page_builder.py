"""
These functions are used to build individual project pages to be used
as a preview in the builder
"""
# SERVER
from TemplateParser.Server.Index.ServerIndexPage import ServerIndexPage
from TemplateParser.Server.Database.DatabasePage import DatabasePage
from TemplateParser.Server.Model.ModelPage import ModelPage
from TemplateParser.Server.Model.ModelPage import ModelPage
from TemplateParser.Server.Controller.Controller import ControllerPage
from TemplateParser.Server.Routes.RoutesPage import RoutesPage
from TemplateParser.Server.Middlewares.MiddlewaresPage import MiddlewaresPage
# CLIENT
from TemplateParser.Client.App.AppPage import AppPage
from TemplateParser.Client.Home.HomePage import HomePage
from TemplateParser.Client.SrcIndex.SrcIndexPage import SrcIndexPage
from TemplateParser.Client.LoginPage.LoginPage import LoginPage
from TemplateParser.Client.PrivateRoute.PrivateRoute import PrivateRoutePage
from TemplateParser.Client.ShowAll.ShowAllPage import ShowAllPage
from TemplateParser.Client.ShowOne.ShowOnePage import ShowOnePage
from TemplateParser.Client.ShowEdit.ShowEditPage import ShowEditPage
from TemplateParser.Client.ShowNew.ShowNewPage import ShowNewPage
from TemplateParser.Client.Nav.NavPage import NavPage
from TemplateParser.Client.UseApi.UseApiPage import UseApiPage
from TemplateParser.Client.UseAuth.UseAuthPage import UseAuthPage
from TemplateParser.Client.UseFind.UseFindPage import UseFindPage
from TemplateParser.Client.AuthContext.AuthContextPage import AuthContextPage
from TemplateParser.Client.AuthHeader.AuthHeaderPage import AuthHeaderPage

########## SERVER ##########

def build_controller_page(project, controller, model=None, is_auth=False):
  page = ControllerPage(project, controller, is_auth, is_preview=True)
  output = page.to_string()
  page.close_files()
  return output

def build_model_page(project, model):
  page = ModelPage(project, model,  is_preview=True)
  output = page.to_string()
  page.close_files()
  return output

def build_db_page(project):
  page = DatabasePage(project,  is_preview=True)
  output = page.to_string()
  page.close_files()
  return output

def build_server_page(project):
  page = ServerIndexPage(project,  is_preview=True)
  output = page.to_string()
  page.close_files()
  return output

def build_routes_page(project):
  page = RoutesPage(project,  is_preview=True)
  output = page.to_string()
  page.close_files()
  return output

def build_middlewares_page(project):
  middlewares = MiddlewaresPage(project,  is_preview=True)
  
  output = middlewares.to_string()
  
  middlewares.close_files()
  return output







########## CLIENT ##########

def build_client_app_page(project):
  page = AppPage(project)
  output = page.to_string()
  page.close_files()
  return output

def build_client_home_page(project):
  page = HomePage(project)
  output = page.to_string()
  page.close_files()
  return output

def build_client_src_index(project):
  page = SrcIndexPage(project)
  output = page.to_string()
  page.close_files()
  return output

def build_client_show_all(project, model):
  page = ShowAllPage(project, model)
  output = page.to_string()
  page.close_files()
  return output

def build_client_show_one(project, model):
  page = ShowOnePage(project, model)
  output = page.to_string()
  page.close_files()
  return output

def build_client_show_new(project, model):
  page = ShowNewPage(project, model)
  output = page.to_string()
  page.close_files()
  return output

def build_client_show_edit(project, model):
  page = ShowEditPage(project, model)
  output = page.to_string()
  page.close_files()
  return output

def build_client_navbar(project):
  page = NavPage(project, project.auth_object)
  output = page.to_string()
  page.close_files()
  return output

def build_client_login(project):
  page = LoginPage(project)
  output = page.to_string()
  page.close_files()
  return output

def build_client_private_route(project):
  page = PrivateRoutePage(project, project.auth_object)
  output = page.to_string()
  page.close_files()
  return output

def build_client_use_api(project):
  page = UseApiPage(project)
  output = page.to_string()
  page.close_files()
  return output

def build_client_use_auth(project):
  page = UseAuthPage(project)
  output = page.to_string()
  page.close_files()
  return output

def build_client_use_find(project):
  page = UseFindPage(project, project.auth_object)
  output = page.to_string()
  page.close_files()
  return output

def build_client_auth_header(project):
  page = AuthHeaderPage(project)
  output = page.to_string()
  page.close_files()
  return output

def build_client_auth_context(project):
  page = AuthContextPage(project, project.auth_object)
  output = page.to_string()
  page.close_files()
  return output