import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode("p", "The Value", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_one_prop_to_html(self):
        node = HTMLNode("p", "The Value", None, {"id": "paragraph"})
        self.assertEqual(node.props_to_html(), ' id="paragraph"')

    def test_multiple_props_to_html(self):
        node = HTMLNode("p", "The Value", None, {"id":"paragraph", "class":"intro"})
        self.assertEqual(node.props_to_html(), ' id="paragraph" class="intro"')

    def test_not_implemented_err(self):
        node = HTMLNode("p", "yo", None, None)
        with self.assertRaises(NotImplementedError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Method not implemented")

if __name__ == "__main__":
    unittest.main()