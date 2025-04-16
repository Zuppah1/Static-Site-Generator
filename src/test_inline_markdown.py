import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


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
        result = []
        self.assertEqual(delimited_node, result)

class TestExtract(unittest.TestCase): 
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

class TestImageLinkSplit(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_beginning_end(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) at the beginning and end [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" at the beginning and end ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_beginning_end(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) at the beginning and end ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" at the beginning and end ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_and_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://example.com) in it.",
            TextType.TEXT,
        )
        
        nodes_after_images = split_nodes_image([node])
        final_nodes = split_nodes_link(nodes_after_images)
        
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" in it.", TextType.TEXT),
            ],
            final_nodes,
        )

    def test_split_without_images_links(self):
        node = TextNode(
            "This is text without any images or links in it.",
            TextType.TEXT,
        )

        nodes_after_images = split_nodes_image([node])
        final_nodes = split_nodes_link(nodes_after_images)

        self.assertListEqual(
            [
                TextNode("This is text without any images or links in it.", TextType.TEXT)              
            ],
            final_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_all_in_one(self):
        node = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
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
            ],
            node
        )

    def test_no_text(self):
        node = text_to_textnodes("**text** _italic_ `code block` ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("text", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code block", TextType.CODE),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            node
        )

    def test_just_text(self):
        node = text_to_textnodes("This is plain text without any markdown")
        self.assertListEqual(
            [
                TextNode("This is plain text without any markdown", TextType.TEXT),
            ],
            node
        )

    def test_empty_input(self):
        node = text_to_textnodes("")
        self.assertListEqual([], node)