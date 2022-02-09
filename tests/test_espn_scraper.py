import unittest
import pickle
from bs4 import BeautifulSoup
from src.scrapers import espn_scraper as es

class TestESPNScraper(unittest.TestCase):
    def test_extract_data(self):
        esc = es.ESPNScraper()
        with open('tests/espn_scraper_data/messi_espn_html.pickle', 'rb') as f:
            esc.html = pickle.load(f)

        esc.soup = BeautifulSoup(esc.html, 'html.parser')
        esc.current_key = 5

        esc.extract_data()

        with open('tests/espn_scraper_data/messi_espn_news_dict.pickle', 'rb') as f:
            expected_news_dict = pickle.load(f)
            
        self.assertEqual(esc.news_dict, expected_news_dict)


    def test_get_soup(self):
        esc = es.ESPNScraper()
        esc.name = 'Lionel Messi'
        esc.get_soup()

        scraped_name_text = esc.soup.find('a', class_='AnchorLink LogoTile flex items-center pl3 pr3 LogoTile--horizontal flex-row').text 
        
        self.assertIn(esc.name, scraped_name_text)



if __name__ == "__main__":
    unittest.main()