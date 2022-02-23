import concurrent.futures
import json
import yaml
import os
from numpy import safe_eval

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

import boto3
from botocore.config import Config


try:
    from src.scrapers import abstract_scraper as a  # works for unittest
except:
    from scrapers import abstract_scraper as a # works for run main.py

class ESPNScraper(a.AbstractScraper):
    """
    Scraper designed to use Playwright to visit https://www.espn.co.uk/football/,
    search for player name in search box and download the headlines and links
    of the news articles in the search results.

    Attributes specific to ESPNScraper
    ----------------------------------
    news_dict:
        Dictionary with player_id as key and a list of tuples of the form
        (headline, link) as values.
    news_list:
        List of tuples of the form headline, link) for the player being processed.

    Abstract methods in AbstractScraper written for this class:
    -----------------------------------------------------------     
    
    run():
        creates ThreadPoolExecutor with list of player_ids and calls crawl().
    crawl():
        calls get_soup() and extract_data()
    extract_data():
        Extracts headlines and links from soup.

    Other class methods
    -------------------
    get_soup():
        The core of the scraper - uses Playwright to navigate main page and 
        search site for news on player. 

    """
    def __init__(self) -> None:
        self.names_dict = NotImplemented
        self.news_dict = {}
        self.max_workers = 1
        self.url = "https://www.espn.co.uk/football/"
    
    def run(self):
        """
        creates ThreadPoolExecutor with list of player_ids and calls crawl().
        """
        print("in run")
        keys = self.names_dict.keys()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self.crawl, keys)

        self.save_result()
        # for key in keys:
        #     self.crawl(key)

    def crawl(self, key: int) -> None:
        """
        Extracts player name from names_dict and calls
        - get_soup() to retrieve soup of html on search results page of player
        - extract_data() to extract headlines and links from soup
        
        Parameters
        ----------
        url: str
            url to be processed
        """

        print("in crawl", self.names_dict[key])

        self.current_key = key
        self.name = self.names_dict[self.current_key]["name"]
        self.get_soup()
        self.extract_data()

    def get_soup(self):
        """
        - visits "espn.co.uk/football"
        - deals with GDPR approval
        - fills in search box with name and clicks search button
        - retrieves html on search results page of player and converts to soup 
        """
        
        print("in get soup", self.name)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True) #change to True
            page = browser.new_page()
            page.goto(self.url)

            page.locator("text=Continue without Accepting").click()
            page.locator("id=global-search-trigger").click()
            page.locator("id=global-search-input").fill(self.name)
            # # page.wait_for_timeout(10000)
            page.locator("//html/body/div[5]/div[2]/header/div[2]/ul/li[1]/div/div[1]/input[2]").click()

            page.wait_for_timeout(5000) #wait for news to load
            self.html = page.content()
            self.soup = BeautifulSoup(self.html, 'html.parser')

            browser.close()
    
    def extract_data(self):
        """
        Extracts headlines and links from soup.
        """
        

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

    def save_result(self):
        print('uploading ESPN results to S3 bucket')    
        # Save json to local storage
        #delete old json?
        with open('espn_result.json','w') as f:
            json.dump(self.news_dict, f)

        with open('aws_config.yml', 'r') as f:
            aws_credentials = yaml.load(f, Loader=yaml.FullLoader)

        my_config = Config(            
            region_name = aws_credentials['region_name']
        )

        s3_client = boto3.client(
            's3',
            config = my_config,
            aws_access_key_id = aws_credentials['access_key_id'],
            aws_secret_access_key = aws_credentials['secret_access_key'],            
        )

        response = s3_client.upload_file('espn_result.json', 'fbaggregatorimages', 'espn_result.json')
        print('espn_json uploaded')
        #delete local json
        os.remove('espn_result.json')


    def get_names(self):
        pass