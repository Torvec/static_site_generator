import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_is_empty(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    def test_is_not_empty(self):
        node = HTMLNode("p")
        self.assertIsNotNone(node)
    
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
            "id": "testing"
        }
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank" id="testing"')
    
    def test_repr(self):
        tag = "p"
        value = "Some Value"
        children = []
        props = {"id":"test"}
        node = HTMLNode(tag=tag, value=value, children=children, props=props)
        self.assertEqual(node.__repr__(), f"HTMLNode (Tag: {tag} Value: {value} Children: {children} Props: {props})")

if __name__ == "__main__":
    unittest.main()