import concurrent.futures

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

from scrapers import abstract_scraper as a

class ESPNScraper(a.AbstractScraper):
    def __init__(self) -> None:
        self.names_dict = NotImplemented
        self.news_dict = {}
        self.max_workers = 1
        self.url = "https://www.espn.co.uk/football/"
    
    def run(self):
        print("in run")
        keys = self.names_dict.keys()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self.crawl, keys)

        # for key in keys:
        #     self.crawl(key)

    def crawl(self, key: int) -> None:
        print("in crawl", self.names_dict[key])

        self.current_key = key
        self.name = self.names_dict[self.current_key]["name"]
        print("name assigned", self.name)
        self.get_soup()
        self.extract_data()

    def get_soup(self):
        print("in get soup", self.name)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False) #change to True
            page = browser.new_page()
            page.goto(self.url)

            page.locator("text=Continue without Accepting").click()
            page.locator("id=global-search-trigger").click()
            page.locator("id=global-search-input").fill(self.name)
            print("name filled")
            # # page.wait_for_timeout(10000)
            page.locator("//html/body/div[5]/div[2]/header/div[2]/ul/li[1]/div/div[1]/input[2]").click()

            page.wait_for_timeout(5000)
            self.html = page.content()
            self.soup = BeautifulSoup(self.html, 'html.parser')

            browser.close()
    
    def extract_data(self):
        print("in extract data", self.name)

        news_divs = self.soup.find_all("li", class_="article__Results__Item")
        self.news_list = []
        for div in news_divs:
            text = div.text
            ellipsis_loc = text.find("…")
            text = text[:ellipsis_loc]
            self.news_list.append((text,div.find('a')['href']))
            # print(div.text)
            link = div.find('a')
            # print(link['href'])
        print(self.news_dict)
        self.news_dict[self.current_key] = self.news_list

    def save_result(self, file_name):
        pass

    def get_names(self):
        pass