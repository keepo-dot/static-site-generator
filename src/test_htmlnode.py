import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html_with_single_prop(self):
        # Test with a single property
        node = HTMLNode("a", "Click me!", None, {"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')
    
    def test_props_to_html_with_multiple_props(self):
        # Test with multiple properties
        node = HTMLNode("a", "Click me!", None, {
            "href": "https://example.com",
            "target": "_blank"
        })
        # The order of properties in a dictionary is not guaranteed,
        # so we need to check both possibilities
        possible_outputs = [
            ' href="https://example.com" target="_blank"',
            ' target="_blank" href="https://example.com"'
        ]
        self.assertIn(node.props_to_html(), possible_outputs)
    
    def test_props_to_html_with_no_props(self):
        # Test with no properties
        node = HTMLNode("p", "Hello, world!", None, None)
        self.assertEqual(node.props_to_html(), "")
    
    def test_repr_method(self):
        # Test the __repr__ method
        node = HTMLNode("div", "Content", None, {"class": "container"})
        # The exact format can vary, but it should include all the attributes
        repr_str = repr(node)
        self.assertIn("div", repr_str)
        self.assertIn("Content", repr_str)
        self.assertIn("container", repr_str)

if __name__ == "__main__":
    unittest.main()
