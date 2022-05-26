import unittest
from src.categorizing.categorizer import EmptyCategorizer

class TestEmptyCategorizer(unittest.TestCase):
    def test_empty_categorizer(self):
        categorizer = EmptyCategorizer()
        category1 = categorizer.categorize("", "", None, {})
        category2 = categorizer.categorize("string", "string2", None, {})
        category3 = categorizer.categorize("string", "string2", None, {"content": "string3"})
        category4 = categorizer.categorize("string", "string2", {"type": "RegularGroup"}, {"content": "string4"})
        self.assertEqual(category1, category2)
        self.assertEqual(category1, category3)
        self.assertEqual(category1, category4)