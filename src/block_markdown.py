from enum import Enum

from htmlnode import ParentNode, text_node_to_html_node
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH= "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "ulist"
    OLIST = "olist"

def markdown_to_blocks(markdown):
    markdown_list = []
    split_list = markdown.split("\n\n")
    for block in split_list:
        block = block.strip()
        if not block:
            continue
        markdown_list.append(block)
    return markdown_list

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_block_type(block):
    if block.startswith("#") and " " in block and len(block.split(" ")[0]) <= 6:
        return BlockType.HEADING
    
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    elif all(line.startswith(">") for line in block.splitlines()):
        return BlockType.QUOTE
    
    elif all(line.startswith("- ") for line in block.splitlines()):
        return BlockType.ULIST
    
    elif all(line.split(". ")[0].isdigit() and int(line.split(". ")[0]) == i + 1 for i, line in enumerate(block.splitlines())):
        return BlockType.OLIST
    
    else:
        return BlockType.PARAGRAPH
    
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragprah = " ".join(lines)
    children = text_to_children(paragprah)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])\
    
def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

