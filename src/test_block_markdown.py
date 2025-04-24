import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

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
        result = BlockType.ORDERED_LIST
        block = block_to_block_type(string)
        self.assertEqual(block, result)

    def test_block_to_block_type_unordered(self):
        string = "- This" \
        "- is an unordered" \
        "- list"
        result = BlockType.UNORDERED_LIST
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
    