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
                prop_str = f' {key}="{value}"'
                props_list.append(prop_str)
            return ''.join(props_list)
        return ""
    
    def __repr__(self):
        return f"HTMLNode (Tag: {self.tag} Value: {self.value} Children: {self.children} Props: {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None or not self.value:
            raise ValueError
        if self.tag == None:
            return f"{self.value}"
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"