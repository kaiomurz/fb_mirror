
from scrapers.abstract_scraper import AbstractScraper
import threading
import concurrent.futures
import re
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

    def run_crawler(self):
        self.get_soup(self.urls)
        self.extract_data(self.soup)

    def start_crawl_threads(self, urls):        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor: 
            executor.map(self.run_crawler, self.urls)

    def get_soup(self, url):
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        
    def extract_data(self, soup):
        table = soup.find('tbody')
        links = table.find_all('a')
        result = ["https://fbref.com" + link['href'] for link in links if 'squads' in link['href']]
    
    def show_result(self, result):
        print(result)

    def save_result(self,result, file_name):
        pickle.dump(result,open(file_name,'wb'))


if __name__ == "__main__":
    print("club url scraper imported")
