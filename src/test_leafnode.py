import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_notag(self):
        node = LeafNode(None, "Just paste me RAW")
        self.assertEqual(node.to_html(), "Just paste me RAW")

    def test_leaf_to_html_verror(self):
        node = LeafNode("p", None, {"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()