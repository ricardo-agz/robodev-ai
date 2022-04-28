import unittest
from TemplateParser.Project import Project
from TemplateParser.Model import Model

class TestProject(unittest.TestCase):

  def test_set_relations_one_to_many(self):
    user_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
      {'name': 'email', 'type': 'String', 'required': True},
      {'name': 'password', 'type': 'String', 'required': True},
    ]
    post_schema = [
      {'name': 'title', 'type': 'String', 'required': True},
      {'name': 'content', 'type': 'Text', 'required': True},
    ]
    user = \
      Model(
        name='user', 
        schema=user_schema, 
        has_many=[('user', 'friends'), ('post', 'posts'), ('user', 'blocked')]
      )
    post = \
      Model(
        name='post', 
        schema=post_schema, 
        has_many=[('user', 'friends'), ('post', 'posts')],
        belongs_to=[('user', 'author')]
      )
    project = \
      Project(
        "test_project",
        models=[user, post],
        auth_object='user',
        email="test@email.co"
      )

    expected = [(post, "posts")]
    actual = user.get_one_to_many()
    self.assertEqual(expected, actual)

  def test_set_relations_many_to_many(self):
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
        has_many=[('user', 'friends'), ('course', 'classes'), ('user', 'blocked')]
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

    user_expected = [(user, 'friends'), (course, "classes"), (user, 'blocked')]
    user_actual = user.get_many_to_many()
    course_expected = [(user, 'students')]
    course_actual = course.get_many_to_many()
    self.assertEqual(user_expected, user_actual)
    self.assertEqual(course_expected, course_actual)

  def test_get_complement_alias_otm(self):
    user_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
      {'name': 'email', 'type': 'String', 'required': True},
      {'name': 'password', 'type': 'String', 'required': True},
    ]
    post_schema = [
      {'name': 'title', 'type': 'String', 'required': True},
      {'name': 'content', 'type': 'Text', 'required': True},
    ]
    user = \
      Model(
        name='user', 
        schema=user_schema, 
        has_many=[('user', 'friends'), ('post', 'posts'), ('user', 'blocked')]
      )
    post = \
      Model(
        name='post', 
        schema=post_schema, 
        has_many=[('user', 'friends'), ('post', 'posts')],
        belongs_to=[('user', 'author')]
      )
    project = \
      Project(
        "test_project",
        models=[user, post],
        auth_object='user',
        email="test@email.co"
      )

    expected1 = "author"
    expected2 = "posts"
    actual1 = project.get_one_to_many_complement_alias(user, "posts")
    actual2 = project.get_one_to_many_complement_alias(post, "author")
    self.assertEqual(expected1, actual1)
    self.assertEqual(expected2, actual2)


