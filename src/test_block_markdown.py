import unittest

from block_markdown import BlockType, markdown_to_blocks, block_to_blocktype, markdown_to_htmlnode


class TestMarkdownToBlock(unittest.TestCase):
    def test_expected_output(self):
        input_markdown = '''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item'''
        expected_output = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item", 
        ]
        self.assertEqual(markdown_to_blocks(input_markdown), expected_output)

    def test_excessive_line_breaks(self):
        input_markdown = '''# This is a heading







This is a paragraph of text. It has some **bold** and *italic* words inside of it.'''
        expected_output = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
        ]
        self.assertEqual(markdown_to_blocks(input_markdown), expected_output)
        

class TestBlockToBlockType(unittest.TestCase):
    def test_expected_output(self):
        hdr = "# This is a heading"
        self.assertEqual(block_to_blocktype(hdr), BlockType.HEADING)

        hdr = "## This is a heading"
        self.assertEqual(block_to_blocktype(hdr), BlockType.HEADING)

        hdr = "### This is a heading"
        self.assertEqual(block_to_blocktype(hdr), BlockType.HEADING)

        hdr = "#### This is a heading"
        self.assertEqual(block_to_blocktype(hdr), BlockType.HEADING)

        hdr = "##### This is a heading"
        self.assertEqual(block_to_blocktype(hdr), BlockType.HEADING)

        hdr = "###### This is a heading"
        self.assertEqual(block_to_blocktype(hdr), BlockType.HEADING)

        code = """```python
        print("Hello, world!")
        ```"""
        self.assertEqual(block_to_blocktype(code), BlockType.CODE)

        quote = "> This is a quote\n> This is also a quote\n> Another quote"
        self.assertEqual(block_to_blocktype(quote), BlockType.QUOTE)

        ul = "* This is a list item\n* This is another list item\n* and another one"
        self.assertEqual(block_to_blocktype(ul), BlockType.UL)

        ul = "- This is a list item\n- This is another list item\n- and another one"
        self.assertEqual(block_to_blocktype(ul), BlockType.UL)

        ol = "1. This is a list item\n2. This is another list item\n3. and another one"
        self.assertEqual(block_to_blocktype(ol), BlockType.OL)

        self.assertEqual(block_to_blocktype("This is a paragraph"), BlockType.PARAGRAPH)
        
        self.assertEqual(block_to_blocktype(""), BlockType.PARAGRAPH)
        
        self.assertEqual(block_to_blocktype("    "), BlockType.PARAGRAPH)
    
    def test_invalid_quote_block_output(self):
        quote = "> Yes\n>Also yes\n+No?"
        self.assertEqual(block_to_blocktype(quote), BlockType.PARAGRAPH)
    
    def test_invalid_unordered_list_block_output(self):
        ul = "* Yes\nx Nope\n* yes"
        self.assertEqual(block_to_blocktype(ul), BlockType.PARAGRAPH)

    def test_invlaid_ordered_list_block_output(self):
        ol = "1. yep\n5. nah bruh\n3. I count good"
        self.assertEqual(block_to_blocktype(ol), BlockType.PARAGRAPH)


    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


if __name__ == "__main__":
    unittest.main()