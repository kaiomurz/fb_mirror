
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
        self.max_workers = 1
        self.counter = 0

    def run(self):
        #validate whether there's a URL        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor: 
            executor.map(self.crawl, self.urls)

    def crawl(self, url):
        print("in crawl", url)
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.extract_data()
        
    def extract_data(self):
        print("extract data")        
        table = self.soup.find('tbody')
        links = table.find_all('a')
        self.result = ["https://fbref.com" + link['href'] for link in links if 'squads' in link['href']]
       
    # def save_result(self, file_name):
    #     pickle.dump(self.result,open(file_name,'wb'))

