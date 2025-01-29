import unittest
from TemplateParser.Model import Model
from TemplateParser.Route import Route

class TestRoute(unittest.TestCase):

  def test_index_route(self):
    route = Route("index", "get", "/users", None, protected=True, logic="some logic")

    expected = "some logic"
    actual = route.logic
    self.assertEqual(expected, actual)

  