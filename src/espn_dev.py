from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from scrapers.espn_scraper import ESPNScraper


test_info_dict = {
    1:{"name": "Lionel Messi"}, 
    2:{"name": "Fabinho"},
    3:{"name": "Thomas Müller"},
    4:{"name": "Error Test"},
    5:{"name": "Josip Stanišić"}
}

esc = ESPNScraper()
esc.names_dict = test_info_dict
esc.run()