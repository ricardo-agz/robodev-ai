import unittest
from TemplateParser.Model import Model
from TemplateParser.Route import Route

class TestModel(unittest.TestCase):

  def test_naming(self):
    model_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
    ]
    model = Model(
                  name='user', 
                  schema=model_schema,
                )

    expected = "Users"
    actual = model.plural
    self.assertEqual(expected, actual)

  def test_naming_goose(self):
    model_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
    ]
    model = Model(
                  name='goose', 
                  schema=model_schema,
                )

    expected = "Geese"
    actual = model.plural
    self.assertEqual(expected, actual)

  def test_naming_non_camelcase(self):
    model_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
    ]
    model = Model(
                  name='user_document', 
                  schema=model_schema,
                )

    expected = "UserDocument"
    actual = model.name
    self.assertEqual(expected, actual)
    self.assertEqual("UserDocuments", model.plural)

  def test_self_references(self):
    user_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
      {'name': 'email', 'type': 'String', 'required': True},
      {'name': 'password', 'type': 'String', 'required': True},
    ]
    user = Model(
                  name='user', 
                  schema=user_schema, 
                  has_many=[('user', 'friends'), ('post', 'posts'), ('user', 'blocked')]
                )

    expected = ['friends', 'blocked']
    actual = user.get_self_referencing()
    self.assertEqual(expected, actual)

  def test_belongs_to_str_true(self):
    post_schema = [
      {'name': 'title', 'type': 'String', 'required': True},
      {'name': 'content', 'type': 'Text', 'required': True},
    ]
    post = Model(
                  name='post', 
                  schema=post_schema, 
                  has_many=[('user', 'friends'), ('post', 'posts')],
                  belongs_to=[('user', 'author')]
                )
                
    self.assertTrue(post.does_belong_to('user'))

  def test_belongs_to_str_false(self):
    user_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
      {'name': 'email', 'type': 'String', 'required': True},
      {'name': 'password', 'type': 'String', 'required': True},
    ]
    user = Model(
                  name='user', 
                  schema=user_schema, 
                  has_many=[('user', 'friends'), ('post', 'posts'), ('user', 'blocked')]
                )
                
    self.assertFalse(user.does_belong_to('post'))

  def test_belongs_to_obj_true(self):
    user_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
      {'name': 'email', 'type': 'String', 'required': True},
      {'name': 'password', 'type': 'String', 'required': True},
    ]
    post_schema = [
      {'name': 'title', 'type': 'String', 'required': True},
      {'name': 'content', 'type': 'Text', 'required': True},
    ]
    user = Model(
                  name='user', 
                  schema=user_schema, 
                  has_many=[('user', 'friends'), ('post', 'posts'), ('user', 'blocked')]
                )
    post = Model(
                  name='post', 
                  schema=post_schema, 
                  has_many=[('user', 'friends'), ('post', 'posts')],
                  belongs_to=[('user', 'author')]
                )
                
    self.assertTrue(post.does_belong_to(user))

  def test_belongs_to_obj_false(self):
    user_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
      {'name': 'email', 'type': 'String', 'required': True},
      {'name': 'password', 'type': 'String', 'required': True},
    ]
    post_schema = [
      {'name': 'title', 'type': 'String', 'required': True},
      {'name': 'content', 'type': 'Text', 'required': True},
    ]
    user = Model(
                  name='user', 
                  schema=user_schema, 
                  has_many=[('user', 'friends'), ('post', 'posts'), ('user', 'blocked')]
                )
    post = Model(
                  name='post', 
                  schema=post_schema, 
                  has_many=[('user', 'friends'), ('post', 'posts')],
                  belongs_to=[('user', 'author')]
                )
                
    self.assertFalse(user.does_belong_to(post))

  def test_has_many_str_true(self):
    user_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
      {'name': 'email', 'type': 'String', 'required': True},
      {'name': 'password', 'type': 'String', 'required': True},
    ]
    user = Model(
                  name='user', 
                  schema=user_schema, 
                  has_many=[('user', 'friends'), ('post', 'posts'), ('user', 'blocked')]
                )
                
    self.assertTrue(user.does_have_many('post'))

  def test_has_many_str_false(self):
    post_schema = [
      {'name': 'title', 'type': 'String', 'required': True},
      {'name': 'content', 'type': 'Text', 'required': True},
    ]
    post = Model(
                  name='post', 
                  schema=post_schema, 
                  has_many=[('comment', 'comments')],
                  belongs_to=[('user', 'author')]
                )
                
    self.assertFalse(post.does_have_many('user'))

  def test_has_many_obj_true(self):
    user_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
      {'name': 'email', 'type': 'String', 'required': True},
      {'name': 'password', 'type': 'String', 'required': True},
    ]
    post_schema = [
      {'name': 'title', 'type': 'String', 'required': True},
      {'name': 'content', 'type': 'Text', 'required': True},
    ]
    user = Model(
                  name='user', 
                  schema=user_schema, 
                  has_many=[('user', 'friends'), ('post', 'posts'), ('user', 'blocked')]
                )
    post = Model(
                  name='post', 
                  schema=post_schema, 
                  has_many=[('comment', 'comments')],
                  belongs_to=[('user', 'author')]
                )
                
    self.assertTrue(user.does_have_many(post))

  def test_has_many_obj_false(self):
    user_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
      {'name': 'email', 'type': 'String', 'required': True},
      {'name': 'password', 'type': 'String', 'required': True},
    ]
    post_schema = [
      {'name': 'title', 'type': 'String', 'required': True},
      {'name': 'content', 'type': 'Text', 'required': True},
    ]
    user = Model(
                  name='user', 
                  schema=user_schema, 
                  has_many=[('user', 'friends'), ('post', 'posts'), ('user', 'blocked')]
                )
    post = Model(
                  name='post', 
                  schema=post_schema, 
                  has_many=[('comment', 'comments')],
                  belongs_to=[('user', 'author')]
                )
                
    self.assertFalse(post.does_have_many(user))

  def test_has_many_obj_self_reference_true(self):
    user_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
      {'name': 'email', 'type': 'String', 'required': True},
      {'name': 'password', 'type': 'String', 'required': True},
    ]
    post_schema = [
      {'name': 'title', 'type': 'String', 'required': True},
      {'name': 'content', 'type': 'Text', 'required': True},
    ]
    user = Model(
                  name='user', 
                  schema=user_schema, 
                  has_many=[('user', 'friends'), ('post', 'posts'), ('user', 'blocked')]
                )
    post = Model(
                  name='post', 
                  schema=post_schema, 
                  has_many=[('comment', 'comments')],
                  belongs_to=[('user', 'author')]
                )
                
    self.assertTrue(user.does_have_many(user))

  def test_has_many_obj_many_many_true(self):
    user_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
      {'name': 'email', 'type': 'String', 'required': True},
      {'name': 'password', 'type': 'String', 'required': True},
    ]
    course_schema = [
      {'name': 'title', 'type': 'String', 'required': True},
      {'name': 'description', 'type': 'Text', 'required': True},
    ]
    user = Model(
                  name='user', 
                  schema=user_schema, 
                  has_many=[('user', 'friends'), ('post', 'posts'), ('course', 'classes')]
                )
    course = Model(
                  name='course', 
                  schema=course_schema, 
                  has_many=[('user', 'students'), ('course', 'crosslist')],
                )
                
    self.assertTrue(user.does_have_many(course))
    self.assertTrue(course.does_have_many(user))

  def test_routes_init(self):
    user_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
      {'name': 'email', 'type': 'String', 'required': True},
      {'name': 'password', 'type': 'String', 'required': True},
    ]
    user = Model(
        name='user', 
        schema=user_schema, 
        has_many=[('user', 'friends'), ('post', 'posts'), ('course', 'classes')]
      )
                
    self.assertEqual(5, len(user.get_routes()))

  def test_routes_manual(self):
    user_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
      {'name': 'email', 'type': 'String', 'required': True},
      {'name': 'password', 'type': 'String', 'required': True},
    ]
    user = Model(
        name='user', 
        schema=user_schema, 
        has_many=[('user', 'friends'), ('post', 'posts'), ('course', 'classes')],
      )
    user_routes = [
      Route("index", "get", "/users", user, protected=True, logic="some logic")
    ]
    user.set_routes(user_routes)
                
    
    self.assertEqual(1, len(user.get_routes()))
    self.assertEqual("some logic", user.get_routes()[0].get_logic())

  def test_add_route_manual(self):
    user_schema = [
      {'name': 'username', 'type': 'String', 'required': True},
    ]
    user = Model(
        name='user', 
        schema=user_schema, 
        has_many=[('user', 'friends'), ('post', 'posts'), ('course', 'classes')],
      )
    user_routes = [
      Route("index", "get", "/users", user, protected=True, logic="some logic")
    ]
    user.set_routes(user_routes)
                
    user.add_route(Route("index", "get", "/users", user, logic="new route logic"))
    self.assertEqual(2, len(user.get_routes()))
    self.assertEqual("new route logic", user.get_routes()[1].get_logic())

