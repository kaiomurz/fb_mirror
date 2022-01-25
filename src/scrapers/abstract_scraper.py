from abc import ABC, abstractmethod
import pickle
import concurrent.futures
import requests
from bs4 import BeautifulSoup


class AbstractScraper(ABC):
    def __init__(self) -> None:
        print("abstract scraper")
        self.urls = []
        self.current_url = None
        self.html = None
        self.soup = None
        self.result = None
        self.max_workers = 3

    def run(self):
    #validate whether there's a URL        
        # print("in run")
        # with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor: 
        #     executor.map(self.crawl, self.urls)
        for url in self.urls:
            self.crawl(url)

    def crawl(self, url):
        print("in crawl", url)
        self.current_url = url
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        print("going to extract")
        self.extract_data()

    @abstractmethod        
    def extract_data(self):
        pass

    # @abstractmethod    
    def save_result(self, file_name):## add parser file type (eg. csv, or pickle)
        pickle.dump(self.result,open(file_name,'wb'))



