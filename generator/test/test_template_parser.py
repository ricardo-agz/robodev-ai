import unittest
from TemplateParser.Model import Model
from TemplateParser.Route import Route
from TemplateParser.Project import Project
from TemplateParser.Server.Controller.Controller import ControllerPage
from TemplateParser.Server.Index.ServerIndexPage import ServerIndexPage

class TestRoute(unittest.TestCase):

  def test_server_index(self):
    user_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
      {'name': 'email', 'type': 'String', 'required': True},
      {'name': 'password', 'type': 'String', 'required': True},
    ]
    course_schema = [
      {'name': 'title', 'type': 'String', 'required': True},
      {'name': 'description', 'type': 'Text', 'required': True},
    ]
    user = \
      Model(
        name='user', 
        schema=user_schema, 
        has_many=[('user', 'friends'), ('course', 'classes'), ('user', 'blocked')],
        auth=True
      )
    course = \
      Model(
        name='course', 
        schema=course_schema, 
        has_many=[('user', 'students')],
      )
    project = \
      Project(
        "test_project",
        models=[user, course],
        auth_object='user',
        email="test@email.co"
      )
    # server_index = ServerIndexPage(project)
    # server_index.write_out_file()
    # server_index.close_files()
    # user_controler = ControllerPage(project, user)
    # user_controler.write_out_file()
    # user_controler.close_files()

  