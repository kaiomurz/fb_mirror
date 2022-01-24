from lxml import etree
import pandas as pd

from scrapers import abstract_scraper as a


class ClubURLsScraper(a.AbstractScraper):
    def __init__(self) -> None:
        print("Club URLs scraper")
        self.urls = ['https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats']
        self.html = None
        self.soup = None
        self.result = None
        self.max_workers = 1
        self.counter = 0
    
        
    def extract_data(self):
        print("extract data")        
        table = self.soup.find('tbody')
        links = table.find_all('a')
        self.result = ["https://fbref.com" + link['href'] for link in links if 'squads' in link['href']]
       
  

class PlayerURLsScraper(a.AbstractScraper):
    def __init__(self) -> None:
        print("Player URLs scraper")
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

