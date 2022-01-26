from lxml import etree
import pandas as pd
import requests
from bs4 import BeautifulSoup

from scrapers import abstract_scraper as a
# from utility_code.snippets import clean_df


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
        self.player_id_counter = 0    
    
        
    def extract_data(self):
        table = self.soup.find('tbody')
        links = table.find_all('a')
        player_urls = ["https://fbref.com" + link['href']\
        for link in links if\
        'players' in link['href'] and\
        'matchlogs' not in link['href']]

        for url in player_urls:
            self.player_id_counter += 1
            self.result[url] = self.player_id_counter


class PlayerStatsScraper(a.AbstractScraper):
    def __init__(self) -> None:
        print("Player Stats scraper")        
        self.urls_dict = None
        self.max_workers = 1
        self.current_url = None
        self.personal_info_dict = {}
        self.personal_info_df = None
        self.stats_df = "Empty"
        self.result = {}# dict keys are "personal info" and "stats"
        
        
   
    def set_urls(self):
        self.urls = list(self.urls_dict.keys())

    def crawl(self, url):
        # print("in crawl", url)
        self.current_url = url
        # print("current url", self.current_url)
        self.html = requests.get(self.current_url).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        # print("going to extract")
        self.extract_data()

    def extract_data(self):
        personal_info = self.get_personal_info()
        # print("in extract s")
        print(personal_info)
        # print("current url in ed", self.current_url)
        
        player_key = self.urls_dict[self.current_url]
        print("keys", player_key)

        #     print("player key", player_key)
        # except:
        #     raise KeyError
        self.personal_info_dict[player_key] = personal_info

        if self.personal_info_dict[self.urls_dict[self.current_url]]["position"] == 'GK':
            return 
        else:
            self.get_stats()
        # print('pi dict', self.personal_info_dict)

    def get_personal_info(self):
        print("in get_personal_info")
        
        personal_info = {}
        
        name_tag = self.soup.find("h1",attrs={"itemprop":"name"})
        personal_info["name"] = name_tag.text.strip("\n").strip("\n")
        personal_info["player_id"] = self.urls_dict[self.current_url]
        # personal_info["full_name"] = name_tag.parent.next_sibling.text
        
        

        # get position,footedness, club
        strongs = self.soup.find_all('strong')
        for strong in strongs:
            if "Position" in strong.text:
                personal_info["position"] = strong.next_sibling.strip("\xa0 ").strip("\xa0▪")
            if "Footed:" in strong.text:
                personal_info["footedness"] = strong.next_sibling.strip(" ")
            if "Club" in strong.text:
                personal_info["club"] = strong.next_sibling.next_sibling.text



        # birth_place = soup.find(attrs={"itemprop":"birthPlace"}).text
        personal_info["birth_date"] = self.soup.find(attrs={"itemprop":"birthDate"})["data-birth"]
        personal_info["height"] = self.soup.find(attrs={"itemprop":"height"}).text.strip("\n")
        personal_info["weight"] = self.soup.find(attrs={"itemprop":"weight"}).text.strip("\n")

        #get twitter link
        links = self.soup.findAll("a")
        for link in links:
            if link.has_attr("href") and \
            "twitter.com" in link["href"] and \
            "FBref" not in link["href"]:            
                personal_info["twitter_handle"] = link["href"][20:]
        # print(twitter_handle)
        # print("in get info:", personal_info)
        return personal_info

    def create_personal_info_df(self):
        self.personal_info_df = pd.DataFrame.from_dict(self.personal_info_dict, orient='index')

        
    def get_stats(self): 
        #check for goalies
        

        player_id = self.urls_dict[self.current_url]

        print("in get_stats")
        tables = pd.read_html(self.html)
        df = tables[2]        
        # clean first table
        df = self.clean_df(df).copy()
        print("first table cleaned")
        #Concatenate rest of the tables
        for i in range(3, len(tables)):
            new_df = self.clean_df(tables[i]).copy()
            df = pd.concat([df,new_df[new_df.columns[6:]]], axis=1)
        print("player's tables concatenated horizontally")
        print(df.head())

        #weed out new players
        if df.shape[1] < 100:
            return
        self.current_df = df.copy()
        # add player_id
        self.current_df["player_id"] = pd.Series([self.urls_dict[self.current_url] for _ in range(self.current_df.shape[0])]).copy()

        # add current player's df to stats_df     
        if str(type(self.stats_df)) != "<class 'pandas.core.frame.DataFrame'>":
            print("first player")
            self.stats_df= self.current_df.copy()
            print(self.stats_df.head())
        else:
            # print("columns equal:", self.stats_df.columns == df.columns)
            
            print("stats_df", self.stats_df.index)            
            print("current_df", self.current_df.index)            
            # df3 = df3[~df3.index.duplicated(keep='first')]
            self.stats_df = pd.concat([self.stats_df, self.current_df]).copy()
            print("stats df shape", self.stats_df.shape)

    @staticmethod    
    def clean_df(df):
        df = df.drop('Matches', axis=1, level=1) 

        #drop top level from general data column names
        new_columns = list(df.columns[:6].droplevel()) + list(df.columns[6:]) 
        df.columns = new_columns

        # truncate df after list of seasons
        loc = 0
        for i, season in enumerate(df['Season']):
            if str(season).endswith('Seasons'):
                loc = i
                break

        return df.head(loc)


        


#pd.DataFrame.from_dict(d, orient='index')


# def test():
#     print('parser works')

# if __name__ == "__main__":
#     print("parser imported")