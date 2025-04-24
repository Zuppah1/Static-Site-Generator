import unittest
from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# This is a title"
        result = extract_title(markdown)
        expected = "This is a title"
        self.assertEqual(result, expected)

    def test_extract_title_nottitle(self):
        markdown = "## This is not a title"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "missing title")