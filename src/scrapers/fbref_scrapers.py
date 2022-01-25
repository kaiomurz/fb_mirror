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
            self.result[url] = self.counter


class PlayerStatsScraper(a.AbstractScraper):
    def __init__(self) -> None:
        print("Player Stats scraper")        
        self.urls_dict = None
        self.max_workers = 1

        self.personal_info_dict = {}
        self.personal_info_df = None
        self.stats_df = None
        self.result = {}# dict keys are "personal info" and "stats"
        
   
    def set_urls(self):
        self.urls = list(self.urls_dict.keys())

    def crawl(self, url):
        print("in crawl", url)
        # self.current_url = url
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        print("going to extract")
        self.extract_data(url)

    def extract_data(self,url):
        print("in extract")
        personal_info = self.get_personal_info()
        print(personal_info)
        print("current url", url)
        try:
            player_key = self.urls_dict[url]
            print("player key", player_key)
        except:
            raise KeyError
        self.personal_info_dict[player_key] = personal_info 

    def get_personal_info(self):
        print("in get_personal_info")
        
        personal_info = {}
        
        name_tag = self.soup.find("h1",attrs={"itemprop":"name"})
        personal_info["name"] = name_tag.text.strip("\n")
        personal_info["full_name"] = name_tag.parent.next_sibling.text
        
        

        # birth_place = soup.find(attrs={"itemprop":"birthPlace"}).text
        personal_info["birth_date"] = self.soup.find(attrs={"itemprop":"birthDate"})["data-birth"]
        personal_info["height"] = self.soup.find(attrs={"itemprop":"height"}).text.strip("\n")
        personal_info["weight"] = self.soup.find(attrs={"itemprop":"weight"}).text.strip("\n")

        #get twitter link
        # links = self.soup.findAll("a")
        # for link in links:
        #     if link.has_attr("href") and \
        #     "twitter.com" in link["href"] and \
        #     "FBref" not in link["href"]:            
        #         personal_info["twitter_handle"] = link["href"][20:]
        # print(twitter_handle)
        print("in get info:", personal_info)
        return personal_info

#pd.DataFrame.from_dict(d, orient='index')


# def test():
#     print('parser works')

# if __name__ == "__main__":
#     print("parser imported")