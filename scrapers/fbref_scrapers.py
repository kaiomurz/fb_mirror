from lxml import etree
import pandas as pd


from scrapers import abstract_scraper as a


class ClubURLsScraper(a.AbstractScraper):
    def __init__(self) -> None:
        print("Club URLs scraper")
        self.urls = ['https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats']
        self.max_workers = 1            
        
    def extract_data(self):
        print("extract data")        
        table = self.soup.find('tbody')
        links = table.find_all('a')
        self.result = ["https://fbref.com" + link['href'] for link in links if 'squads' in link['href']]
       
  

class PlayerURLsScraper(a.AbstractScraper):
    def __init__(self) -> None:
        print("Player URLs scraper")        
        self.max_workers = 1
        self.result = {}
        self.counter = 0    
        
    def extract_data(self):
        print("in extract")
        table = self.soup.find('tbody')
        links = table.find_all('a')
        player_urls = ["https://fbref.com" + link['href']\
        for link in links if\
        'players' in link['href'] and\
        'matchlogs' not in link['href']]
        # self.result += player_urls
        # print("after extraction", player_urls)
        for url in player_urls:### slicing for testing only. drop eventually.
            print("in loop", url)
            self.counter += 1
            self.result[self.counter] = url
            # self.result[self.counter] = url

