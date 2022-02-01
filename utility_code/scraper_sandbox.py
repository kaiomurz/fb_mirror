from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)
page = browser.new_page()
page.goto("https://www.espn.co.uk/football/")

page.locator("text=Continue without Accepting").click()
page.locator("id=global-search-trigger").click()
page.locator("id=global-search-input").fill("Lionel Messi")
# # page.wait_for_timeout(10000)
page.locator("//html/body/div[5]/div[2]/header/div[2]/ul/li[1]/div/div[1]/input[2]").click()

page.wait_for_timeout(5000)
html = page.content()
soup = BeautifulSoup(html, 'html.parser')

news_divs = soup.find_all("li", class_="article__Results__Item")
news_list = []
for div in news_divs:
    text = div.text
    ellipsis_loc = text.find("…")
    text = text[:ellipsis_loc]
    news_list.append((text,div.find('a')['href']))
    # print(div.text)
    link = div.find('a')
    # print(link['href'])

print(news_list)

browser.close()
playwright.stop()