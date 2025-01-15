class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if isinstance(self.props, dict):
            props_list = []
            for key, value in self.props.items():
                prop_str = f'{key}="{value}"'
                props_list.append(prop_str)
            return " " + " ".join(props_list)
        return ""
    
    def __repr__(self):
        return f"HTMLNode (Tag: {self.tag} Value: {self.value} Children: {self.children} Props: {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("Value is required!")
        if self.tag == None:
            return f"{self.value}"
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is required!")
        if not self.children:
            raise ValueError("No Children Found!")
        children = ''
        for child in self.children:
            children += child.to_html()
        if self.props == None:
            return f"<{self.tag}>{children}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{children}</{self.tag}>"