from abc import ABC, abstractmethod
import pickle
import concurrent.futures
import requests
from bs4 import BeautifulSoup


class AbstractScraper(ABC):
    def __init__(self) -> None:
        print("abstract scraper")
        self.urls = []
        self.html = None
        self.soup = None
        self.result = None
        self.max_workers = 3

    def run(self):
    #validate whether there's a URL        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor: 
            executor.map(self.crawl, self.urls)


    def crawl(self, url):
        print("in crawl", url)
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.extract_data()

    @abstractmethod        
    def extract_data(self):
        pass

    # @abstractmethod    
    def save_result(self, file_name):## add parser file type (eg. csv, or pickle)
        pickle.dump(self.result,open(file_name,'wb'))



