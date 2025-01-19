import unittest

from htmlnode import HTMLNode, LeafNode

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

class TestLeafNode(unittest.TestCase):
    def test_value_err(self):
        node = LeafNode("p", None, None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "A value is required")

    def test_text_output(self):
        node = LeafNode(None, "Raw Text Here", None)
        self.assertEqual(node.to_html(), "Raw Text Here")

    def test_html_output(self):
        node = LeafNode("p", "This is a paragraph", None)
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_html_output_with_props(self):
        node = LeafNode("p", "This is another paragraph", {"id":"paragraph", "class":"intro"})
        self.assertEqual(node.to_html(), '<p id="paragraph" class="intro">This is another paragraph</p>')

    def test_html_output_for_link(self):
        node = LeafNode("a", "A link", {"href":"https://www.boot.dev/", "target":"_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev/" target="_blank">A link</a>')

    def test_html_output_with_children(self):
        node = LeafNode("p", "Some Text", )

if __name__ == "__main__":
    unittest.main()