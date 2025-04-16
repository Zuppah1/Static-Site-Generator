import unittest

from textnode import TextNode, TextType
from split_delimeter import split_nodes_delimiter

class TestDelimiter(unittest.TestCase):
    def test_delimited_CodeinText(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        delimited_node = split_nodes_delimiter([node], "`", TextType.CODE)
        result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(delimited_node, result)
    
    def test_delimited_ItalicInText(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        delimited_node = split_nodes_delimiter([node], "_", TextType.ITALIC)
        result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(delimited_node, result)

    def test_delimited_BoldInText(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        delimited_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(delimited_node, result)

    def test_delimited_multiple_CodeInText(self):
        node = TextNode("This is text with two `code blocks` separated by `regular text` in a string", TextType.TEXT)
        delimited_node = split_nodes_delimiter([node], "`", TextType.CODE)
        result = [
            TextNode("This is text with two ", TextType.TEXT),
            TextNode("code blocks", TextType.CODE),
            TextNode(" separated by ", TextType.TEXT),
            TextNode("regular text", TextType.CODE),
            TextNode(" in a string", TextType.TEXT),
        ]
        self.assertEqual(delimited_node, result)

    def test_delimited_no_delimiters(self):
        node = TextNode("This is text with no delimiters", TextType.TEXT)
        delimited_node = split_nodes_delimiter([node], "`", TextType.CODE)
        result = [
            TextNode("This is text with no delimiters", TextType.TEXT),
        ]
        self.assertEqual(delimited_node, result)

    def test_delimited_not_TEXT(self):
        node = TextNode("This is code", TextType.CODE)
        delimited_node = split_nodes_delimiter([node], "`", TextType.CODE)
        result = [
            TextNode("This is code", TextType.CODE),
        ]
        self.assertEqual(delimited_node, result)

    def test_delimited_list_of_nodes(self):
        nodes = [
            TextNode("First with `code`", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("More `code1` and `code2`", TextType.TEXT)
        ]
        delimited_node = split_nodes_delimiter(nodes, "`", TextType.CODE)
        result = [
            TextNode("First with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("Bold text", TextType.BOLD),
            TextNode("More ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE)
        ]
        self.assertEqual(delimited_node, result)

    def test_delimited_missing_delimiter(self):
        node = TextNode("This is text with a **bold block word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delimited_empty_list(self):
        node = []
        delimited_node = split_nodes_delimiter(node, "`", TextType.CODE)
        result = []
        self.assertEqual(delimited_node, result)

    def test_delimited_empty_string(self):
        node = TextNode("", TextType.TEXT)
        delimited_node = split_nodes_delimiter([node], "`", TextType.CODE)
        result = []
        self.assertEqual(delimited_node, result)

    def test_delimited_EmptyBold(self):
        node = TextNode("****", TextType.TEXT)
        delimited_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        result = [
            TextNode("", TextType.BOLD), 
        ]
        self.assertEqual(delimited_node, result)
