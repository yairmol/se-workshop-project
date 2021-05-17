import unittest

from domain.commerce_system.product import Product
from domain.commerce_system.search_engine import levenshtein_distance, search_by_categories, is_similar_words, \
    search_by_product_name

products = [
    Product("bamba", 5, "bamba by osem", 1, ["snacks"]),
    Product("my_chair", 50, "chair in your style", 1, ["furniture"]),
    Product("mountain bike", 1000, "bike, for the mountains", 1, ["vehicle", "toy"]),
]


class SearchEngineTests(unittest.TestCase):
    def test_edit_distance1(self):
        self.assertEqual(levenshtein_distance("aaa", "aaa"), 0)

    def test_edit_distance_insertions(self):
        self.assertEqual(levenshtein_distance("aabba", "aaa"), 2)

    def test_edit_distance_replacements(self):
        self.assertEqual(levenshtein_distance("abcsa", "aaaaa"), 3)

    def test_edit_distance(self):
        self.assertEqual(levenshtein_distance("Charlie Goes Down After Eating BreakFest",
                                               "Chaarlie Boes own Aftr Eatin BreaakFeest"), 7)

    def test_is_similar_words(self):
        self.assertTrue(is_similar_words("word1", "word2"))

    def test_is_un_similar_words(self):
        self.assertFalse(is_similar_words("someone", "another"))
        self.assertFalse(is_similar_words("osem", "elit"))

    def test_search_by_category(self):
        self.assertEqual(search_by_categories(products, products[1].categories), [products[1]])
        self.assertEqual(search_by_categories(products, ["furniters"]), [products[1]])
        self.assertEqual(search_by_categories(products, ["future"]), [])

    def test_search_by_product_name(self):
        self.assertEqual(search_by_product_name(products, products[0].product_name), [products[0]])
        self.assertEqual(search_by_product_name(products, "noname"), [])
        self.assertEqual(search_by_product_name(products, "mount bike"), [products[2]])
