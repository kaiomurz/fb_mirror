import unittest
from unittest import result
import pickle
from bs4 import BeautifulSoup
from src.scrapers import wiki_scrapers as ws



class TestWikiScrapers(unittest.TestCase):   

    # def test_get_wiki_content(self):
    #     wcs = ws.WikiContentScraper
    #     with open('tests/wiki_scraper_data/lionel_messi_html.pickle', 'rb') as f:
    #         wcs.html = pickle.load(f)
    #     wcs.soup = BeautifulSoup(wcs.html, 'html.parser')
    #     wcs.get_wiki_content(wcs)
    #     result = wcs.content_dict
    #     with open('tests/wiki_scraper_data/lionel_messi_content_dict.pickle', 'rb') as f:
    #         expected_result = pickle.load(f)
        
    #     self.assertEqual(result, expected_result)

    def test_add_text(self):
        wcs = ws.WikiContentScraper()

        wcs.content_dict = {'opening':"opening paragraph", (1,2,3):"paragraph"}
        wcs.previous_is_p = True
        wcs.add_text((1,2,3),"next paragraph")
        expected_result = {'opening':"opening paragraph", 
                            (1,2,3):"paragraph"+"\n"+"next paragraph"}
        result = wcs.content_dict
        self.assertEqual(result, expected_result)

        wcs.content_dict = {'opening':"opening paragraph", (1,2,3):"paragraph"}
        wcs.previous_is_p = False
        wcs.add_text((1,2,3),"next paragraph")
        expected_result = {'opening':"opening paragraph", 
                            (1,2,3):"next paragraph"}
        result = wcs.content_dict
        self.assertEqual(result, expected_result)
        

    def test_clean_header(self):
        wcs = ws.WikiContentScraper()
        text_1 = "hello, world [edit]"
        text_2 = "hello, world"
        result_1 = wcs.clean_header(text_1).strip(" ")
        result_2 = wcs.clean_header(text_2).strip(" ")
        expected_result = "hello, world"
        self.assertEqual(result_1, expected_result)
        self.assertEqual(result_2, expected_result)


    def test_update_header_text_dict(self):
        #setup and teardown when moving to multiple cases
        wcs = ws.WikiContentScraper()
        current_header = "h3"
        wcs.header_text_dict = {
            'h1': 'header1 text',
            'h2': 'header2 text',
            'h3': 'header3 text',
            'h4': 'header4 text',
            'h5': 'header5 text'
        }
        
        wcs.update_header_text_dict(current_header)
        result = wcs.header_text_dict
        expected_result = {
            'h1': 'header1 text',
            'h2': 'header2 text'
        }      
        self.assertEqual(result, expected_result)

        wcs.header_text_dict = {
            'h1': 'header1 text',
            'h4': 'header4 text',
            'h2': 'header2 text',
            'h5': 'header5 text',
            'h3': 'header3 text'
        }
        
        wcs.update_header_text_dict(current_header)
        result = wcs.header_text_dict
        expected_result = {
            'h1': 'header1 text',
            'h2': 'header2 text'
        }      
        self.assertEqual(result, expected_result)

        #unsorted

    def test_scrape_images(self):
        pass


    def test_merge(self):
        wcs = ws.WikiContentScraper()

        a = {1:{2:3}}
        b = {1:{4:5}}
        result = wcs.merge(a,b)
        expected_result = {1:{2:3, 4:5}}
        self.assertEqual(result, expected_result)

        
        a = {1:{2:3}}
        b = {2:{4:5}}
        result = wcs.merge(a,b)
        expected_result = {1:{2:3}, 2:{4:5}}
        self.assertEqual(result, expected_result)

        a = {1:{2:{3:4}}}
        b = {1:{2:{4:5}}}
        result = wcs.merge(a,b)
        expected_result = {1:{2:{3:4,4:5}}}
        self.assertEqual(result, expected_result)

    def test_structure_as_dict(self):
        wcs = ws.WikiContentScraper()
        d = {(1,2,3):4}
        result = wcs.structure_as_dict(d)
        self.assertEqual(result, {1:{2:{3:4}}})

class Test_get_wikipedia_links(unittest.TestCase):   
    def test_get_wikipedia_links(self):
        test_info_dict = {
            1:{"name": "Josip Stanišić"},
            2:{"name": "Fabinho"},
            3:{"name": "Thomas Müller"},
            4:{"name": "Neymar Jr."},
            5:{"name": "Lionel Messi"}, 
            6:{"name": "Jordan Henderson"},
            7:{"name": "Andriy Lunin"},      
            8:{"name": "Deliberate error"}
        }

        result = ws.get_wikipedia_links(test_info_dict)

        expected_result = (
            {
                'https://en.wikipedia.org/wiki/Josip_Stani%C5%A1i%C4%87': 1,
                'https://en.wikipedia.org/wiki/Fabinho_(footballer,_born_1993)': 2,
                'https://en.wikipedia.org/wiki/Thomas_M%C3%BCller_(disambiguation)': 3,
                'https://en.wikipedia.org/wiki/Neymar': 4,
                'https://en.wikipedia.org/wiki/Lionel_Messi': 5, 
                'https://en.wikipedia.org/wiki/Jordan_Henderson': 6,
                'https://en.wikipedia.org/wiki/Andriy_Lunin': 7
            },
            {'Deliberate error': 'no "footballer" in response'}
        )

        self.assertEqual(result, expected_result)


    
# check types. 
# look at types of assert statements and see if they apply

if __name__ == "__main__":
    unittest.main()