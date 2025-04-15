import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()