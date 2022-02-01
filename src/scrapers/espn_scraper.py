import concurrent.futures

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

from scrapers import abstract_scraper as a

class ESPNScraper(a.AbstractScraper):
    def __init__(self) -> None:
        self.names_dict = NotImplemented
        self.news_dict = {}
        self.max_workers = 3
        self.url = "https://www.espn.co.uk/football/"
    
    def run(self):
        keys = self.names_dict.keys()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self.crawl, keys)
    
    def crawl(self, key: int) -> None:
        self.current_key = key
        name = self.names_dict[self.current_key]
        self.get_soup(name)
        self.extract_data()

    def get_soup(self,name):
                
        with sync_playwright() as playwright:
            # playwright = sync_playwright().start()
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.url)

            page.locator("text=Continue without Accepting").click()
            page.locator("id=global-search-trigger").click()
            page.locator("id=global-search-input").fill(name)
            print("name filled")
            # # page.wait_for_timeout(10000)
            page.locator("//html/body/div[5]/div[2]/header/div[2]/ul/li[1]/div/div[1]/input[2]").click()

            page.wait_for_timeout(1000)
            self.html = page.content()
            self.soup = BeautifulSoup(self.html, 'html.parser')

            browser.close()
    
    def extract_data(self):
        news_divs = self.soup.find_all("li", class_="article__Results__Item")
        news_list = []
        for div in news_divs:
            text = div.text
            ellipsis_loc = text.find("…")
            text = text[:ellipsis_loc]
            news_list.append((text,div.find('a')['href']))
            # print(div.text)
            link = div.find('a')
            # print(link['href'])
        self.news_dict[self.current_key] = news_list

    def save_result(self, file_name):
        pass
    
    def get_names(self):
        pass