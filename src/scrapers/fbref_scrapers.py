from lxml import etree
import pandas as pd


from scrapers import abstract_scraper as a


class ClubURLsScraper(a.AbstractScraper):
    def __init__(self) -> None:
        print("Club URLs scraper")
        self.urls = ['https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats']
        self.max_workers = 1            
        
    def extract_data(self):
        print("extract data")        
        table = self.soup.find('tbody')
        links = table.find_all('a')
        self.result = ["https://fbref.com" + link['href'] for link in links if 'squads' in link['href']]
       
  

class PlayerURLsScraper(a.AbstractScraper):
    def __init__(self) -> None:
        print("Player URLs scraper")        
        self.max_workers = 1
        self.result = {}
        self.counter = 0    
        
    def extract_data(self):
        table = self.soup.find('tbody')
        links = table.find_all('a')
        player_urls = ["https://fbref.com" + link['href']\
        for link in links if\
        'players' in link['href'] and\
        'matchlogs' not in link['href']]

        for url in player_urls:
            self.counter += 1
            self.result[self.counter] = url



# def get_personal_info(soup):
#     print("in get_personal_info")
    
#     personal_info = {}
    
#     name_tag = soup.find("h1",attrs={"itemprop":"name"})
#     personal_info["name"] = name_tag.text.strip("\n")
#     personal_info["full_name"] = name_tag.parent.next_sibling.text
    
    

#     # birth_place = soup.find(attrs={"itemprop":"birthPlace"}).text
#     personal_info["birth_date"] = soup.find(attrs={"itemprop":"birthDate"})["data-birth"]
#     personal_info["height"] = soup.find(attrs={"itemprop":"height"}).text.strip("\n")
#     personal_info["weight"] = soup.find(attrs={"itemprop":"weight"}).text.strip("\n")

#     #get twitter link
#     # links = soup.findAll("a")
#     # for link in links:
#     #     if link.has_attr("href") and \
#     #     "twitter.com" in link["href"] and \
#     #     "FBref" not in link["href"]:            
#     #         twitter_handle = link["href"][20:]
#     # print(twitter_handle)
    

#     return personal_info


# def test():
#     print('parser works')

# if __name__ == "__main__":
#     print("parser imported")