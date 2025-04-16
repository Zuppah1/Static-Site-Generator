import unittest

from htmlnode import HTMLNode, LeafNode, text_node_to_html_node, TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_href(self):
        node = HTMLNode(props={"href": "https://example.com"})
        expected = ' href="https://example.com"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_with_mutiple_props(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertTrue(' href="https://example.com"' in result)
        self.assertTrue(' target="_blank"' in result)
        self.assertEqual(len(result), len(' href="https://example.com" target="_blank"'))

    def test_props_to_html_with_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

class TestTEXTtoHTML(unittest.TestCase):

    def test_text_node_to_html_node_with_text(self):
        text_node = TextNode("Hello World", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "Hello World")
        self.assertIsNone(html_node.tag)  

    def test_text_node_to_html_node_with_bold(self):
        text_node = TextNode("Hello World", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "Hello World")
        self.assertEqual(html_node.tag, "b")

    def test_text_node_to_html_node_with_italic(self):
        text_node = TextNode("Hello World", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "Hello World")
        self.assertEqual(html_node.tag, "i")

    def test_text_node_to_html_node_with_code(self):
        text_node = TextNode("Hello World", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "Hello World")
        self.assertEqual(html_node.tag, "code")  

    def test_text_node_to_html_node_with_link(self):
        text_node = TextNode("Hello World", TextType.LINK, "something.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "Hello World")
        self.assertEqual(html_node.tag, "a") 
        self.assertEqual(html_node.props, {"href":'something.com'})

    def test_text_node_to_html_node_with_image(self):
        text_node = TextNode("Hello World", TextType.IMAGE, "something.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.tag, "img") 
        self.assertEqual(html_node.props, {"src":'something.com', "alt":"Hello World"})


if __name__ == "__main__":
    unittest.main()