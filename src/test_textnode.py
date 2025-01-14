import unittest

from textnode import TextNode, TextType

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
        node = TextNode("Testing", TextType.NORMAL, "https://testing.com/")
        self.assertIsNotNone(node.url)
    
    def test_url_does_not_exist(self):
        node = TextNode("Testing", TextType.NORMAL)
        self.assertIsNone(node.url)

    def test_texttype_is_bold(self):
        node = TextNode("Testing again", TextType.BOLD, "https://testing.com/")
        self.assertEqual(node.text_type, TextType.BOLD)

if __name__ == "__main__":
    unittest.main()