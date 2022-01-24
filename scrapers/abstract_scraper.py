from abc import ABC, abstractmethod
import pickle

class AbstractScraper(ABC):
    def __init__(self) -> None:
        print("abstract scraper")
        self.urls = []
        self.html = None
        self.soup = None
        self.result = None
        self.max_workers = 3

    @abstractmethod
    def run(self):        
        pass

    @abstractmethod
    def crawl(self, url):
        pass


    @abstractmethod        
    def extract_data(self):
        pass

    # @abstractmethod    
    # def show_result(self, result):
    #     pass

    @abstractmethod    
    def save_result(self, file_name):## add parser file type (eg. csv, df) and functionality. maybe convert this to actual function?
        pass
        # pickle.dump(self.result,open(file_name,'wb'))

# if __name__ == "__main__":
#     print("abstract scraper imported")

