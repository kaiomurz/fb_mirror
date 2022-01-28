from abc import ABC, abstractmethod
import pickle
import concurrent.futures
import requests
from bs4 import BeautifulSoup


class AbstractScraper(ABC):
    """
    Abstract base class for a scraper. 

    Attributes
    ----------
    urls : list
        list of urls to iterate from which to extract data.
    current_url : string
        url currently being scraped
    html: str
        html text of response from request to url.
    soup: bs4.BeautifulSoup
        BeautifulSoup object of HTML.
    result: 
        result of data extracted. can be of any type.
    max_workers: int
        number of threads used by thread pool executor.


    Methods
    -------
    run():
        creates ThreadPoolExecutor with list of URLs and calls crawl().
    crawl(url):
        fetches HTML, converts to soup, and calls extract_data().
    extract_data(): abstractmethod
        extracts required data from soup according to specific needs of
        the website.
    save_result(): abstractmethod
        saves result in file type specific to task

    """

    def __init__(self) -> None:
        """
        urls : list
            list of urls to iterate from which to extract data.
        current_url : string
            url currently being scraped
        html: str
            html text of response from request to url.
        soup: bs4.BeautifulSoup
            BeautifulSoup object of HTML.
        result: 
            result of data extracted. can be of any type.
        max_workers: int
            number of threads used by thread pool executor.

        """
        print("abstract scraper")
        self.urls = []
        self.current_url = None
        self.html = None
        self.soup = None
        self.result = None
        self.max_workers = 3

    def run(self) -> None:
        """
        creates ThreadPoolExecutor with list of URLs and calls crawl().
        """
    #validate whether there's a URL        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor: 
            executor.map(self.crawl, self.urls)
        

    def crawl(self, url:str) -> None:
        """
        fetches HTML, converts to soup, and calls extract_data().
        """

        self.current_url = url
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.extract_data()

    @abstractmethod        
    def extract_data(self):
        """
        extracts required data from soup according to specific needs of
        the website. 
    
        """

        pass

    @abstractmethod    
    def save_result(self, file_name):## add parser file type (eg. csv, or pickle)
        """
        saves result in file type specific to task.

        
        """

        pass


