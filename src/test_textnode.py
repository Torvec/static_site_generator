import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
    
    def test_not_eq(self):
        node1 = TextNode("This is a test", TextType.BOLD)
        node2 = TextNode("This is a test", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_url_none(self):
        node = TextNode("This is a test", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_url_not_none(self):
        node = TextNode("Yo", TextType.LINK, "https://www.boot.dev")
        self.assertIsNotNone(node.url)
    
    def test_repr(self):
        node = TextNode("This is a test", TextType.TEXT, "https://www.boot.dev/")
        self.assertEqual(repr(node), "TextNode(This is a test, text, https://www.boot.dev/)")


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_invalid_text_type(self):
        text_node = TextNode("Stop! Error Time!", "WTF")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), f"Invalid text type: {text_node.text_type}")

    def test_text_output(self):
        text_node = TextNode("Just Text", TextType.TEXT)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, None)
        self.assertEqual(leaf_node.value, "Just Text")

    def test_bold_output(self):
        text_node = TextNode("Bold Text", TextType.BOLD)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "b")
        self.assertEqual(leaf_node.value, "Bold Text")

    def test_italic_output(self):
        text_node = TextNode("Italic Text", TextType.ITALIC)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "i")
        self.assertEqual(leaf_node.value, "Italic Text")

    def test_code_output(self):
        text_node = TextNode("Code Text", TextType.CODE)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "code")
        self.assertEqual(leaf_node.value, "Code Text")

    def test_link_output(self):
        text_node = TextNode("Link Text", TextType.LINK, "https://www.boot.dev/")
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "a")
        self.assertEqual(leaf_node.value, "Link Text")
        self.assertEqual(leaf_node.props, {"href": "https://www.boot.dev/"})

    def test_image_output(self):
        text_node = TextNode("Alt Text", TextType.IMAGE, "/public/boots.png")
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "img")
        self.assertEqual(leaf_node.value, "")
        self.assertEqual(leaf_node.props, {"src": "/public/boots.png", "alt": "Alt Text"})


if __name__ == "__main__":
    unittest.main()