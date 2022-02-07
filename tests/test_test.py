import sys
import unittest
from unittest import result
from src.scrapers import wiki_scrapers as ws

wsc = ws.WikiContentScraper()

class TestMerge(unittest.TestCase):
    def test_merge(self):
        a = {1:{2:3}}
        b = {1:{4:5}}
        result = wsc.merge(a,b)
        self.assertEqual(result, {1:{2:3, 4:5}})
        ### also write test for dicts with different keys and recursive calls

if __name__ == "__main__":
    # sys.path.append("src/scrapers")
    print(sys.path)
    unittest.main()