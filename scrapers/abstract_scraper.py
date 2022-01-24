from abc import ABC, abstractmethod

class AbstractScraper(ABC):
    def __init__(self) -> None:
        print("abstract scraper")
        self.urls = []
        self.html = None
        self.soup = None
        self.result = None
        self.max_workers = 3

    @abstractmethod
    def run_crawler(self):
        pass

    @abstractmethod
    def start_crawl_threads(self, urls):        
        pass

    @abstractmethod    
    def get_soup(self, url):
        pass

    @abstractmethod        
    def extract_data(self, soup):
        pass

    @abstractmethod    
    def show_result(self, result):
        pass

    @abstractmethod    
    def save_result(self,result):
        pass

if __name__ == "__main__":
    print("abstract scraper imported")

