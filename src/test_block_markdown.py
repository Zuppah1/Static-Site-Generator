import unittest
from block_markdown import (
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_triple_space(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_one_paragraph(self):
        md = """




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line"
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        string = "This is a regular paragraph"
        result = BlockType.PARAGRAPH
        block = block_to_block_type(string)
        self.assertEqual(block, result)

    def test_block_to_block_type_code(self):
        string = "```This is a block of code```"
        result = BlockType.CODE
        block = block_to_block_type(string)
        self.assertEqual(block, result)

    def test_block_to_block_type_quote(self):
        string = ">This is a" \
        ">quote block" \
        ">with several lines"
        result = BlockType.QUOTE
        block = block_to_block_type(string)
        self.assertEqual(block, result)

    def test_block_to_block_type_ordered(self):
        string = "1. This" \
        "2. is an ordered" \
        "3. list"
        result = BlockType.OLIST
        block = block_to_block_type(string)
        self.assertEqual(block, result)

    def test_block_to_block_type_unordered(self):
        string = "- This" \
        "- is an unordered" \
        "- list"
        result = BlockType.ULIST
        block = block_to_block_type(string)
        self.assertEqual(block, result)

    def test_block_to_block_type_heading(self):
        string = "#### This is a heading"
        result = BlockType.HEADING
        block = block_to_block_type(string)
        self.assertEqual(block, result)
    
    def test_block_to_block_type_bad_syntax1(self):
        string = "######### This is a bad heading, hence its a paragraph"
        result = BlockType.PARAGRAPH
        block = block_to_block_type(string)
        self.assertEqual(block, result)

    def test_block_to_block_type_bad_syntax2(self):
        string = "```This is a bad code block, hence its a paragraph"
        result = BlockType.PARAGRAPH
        block = block_to_block_type(string)
        self.assertEqual(block, result)

    def test_block_to_block_type_bad_syntax3(self):
        string = " >This is a bad quote block, \n>hence its a paragraph"
        result = BlockType.PARAGRAPH
        block = block_to_block_type(string)
        self.assertEqual(block, result)

    def test_block_to_block_type_bad_syntax4(self):
        string = "1. This is a bad ordered list block,\n1. hence its a paragraph"
        result = BlockType.PARAGRAPH
        block = block_to_block_type(string)
        self.assertEqual(block, result)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
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

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
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

        node = markdown_to_html_node(md)
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

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    