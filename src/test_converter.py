import unittest
from textnode import TextType, TextNode
from htmlnode import LeafNode
# Import your converter function from wherever you placed it
from converter import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node(self):
        # Test for normal text conversion
        node = TextNode("This is normal text", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is normal text")
        self.assertEqual(html_node.props, {})

    def test_bold_node(self):
        # Test for bold text conversion
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.props, {})

    def test_italic_node(self):
        # Test for italic text conversion
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.props, {})

    def test_code_node(self):
        # Test for code text conversion
        node = TextNode("print('Hello World')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello World')")
        self.assertEqual(html_node.props, {})
    
    def test_link_node(self):
        # Test for link conversion
        node = TextNode("Click here", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})

    def test_image_node(self):
        # Test for image conversion
        node = TextNode("An image description", TextType.IMAGE, "https://www.example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
            "src": "https://www.example.com/image.jpg",
            "alt": "An image description"
        })

    def test_invalid_type(self):
        # Create a fake text type that doesn't exist in our enum
        # This is a bit tricky since we're using an Enum, but we can test the exception
        # by creating a node and modifying its text_type after creation
        node = TextNode("Some text", TextType.NORMAL)
        
        # Here we're just testing that an exception is raised for an unsupported type
        # You might need to adjust this based on how you implement your error handling
        with self.assertRaises(Exception):
            # Let's say we want to test with an invalid text_type
            # This is a hacky way to create an invalid scenario
            # In a real test you might mock this or use a different approach
            node.text_type = "InvalidType"
            text_node_to_html_node(node)



class TestSplitDelimiter(unittest.TestCase):
    def test_code_delimit(self):
        node = TextNode("This is `code` in text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "This is "
        assert new_nodes[0].text_type == TextType.NORMAL
        assert new_nodes[1].text == "code"
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text == " in text"
        assert new_nodes[2].text_type == TextType.NORMAL

    def test_bold_delimit(self):
        node = TextNode("A **bold** statement", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "A "
        assert new_nodes[0].text_type == TextType.NORMAL
        assert new_nodes[1].text == "bold"
        assert new_nodes[1].text_type == TextType.BOLD
        assert new_nodes[2].text == " statement"
        assert new_nodes[2].text_type == TextType.NORMAL

    def test_no_delimiter(self):
        node = TextNode("No special delimiters here", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 1
        assert new_nodes[0].text == "No special delimiters here"
        assert new_nodes[0].text_type == TextType.NORMAL

    def test_delimit_exception(self):
        with self.assertRaises(Exception):
            split_nodes_delimiter([invalid_node], "**", TextType.BOLD)
            invalid_node = TextNode("Mismatched **bold delimiters", TextType.NORMAL)


    def test_non_text_skip(self):
        non_normal_node = TextNode("Already bold node", TextType.BOLD)
        node_list = [non_normal_node]
        new_nodes = split_nodes_delimiter(node_list, "**", TextType.BOLD)
        assert len(new_nodes) == 1
        assert new_nodes[0].text == "Already bold node"
        assert new_nodes[0].text_type == TextType.BOLD
class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)





if __name__ == "__main__":
    unittest.main()
