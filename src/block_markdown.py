from enum import Enum

from htmlnode import ParentNode

from textnode import textnode_to_htmlnode

from inline_markdown import text_to_textnode


class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"
    PARAGRAPH = "paragraph"


def markdown_to_blocks(markdown):
    block_list = []
    split_list = markdown.split("\n\n")
    for item in split_list:
        item = item.strip()
        if item:
            block_list.append(item)
    return block_list


def block_to_blocktype(block):
    block_type = None
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        block_type = BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        block_type = BlockType.CODE
    elif block.startswith(">"):
        block_type = BlockType.QUOTE
        split_block = block.split("\n")
        for line in split_block:
            if not line.startswith(">"):
                block_type = BlockType.PARAGRAPH
                break
    elif block.startswith("* ") or block.startswith("- "):
        block_type = BlockType.UL
        split_block = block.split("\n")
        for line in split_block:
            if not line.startswith("* ") and not line.startswith("- "):
                block_type = BlockType.PARAGRAPH
                break
    elif block.startswith("1. "):
        block_type = BlockType.OL
        split_block = block.split("\n")
        expected_number = 1
        for line in split_block:
            if not line.startswith(f"{expected_number}. "):
                block_type = BlockType.PARAGRAPH
                break
            expected_number += 1
    else:
        block_type = BlockType.PARAGRAPH
    return block_type


def markdown_to_htmlnode(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_htmlnode(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_htmlnode(block):
    block_type = block_to_blocktype(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_htmlnode(block)
    if block_type == BlockType.CODE:
        return code_to_htmlnode(block)
    if block_type == BlockType.OL:
        return olist_to_htmlnode(block)
    if block_type == BlockType.UL:
        return ulist_to_htmlnode(block)
    if block_type == BlockType.QUOTE:
        return quote_to_htmlnode(block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnode(text)
    children = []
    for text_node in text_nodes:
        html_node = textnode_to_htmlnode(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_htmlnode(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_htmlnode(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_htmlnode(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_htmlnode(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_htmlnode(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)