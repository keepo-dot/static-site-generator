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
