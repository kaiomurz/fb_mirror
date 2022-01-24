
from scrapers.abstract_scraper import AbstractScraper
import concurrent.futures
import pickle
import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd

class ClubURLsScraper(AbstractScraper):
    def __init__(self) -> None:
        print("Club URL scraper")
        self.urls = []
        self.html = None
        self.soup = None
        self.result = None
        self.max_workers = 3
        self.counter = 0

    def run_crawler(self, url):
        print("in run crawler", url)
        self.get_soup(url)
        self.extract_data()

    def start_crawl_threads(self):        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor: 
            executor.map(self.run_crawler, self.urls)

    def get_soup(self, url):
        print("in get soup", url)        
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        
    def extract_data(self):
        print("extract data")        
        table = self.soup.find('tbody')
        links = table.find_all('a')
        self.result = ["https://fbref.com" + link['href'] for link in links if 'squads' in link['href']]
       
    def save_result(self, file_name):
        pickle.dump(self.result,open(file_name,'wb'))


# if __name__ == "__main__":
#     print("club url scraper imported")
