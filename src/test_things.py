from converter import *
from textnode import TextNode



node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
node2 = "This is _italic_ text."

matches = textnodes_to_text(node)


print(matches)
