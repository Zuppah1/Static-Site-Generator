import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_2(self):
        node = TextNode("Test number 2", TextType.ITALIC)
        node2 = TextNode("Test number 2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_3(self):
        node = TextNode("Test number 3", TextType.TEXT)
        node2 = TextNode("This is different", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_4(self):
        node = TextNode("Test number 4", TextType.TEXT, "https://www.boot.dev")
        node2 = TextNode("Test number 4", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_5(self):
        node = TextNode("Test number 5", TextType.CODE, "https://www.boot.dev")
        node2 = TextNode("Test number 5", TextType.CODE, "https://www.boot.dev")
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()