class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        string = ""
        if self.props == None:
            return string
        for prop, value in self.props.items():
            string += f' {prop}="{value}"'
        return string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("A value is required")
        if self.tag == None:
            return f"{self.value}"
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("A tag is required")
        if not self.children:
            raise ValueError("Children are required")
        children = []
        for child in self.children:
            children.append(child.to_html())
        joined = ''.join(children)
        return f"<{self.tag}{self.props_to_html()}>{joined}</{self.tag}>"