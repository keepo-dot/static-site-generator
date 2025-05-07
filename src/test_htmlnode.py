import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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
    
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )
    #Leaf node tests.
class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "print('Hello, world!'")
        self.assertEqual(node.to_html(), "<code>print('Hello, world!'</code>")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "shrugs")
        self.assertEqual(node.to_html(), "<i>shrugs</i>")

    def test_leaf_to_html_value_none(self):
        with self.assertRaises(ValueError):
            node = LeafNode("b", None)

    def test_leaf_to_html_tag_none(self):
        node = LeafNode("", "This should be raw text.")
        self.assertEqual(node.to_html(), "This should be raw text.")


#Parent Node tests
class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_multiple_children(self):
        children = [
            LeafNode("b", "Bold"),
            LeafNode(None, "Normal"),
            LeafNode("i", "Italic")
        ]
        parent = ParentNode("p", children)
        self.assertEqual(parent.to_html(), "<p><b>Bold</b>Normal<i>Italic</i></p>")

    def test_basic_parent_node(self):
        leaf = LeafNode("span", "Hello")
        parent = ParentNode("div", [leaf])
        self.assertEqual(parent.to_html(), "<div><span>Hello</span></div>")
    
    def test_parent_with_props(self):
        props = {"class": "container"}
        leaf = LeafNode("span", "Hello")
        parent = ParentNode("div", [leaf], props)
        self.assertTrue('class="container"' in parent.to_html())
        self.assertTrue('<span>Hello</span>' in parent.to_html())
    
    def test_missing_tag_error(self):
        leaf = LeafNode("span", "Hello")
        parent = ParentNode(None, [leaf])
        with self.assertRaises(ValueError):
            parent.to_html()
    
    def test_missing_children_error(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parent_with_mixed_children(self):
    # Create a nested parent node with its own child
        nested_child = LeafNode("b", "Bold text")
        nested_parent = ParentNode("strong", [nested_child])
    
    # Create a parent with multiple children, including the nested parent
        children = [
            LeafNode("span", "First child"),
            nested_parent,  # This is a parent node with its own child
            LeafNode(None, "Plain text"),
            LeafNode("em", "Emphasized")
        ]
        parent = ParentNode("div", children)
    
    # Test the resulting HTML structure
        expected = '<div><span>First child</span><strong><b>Bold text</b></strong>Plain text<em>Emphasized</em></div>'
        self.assertEqual(parent.to_html(), expected)



if __name__ == "__main__":
    unittest.main()
