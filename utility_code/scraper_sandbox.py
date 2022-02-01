from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


test_info_dict = {
    1:{"name": "Lionel Messi"}, 
    2:{"name": "Fabinho"},
    3:{"name": "Thomas Müller"},
    4:{"name": "Error Test"},
    5:{"name": "Josip Stanišić"}
}

news_dict = {}

def get_news_list(soup):
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
    return news_list

for key in test_info_dict:
    name = test_info_dict[key]["name"]
    print(name)
    url = "https://www.espn.co.uk/football/"

    with sync_playwright() as playwright:
        # playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        page.locator("text=Continue without Accepting").click()
        page.locator("id=global-search-trigger").click()
        page.locator("id=global-search-input").fill(name)
        print("name filled")
        # # page.wait_for_timeout(10000)
        page.locator("//html/body/div[5]/div[2]/header/div[2]/ul/li[1]/div/div[1]/input[2]").click()

        page.wait_for_timeout(1000)
        html = page.content()

        browser.close()
    # playwright.stop()
    soup = BeautifulSoup(html, 'html.parser')


    news_dict[key] = get_news_list(soup)

print(news_dict)


