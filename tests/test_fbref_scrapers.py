import unittest
from unittest import result
import pickle
import requests
from bs4 import BeautifulSoup
from src.scrapers import fbref_scrapers as fs

class TestClubURLScraper(unittest.TestCase):
    pass

class TestPlayerURLsScraper(unittest.TestCase):
    pass

class TestPlayerDataScraper(unittest.TestCase):
    
    def test_extract_data(self):
        pds = fs.PlayerDataScraper()

        with open('tests/fbref_scrapers_data/urls_dict.pickle', 'rb') as f:
            pds.urls_dict = pickle.load(f)

        pds.current_url = 'https://fbref.com/en/players/b66315ae/Gabriel-Jesus'
        pds.html = requests.get(pds.current_url).content
        pds.soup = BeautifulSoup(pds.html, 'html.parser')

        pds.extract_data()

        with open('tests/fbref_scrapers_data/personal_info_dict.pickle', 'rb') as f:
            expected_personal_info_dict = pickle.load(f)[42]

        self.assertEqual(pds.personal_info_dict[42]["name"], expected_personal_info_dict["name"])
        self.assertEqual(pds.personal_info_dict[42]["position"], expected_personal_info_dict["position"])
        self.assertEqual(pds.personal_info_dict[42]["footedness"], expected_personal_info_dict["footedness"])
        self.assertEqual(pds.personal_info_dict[42]["birth_date"], expected_personal_info_dict["birth_date"])



    def test_get_personal_info(self):       
        pds = fs.PlayerDataScraper()

        with open('tests/fbref_scrapers_data/urls_dict.pickle', 'rb') as f:
            pds.urls_dict = pickle.load(f)

        pds.current_url = 'https://fbref.com/en/players/b66315ae/Gabriel-Jesus'
        pds.soup = BeautifulSoup(requests.get(pds.current_url).content, 'html.parser')
        personal_info_dict = pds.get_personal_info()

        with open('tests/fbref_scrapers_data/personal_info_dict.pickle', 'rb') as f:
            expected_personal_info_dict = pickle.load(f)[42]

        self.assertEqual(personal_info_dict["name"], expected_personal_info_dict["name"])
        self.assertEqual(personal_info_dict["position"], expected_personal_info_dict["position"])
        self.assertEqual(personal_info_dict["footedness"], expected_personal_info_dict["footedness"])
        self.assertEqual(personal_info_dict["birth_date"], expected_personal_info_dict["birth_date"])
         
      
    def test_get_stats(self):
        urls_dict = {'https://fbref.com/en/players/d70ce98e/Lionel-Messi':1}

        pds = fs.PlayerDataScraper()
        pds.urls_dict = urls_dict
        pds.run()

        with open('tests/fbref_scrapers_data/messi_stats_df.pickle','rb') as f:
            expected_stats_df = pickle.load(f)

        self.assertEqual(list(pds.stats_df.columns), list(expected_stats_df.columns))
        # converted to lists because .columns are np arrays and therefore __eq__ returns
        # an array of booleans instead of a single boolean.

    def test_clean_df(self):
        pass
