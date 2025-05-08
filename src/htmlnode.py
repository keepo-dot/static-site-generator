


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props



    def to_html(self):
        raise NotImplementedError("To be implemented by child classes.")



    def props_to_html(self):
        result = ""
        if self.props == None:
            return ""
        if self.props:
            for key, value in self.props.items():
                result += f' {key}="{value}"'
            return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag)
        #if props is None:
        #    self.props = {}
        if value is None:
            raise ValueError("LeafNode must have a value.")
        self.value = value
        self.props = props


    def to_html(self):
        if self.value == None:
            print("DEBUG: node missing value:", self)
            raise ValueError("'value' property must contain a value.")
        if self.tag is None or self.tag == "":
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"




class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)



    def to_html(self):
        if not self.tag or self.tag == "":
            raise ValueError("ParentNode must have a tag.")
        if not self.children or self.children == "":
            raise ValueError("ParentNode must have children.")
        child_string = ""
        for child in self.children:
            child_string += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_string}</{self.tag}>"


def markdown_to_html_node(markdown):
    pass

