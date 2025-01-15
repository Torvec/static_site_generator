import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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
        self.assertEqual(node.__repr__(), "HTMLNode(p, Some Value, children: [], {'id': 'test'})")

class TestLeafNode(unittest.TestCase):
    def test_LeafNode_value_err(self):
        node = LeafNode(tag=None, value=None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: no value")
    
    def test_LeafNode_text_output(self):
        tag=None
        value = "Some Text For Ya"
        node = LeafNode(tag=tag, value=value)
        self.assertEqual(node.to_html(), "Some Text For Ya")

    def test_LeafNode_tag_no_attr_output(self):
        tag = "p"
        value = "Some values yo"
        node = LeafNode(tag=tag, value=value)
        self.assertEqual(node.to_html(), "<p>Some values yo</p>")

    def test_LeafNode_tag_output(self):
        tag = "p"
        value = "Text In a Tag"
        props = {"class":"text"}
        node = LeafNode(tag=tag, value=value, props=props)
        self.assertEqual(node.to_html(), '<p class="text">Text In a Tag</p>')

class TestParentNode(unittest.TestCase):
    def test_ParentNode_no_tag_err(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode(tag=None, children=children)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: no tag")

    def test_ParentNode_no_children_err(self):
        tag = "p"
        node = ParentNode(tag=tag, children=None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: no children")

    def test_ParentNode_output(self):
        tag = "p"
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode(tag=tag, children=children)
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_ParentNode_nested_output(self):
        tag = 'p'
        children = [
            ParentNode(
                tag = "a",
                children = [
                    LeafNode(None, "Google")
                ],
                props = {
                    "href": "https://google.com/",
                    "target": "_blank"    
                },
            ),
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        props = {"id":"test"}
        node = ParentNode(tag=tag, children=children, props=props)
        self.assertEqual(node.to_html(), '<p id="test"><a href="https://google.com/" target="_blank">Google</a><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

if __name__ == "__main__":
    unittest.main()