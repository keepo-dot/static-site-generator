import unittest
from textnode import TextType, TextNode
from htmlnode import LeafNode
# Import your converter function from wherever you placed it
from converter import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, markdown_to_blocks

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

class TestSPlitShit(unittest.TestCase):

    def test_no_links(self):
        node = TextNode("This is plain text with no links.", TextType.NORMAL)
        result = split_nodes_link([node])
        self.assertListEqual(result, [node])

    def test_multiple_links(self):
        node = TextNode(
            "Here is [link one](http://example1.com) and [link two](http://example2.com).",
            TextType.NORMAL,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("Here is ", TextType.NORMAL),
            TextNode("link one", TextType.LINK, "http://example1.com"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("link two", TextType.LINK, "http://example2.com"),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertListEqual(result, expected)

    def test_malformed_links(self):
        node = TextNode(
            "Here is a [link without closing brackets](http://example.com",
            TextType.NORMAL,
        )
        result = split_nodes_link([node])
        self.assertListEqual(result, [node])  # Malformed content should remain untouched


    def test_split_single_image(self):
        node = TextNode(
            "This text has an ![image](http://example.com/image.png).",
            TextType.NORMAL,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("This text has an ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "http://example.com/image.png"),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertListEqual(result, expected)

    def test_no_images(self):
        node = TextNode("This is plain text with no images.", TextType.NORMAL)
        result = split_nodes_image([node])
        self.assertListEqual(result, [node])
    def test_split_single_link(self):
        # Input node contains one link
        node = TextNode(
            "This is text with a [link](https://www.example.com)",
            TextType.NORMAL,
        )
        result = split_nodes_link([node])
        
        # Expected split nodes
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://www.example.com"),
        ]
        
        self.assertListEqual(result, expected)


    def test_multiple_images(self):
        node = TextNode(
            "Here is one ![image1](http://example.com/image1.png) and another ![image2](http://example.com/image2.png).",
            TextType.NORMAL,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("Here is one ", TextType.NORMAL),
            TextNode("image1", TextType.IMAGE, "http://example.com/image1.png"),
            TextNode(" and another ", TextType.NORMAL),
            TextNode("image2", TextType.IMAGE, "http://example.com/image2.png"),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertListEqual(result, expected)

    def test_malformed_images(self):
        node = TextNode(
            "Here is an image with missing brackets ![image(http://example.com/image.png",
            TextType.NORMAL,
        )
        result = split_nodes_image([node])
        self.assertListEqual(result, [node])  # Malformed content should remain untouched

"""
    def test_empty_text(self):
        node = TextNode("", TextType.NORMAL)
        result = split_nodes_image([node])
        self.assertListEqual(result, [node])  # No work to do for an empty node
"""


def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )



if __name__ == "__main__":
    unittest.main()
