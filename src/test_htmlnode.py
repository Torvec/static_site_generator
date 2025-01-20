import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        self.assertEqual(str(context.exception), "to_html method not implemented")


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


class TestParentNode(unittest.TestCase):
    def test_tag_err(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode("", children, None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "A tag is required")

    def test_children_err(self):
        children = []
        node = ParentNode("p", children, None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Children are required")

    def test_one_child_output(self):
        children = [
            LeafNode("b", "Bold text"),
        ]
        node = ParentNode("p", children, None)
        self.assertEqual(node.to_html(), '<p><b>Bold text</b></p>')

    def test_multi_child_output(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode("p", children, {"id":"intro"})
        self.assertEqual(node.to_html(), '<p id="intro"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_multi_parent_and_child_output(self):
        nested_children = [
            LeafNode("a", "A link", {"href":"https://www.boot.dev/", "target":"_blank"}),
            LeafNode(None, "Normal text"),
        ]
        children = [
            ParentNode("p", nested_children, None),
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode("div", children, {"class":"wrapper", "id":"content"})
        self.assertEqual(node.to_html(), '<div class="wrapper" id="content"><p><a href="https://www.boot.dev/" target="_blank">A link</a>Normal text</p><b>Bold text</b>Normal text</div>')

    def test_nested_parent_child_output(self):
        children_five = [
            LeafNode("a", "Contact", {"href":"/contact"})
        ]
        children_four = [
            LeafNode("a", "About", {"href":"/about"})
        ]
        children_three = [
            LeafNode("a", "Home", {"href":"/home"})
        ]
        children_two = [
            ParentNode("li", children_three, None),
            ParentNode("li", children_four, None),
            ParentNode("li", children_five, None)
        ]
        children_one = [
            ParentNode("ul", children_two, None)
        ]
        node = ParentNode("nav", children_one, {"class":"navlist", "id":"navbar"})
        self.assertEqual(node.to_html(), '<nav class="navlist" id="navbar"><ul><li><a href="/home">Home</a></li><li><a href="/about">About</a></li><li><a href="/contact">Contact</a></li></ul></nav>')

    def test_nested_parent_tag_err(self):
        children_five = [
            LeafNode("a", "Contact", {"href":"/contact"})
        ]
        children_four = [
            LeafNode("a", "About", {"href":"/about"})
        ]
        children_three = [
            LeafNode("a", "Home", {"href":"/home"})
        ]
        children_two = [
            ParentNode("li", children_three, None),
            ParentNode("li", children_four, None),
            ParentNode("", children_five, None)
        ]
        children_one = [
            ParentNode("ul", children_two, None)
        ]
        node = ParentNode("nav", children_one, {"class":"navlist", "id":"navbar"})
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "A tag is required")
        
    def test_nested_parent_child_err(self):
        children_five = []
        children_four = [
            LeafNode("a", "About", {"href":"/about"})
        ]
        children_three = [
            LeafNode("a", "Home", {"href":"/home"})
        ]
        children_two = [
            ParentNode("li", children_three, None),
            ParentNode("li", children_four, None),
            ParentNode("li", children_five, None)
        ]
        children_one = [
            ParentNode("ul", children_two, None)
        ]
        node = ParentNode("nav", children_one, {"class":"navlist", "id":"navbar"})
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Children are required")


if __name__ == "__main__":
    unittest.main()