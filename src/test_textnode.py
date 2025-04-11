import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq_text(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is also a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_uneq_texttype(self):
        node =  TextNode("This is a node.", TextType.BOLD)
        node2 = TextNode("This is a node.", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_behavior(self):
        node = TextNode("This is a URL Node.", TextType.LINK, "https://wiki.archlinux.org/title/Main_page")
        node2 = TextNode("This is a URL Node with no URL.", TextType.LINK)
        node3 = TextNode("Text", TextType.LINK, "https://example.com")
        node4 = TextNode("Text", TextType.LINK, "https://example.com")
        self.assertIsNone(node2.url)
        self.assertEqual(node3, node4)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node.url, None)

    def test_mixed_props(self):
        node = TextNode("This is a test node.", TextType.NORMAL,"https://archlinux.org/")
        node2 = TextNode("This is a test node.", TextType.BOLD, "https://archlinux.org/")
        node3 = TextNode("This is a test node as well.", TextType.LINK, "https://www.google.com")
        node6 = TextNode("This is a test node.", TextType.NORMAL, "https://archlinux.org/")
        node7 = TextNode("This is a test node.", TextType.NORMAL, "https://www.gnu.org/")
        node8 = TextNode("Completely different text.", TextType.NORMAL, "https://archlinux.org/")

# Testing that similar properties result in equality
        self.assertEqual(node6, node)

# Ensuring inequality when only the URL changes
        self.assertNotEqual(node, node7)

# Ensuring inequality when only the text changes
        self.assertNotEqual(node, node8)
        self.assertNotEqual(node3, node2)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)



if __name__ == "__main__":
    unittest.main()
