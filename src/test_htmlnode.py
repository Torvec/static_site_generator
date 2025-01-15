import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_HTMLNode_is_empty(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    def test_HTMLNode_is_not_empty(self):
        node = HTMLNode("p")
        self.assertIsNotNone(node)
    
    def test_HTMLNode_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
            "id": "testing"
        }
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank" id="testing"')
    
    def test_HTMLNode_repr(self):
        tag = "p"
        value = "Some Value"
        children = []
        props = {"id":"test"}
        node = HTMLNode(tag=tag, value=value, children=children, props=props)
        self.assertEqual(node.__repr__(), f"HTMLNode (Tag: {tag} Value: {value} Children: {children} Props: {props})")

class TestLeafNode(unittest.TestCase):
    def test_LeafNode_value_err(self):
        node = LeafNode(tag=None, value=None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_LeafNode_text_output(self):
        tag=None
        value = "Some Text For Ya"
        node = LeafNode(tag=tag, value=value)
        self.assertEqual(node.to_html(), f"{value}")

    def test_LeafNode_tag_no_attr_output(self):
        tag = "p"
        value = "Some values yo"
        node = LeafNode(tag=tag, value=value)
        self.assertEqual(node.to_html(), f"<{tag}>{value}</{tag}>")

    def test_LeafNode_tag_output(self):
        tag = "p"
        value = "Text In a Tag"
        props = {"class":"text"}
        node = LeafNode(tag=tag, value=value, props=props)
        self.assertEqual(node.to_html(), f"<{tag} {node.props_to_html()}>{value}</{tag}>")

if __name__ == "__main__":
    unittest.main()