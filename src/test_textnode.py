import unittest

from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()