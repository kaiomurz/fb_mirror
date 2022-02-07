import unittest
from unittest import result
from wiki_scrapers import WikiContentScraper as ws


class TestMerge(unittest.TestCase):
    def test_merge(self):
        a = {1:{2:3}}
        b = {1:{4:5}}
        result = ws.merge(a,b)
        self.assertEqual(result, {1:{2:3, 4:5}})

if __name__ == "__main__":
    unittest.main()