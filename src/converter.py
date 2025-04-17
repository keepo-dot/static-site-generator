from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode
import re


def text_node_to_html_node(text_node):
    if text_node.text_type is TextType.NORMAL:
        return LeafNode(None, text_node.text)
    if text_node.text_type is TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type is TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type is TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type is TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type is TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise Exception("Invalid TextType")



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []
    for node in old_nodes:
        if delimiter not in node.text:
            return old_nodes
        if node.text_type is not TextType.NORMAL:
            new_node_list.append(node)

        if node.text_type is TextType.NORMAL:
            new_node_split = node.text.split(delimiter) 
            if len(new_node_split) < 2 or len(new_node_split) % 2 == 0:
                raise Exception("Invalid Markdown syntax")
            for i in range(0, len(new_node_split)):
                new_text_type = TextType.NORMAL if i % 2 == 0 else text_type
                new_text_node = TextNode(new_node_split[i], new_text_type)
                new_node_list.append(new_text_node)
    return new_node_list


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
