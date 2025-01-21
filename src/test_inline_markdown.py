import unittest

from textnode import TextType, TextNode

from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link,
    text_to_textnode,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_non_text_node_output(self):
        input_list = [
            TextNode("bold text", TextType.BOLD),
            TextNode("italic text", TextType.ITALIC),
            TextNode("code text", TextType.CODE),
        ]
        expected_output = [
            TextNode("bold text", TextType.BOLD),
            TextNode("italic text", TextType.ITALIC),
            TextNode("code text", TextType.CODE),
        ]
        self.assertEqual(split_nodes_delimiter(input_list, "", ""), expected_output)

    def test_no_matching_delimiter(self):
        input_list = [
            TextNode("This is **bold text", TextType.TEXT),
            TextNode("This is *italic* text", TextType.TEXT),
        ]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(input_list, "**", TextType.BOLD) 
        self.assertEqual(str(context.exception), "No matching delimiter found")

    def test_expected_bold_output(self):
        input_list = [
            TextNode("**This** is **bold** text", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode("This is some `code` text with some **bold** in it", TextType.TEXT),
        ]
        expected_output = [
            TextNode("", TextType.TEXT),
            TextNode("This", TextType.BOLD),
            TextNode(" is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode("This is some `code` text with some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(input_list, "**", TextType.BOLD), expected_output)

    def test_expected_code_output(self):
        input_list = [
            TextNode("**This** is **bold** text", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode("This is some `code` text with some **bold** in it", TextType.TEXT),
        ]
        expected_output = [
            TextNode("**This** is **bold** text", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode("This is some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text with some **bold** in it", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(input_list, "`", TextType.CODE), expected_output)

    def test_expected_italic_output(self):
        input_list = [
            TextNode("**This** is *italic* text", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("This is some `code` text with some *italics* in it", TextType.TEXT),
        ]
        nodes_after_bold = split_nodes_delimiter(input_list, "**", TextType.BOLD)
        final_nodes = split_nodes_delimiter(nodes_after_bold, "*", TextType.ITALIC)
        expected_output = [
            TextNode("", TextType.TEXT),
            TextNode("This", TextType.BOLD),
            TextNode(" is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("This is some `code` text with some ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(final_nodes, expected_output)

    def test_no_delimiter_found_output(self):
        input_list = [
            TextNode("This is **important**!", TextType.TEXT)
        ]
        expected_output = [
            TextNode("This is **important**!", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter(input_list, "`", TextType.CODE), expected_output)

    def test_empty_delimiter_output(self):
        input_list = [
            TextNode("This is ****!", TextType.TEXT)
        ]
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("", TextType.BOLD),
            TextNode("!", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(input_list, "**", TextType.BOLD), expected_output)


class TestExtractMarkdowImages(unittest.TestCase):
    def test_expected_output(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_expected_output(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])


class TestSplitNodesImage(unittest.TestCase):
    def test_expected_output(self): 
        input_list = [
            TextNode("![alt one](/image-one.png) some filler text. ![alt two](/image-two.png) some more filler text. ![alt three](/image-three.png)", TextType.TEXT),
            TextNode("Even more text, for testing.", TextType.TEXT)
        ]
        expected_output = [
            TextNode("alt one", TextType.IMAGE, "/image-one.png"),
            TextNode(" some filler text. ", TextType.TEXT),
            TextNode("alt two", TextType.IMAGE, "/image-two.png"),
            TextNode(" some more filler text. ", TextType.TEXT),
            TextNode("alt three", TextType.IMAGE, "/image-three.png"),
            TextNode("Even more text, for testing.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image(input_list), expected_output)


class TestSplitNodesLink(unittest.TestCase):
    def test_expected_output(self):
        input_list = [
            TextNode("[text one](https://www.one.org) some filler text. [text two](https://www.two.org) some more filler text. [text three](https://www.three.org)", TextType.TEXT),
            TextNode("Even more text, for testing.", TextType.TEXT)
        ]
        expected_output = [
            TextNode("text one", TextType.LINK, "https://www.one.org"),
            TextNode(" some filler text. ", TextType.TEXT),
            TextNode("text two", TextType.LINK, "https://www.two.org"),
            TextNode(" some more filler text. ", TextType.TEXT),
            TextNode("text three", TextType.LINK, "https://www.three.org"),
            TextNode("Even more text, for testing.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link(input_list), expected_output)


class TestTextToTextnode(unittest.TestCase):
    def test_expected_output(self):
        input_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnode(input_text), expected_output)


if __name__ == "__main__":
    unittest.main()