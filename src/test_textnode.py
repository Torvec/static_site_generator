import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node1 = TextNode("This is text node 1", TextType.CODE)
        node2 = TextNode("This is text node 2", TextType.CODE)
        self.assertNotEqual(node1, node2)
    
    def test_url_exists(self):
        node = TextNode("Testing", TextType.TEXT, "https://testing.com/")
        self.assertIsNotNone(node.url)
    
    def test_url_does_not_exist(self):
        node = TextNode("Testing", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_texttype_is_bold(self):
        node = TextNode("Testing again", TextType.BOLD, "https://testing.com/")
        self.assertEqual(node.text_type, TextType.BOLD)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_conversion(self):
        node = TextNode("Just Text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Just Text")
        self.assertIsNone(html_node.props)

    def test_bold_node_conversion(self):
        node = TextNode("Bold Text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold Text")
        self.assertIsNone(html_node.props)

    def test_italic_node_conversion(self):
        node = TextNode("Italic Text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic Text")
        self.assertIsNone(html_node.props)

    def test_code_node_conversion(self):
        node = TextNode("It's Code yo", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "It's Code yo")
        self.assertIsNone(html_node.props)

    def test_link_node_conversion(self):
        node = TextNode("Link Text", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link Text")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_image_node_conversion(self):
        node = TextNode("Alt Text", TextType.IMAGE, "/public/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "/public/image.png", "alt": "Alt Text"})

if __name__ == "__main__":
    unittest.main()