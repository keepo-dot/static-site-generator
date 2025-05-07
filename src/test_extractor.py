import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_success(self):
        markdown = "# My Title\nMore text here"
        self.assertEqual(extract_title(markdown), "My Title")

    def test_extract_title_missing_header(self):
        markdown = "No headers here!"
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()

