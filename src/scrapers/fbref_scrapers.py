import concurrent.futures

import pandas as pd
import requests
from bs4 import BeautifulSoup

from scrapers import abstract_scraper as a


class ClubURLsScraper(a.AbstractScraper):
    """
    Scraper designed to fetch URLs of the 'Big 5' European teams from 
    FBRef.com.
   
    Abstract methods in AbstractScraper written for this class:
    -----------------------------------------------------------
    extract_data(): 
        parses the soup and extracts required links.
    save_result(): abstractmethod
        yet to be written

    """

    def __init__(self) -> None:
        self.urls = ['https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats']
        self.max_workers = 1            
        
    def extract_data(self) -> None:
        """
        parses the soup and extracts required links.
        """

        table = self.soup.find('tbody')
        links = table.find_all('a')
        self.result = ["https://fbref.com" + link['href'] for link in links if 'squads' in link['href']]

    def save_result(self, file_name) -> None:
        pass
  

class PlayerURLsScraper(a.AbstractScraper):
    """
    Scraper designed to fetch URLs of individual player pages from
    club pages on FBRef.com using links to clubs generated by 
    ClubsURLsScraper.

    player_id_counter is an autoincrementing index. This index is used as a 
    reference to the player in all subsequent actions. 
    
    Abstract methods in AbstractScraper written for this class:
    -----------------------------------------------------------
    extract_data(): 
        parses the soup and extracts links to player pages.
    save_result(): abstractmethod
        yet to be written

    """

    def __init__(self) -> None:
        self.max_workers = 1
        self.result = {}
        self.player_id_counter = 0    
    
        
    def extract_data(self) -> None:
        """
        Parses the soup and extracts links to player pages.
        """
        
        table = self.soup.find('tbody')
        links = table.find_all('a')
        player_urls = ["https://fbref.com" + link['href']\
        for link in links if\
        'players' in link['href'] and\
        'matchlogs' not in link['href']]

        for url in player_urls:
            self.player_id_counter += 1
            self.result[url] = self.player_id_counter

    def save_result(self, file_name) -> None:
        pass


class PlayerDataScraper(a.AbstractScraper):# docstring not complete. class not yet reviewed.
    """
    Scraper designed to extract from player's pages
    - personal info and store in dataframe (one row per player)
    - stats tables and store in dataframe (one row per (player,season))

    Attributes specific to PlayerDataScraper
    ----------------------------------------
    urls_dict: dict
        dictionary with urls as keys and ids as values.
    current_url: str
        url whose soup is being currently processed
    personal_info_dict: dict
        dictionary with player_ids as keys and dicts as values. These dicts
        have "name", "position" etc, as keys and their respective attributes 
        as values.
    personal_info_df: pd.DataFrame
        DataFrame derived from personal_info_dict indexed with player_id. 
    stats_df: pd.DataFrame
        consolidated data frame of all the seasons tables of all the players.
        includes a column for player_id to be used as foreign key when storing
        in a SQL database.
    result: dict
        contains results of scrapers. keys include personal_info and stats and 
        values are the respective dataframes. 
    
    Abstract methods in AbstractScraper written for this class:
    -----------------------------------------------------------
    extract_data(): 
        - call get_personal_info() and store dict returned in 
          self.personal_info_dict()
        - call get_stats()
        
    save_result(): abstractmethod
        yet to be written

    Other methods specific to PlayerDataScraper
    -------------
    get_personal_info(self)
        extract 
            - name
            - birth date
            - height
            - weight            
            - position
            - footedness
            - club
            - twitter handle
        from player page and return as dict

    get_stats(self)
        extract seasons tables from player page and concatenate them together
        into a df.
        then concatenate the player df with the overall stats df.

    clean_df(df)
        cleans column names of  current table being processed and makes it ready 
        for concatenation.
    """

    def __init__(self) -> None:
        self.urls_dict = None ### {}?
        self.max_workers = 1
        self.current_url = NotImplemented
        self.personal_info_dict = {}
        self.personal_info_df = NotImplemented
        self.stats_df = "Empty" # NotImplemented? also change in if statement
        self.result = {}# dict keys are "personal info" and "stats"        
        self.errors_dict = {}
   
        
   
    def run(self) -> None:
        """
        creates ThreadPoolExecutor with list of URLs and calls crawl().
        additional it also does the pre and post work of creating the urls list
        and the personal_info_df.
        """
        self.urls = list(self.urls_dict.keys())
        #validate whether there's a URL        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor: 
            executor.map(self.crawl, self.urls)
        
        self.personal_info_df = pd.DataFrame.from_dict(self.personal_info_dict, orient='index')
        

    def extract_data(self):
        """
        calls
        - get_personal_info() and stores dict returned in self.personal_info_dict()
        - get_stats()
        """
        
        personal_info = self.get_personal_info()
        player_key = self.urls_dict[self.current_url]        
        self.personal_info_dict[player_key] = personal_info

        #modify to call appropriate function for goalkeeper data extraction 
        if self.personal_info_dict[self.urls_dict[self.current_url]]["position"] == 'GK':
            return 
        else: #get return df and add to stats_df
            self.get_stats()

    def get_personal_info(self): #why are only 2 players being added??
        """
        extracts 
            - name
            - birth date
            - height
            - weight            
            - position
            - footedness
            - club
            - twitter handle
        from player page and return as dict
        """
        
        personal_info = {}
        
        name_tag = self.soup.find("h1",attrs={"itemprop":"name"})
        personal_info["name"] = name_tag.text.strip("\n").strip("\n")
        personal_info["player_id"] = self.urls_dict[self.current_url]
        
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
        return personal_info


        
    def get_stats(self):
        """
        extract seasons tables from player page and concatenate them together
        into a df.
        then concatenate the player df with the overall stats df.

        """        

        tables = pd.read_html(self.html)

        #reduce tables to only contain stats tables 
        table_indices = []
        for i, table in enumerate(tables):
            if ( 'Unnamed: 0_level_0',  'Season') in table.columns:
                table_indices.append(i)
        tables = [tables[i] for i in  range(len(tables)) if i in table_indices]

        # clean first table
        df = tables[0]    
        df = self.clean_df(df).copy()
        #Concatenate rest of the tables
        for i in range(1, len(tables)):
            new_df = self.clean_df(tables[i]).copy()
            df = pd.concat([df,new_df[new_df.columns[6:]]], axis=1)

        #weed out squad players who haven't played
        if df.shape[1] < 100:
            return
        self.current_df = df.copy()
        # add player_id column
        self.current_df["player_id"] = pd.Series([self.urls_dict[self.current_url] for _ in range(self.current_df.shape[0])]).copy()


        # add current player's df to stats_df     
        if str(type(self.stats_df)) != "<class 'pandas.core.frame.DataFrame'>": #i.e. if it's the first player
            self.stats_df= self.current_df.copy()
        else:
            try:
                self.stats_df = pd.concat([self.stats_df.copy(), self.current_df], ignore_index=True, sort=False).copy()
            except:
                self.errors_dict[self.current_url] = self.clean_df

    @staticmethod    
    def clean_df(df):
        """
        cleans column names of current table being processed and makes it ready 
        for concatenation.

        """
        
        df = df.drop('Matches', axis=1, level=1) 

        # drop top level from general data column names
        new_columns = list(df.columns[:6].droplevel()) + list(df.columns[6:]) 
        df.columns = new_columns

        # truncate df after list of seasons
        print(df[df.columns[:5]].head())
        loc = 0
        for i, season in enumerate(df['Season']):
            if str(season).endswith('Seasons'):
                loc = i
                break

        return df.head(loc)

    def save_result(self, file_name):
        pass
        


#pd.DataFrame.from_dict(d, orient='index')


# def test():
#     print('parser works')

# if __name__ == "__main__":
#     print("parser imported")