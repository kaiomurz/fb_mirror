from ast import Not
import re
import requests
from bs4 import BeautifulSoup
from scrapers import abstract_scraper as a

class WikiContentScraper(a.AbstractScraper):       
    def __init__(self) -> None:
        self.urls_dict = NotImplemented
        self.content_set = set()
        self.consolidated_dict = {}
        self.content_dict = {}
        self.header_stack = []
        self.exclude_set = {"Contents", "See also", "Notes", "References",\
                    "External links", "Navigation menu", 'Further reading',\
                    'Honours', 'Works cited','Career statistics'}
        self.previous_is_p = False
        self.content = re.compile('(h[2-9])|p')
        self.header_order = ['h2','h3','h4','h5']

        self.max_workers = 1

    def set_urls(self):
        self.urls = list(self.urls_dict.keys())

    # def run(self):#move to multithreading
    #     #validate whether there's a URL        
    #     print("in run")
    #     for url in self.urls:
    #         self.crawl(url)

    def crawl(self, url):
        print("in crawl", url)
        self.current_url = url
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        # insert check to see if soup contains the a valid footballer page.
        self.extract_data()

    def extract_data(self):
        self.current_key = self.urls_dict[self.current_url]
        self.get_wiki_content()
        print(self.content_dict['opening'][:50])
        print("current url and index", self.current_url, self.current_key)
        self.consolidated_dict[self.current_key] = self.content_dict
        print(f'{self.current_key} - {self.current_url}: added' )
        print(self.consolidated_dict[self.current_key]['opening'][:50])
        print("\n\n\n")

    def get_wiki_content(self):
        self.content_dict = {}
        self.header_text_dict = {}
        self.previous_is_p = False

        print("url in get_wiki_content", self.current_url)
        self.body = self.soup.find("div", class_="mw-parser-output")
        for c in self.body.children:
            if c.name is not None and \
                c.text not in self.exclude_set and\
                self.content.match(c.name):
                    if c.name[0] == 'h':
                        # if current header smaller than or equal to last header in header_stack
                        # remove lower order headers from header text dict
                        if c.text == 'Career statistics':
                            return
                        self.update_header_text_dict(c.name)
                        self.header_text_dict[c.name] = self.clean_header(c.text)
                        self.previous_is_p = False
                        # print(header_text_dict)
                        # if not, pop header stack till one above current and delete corresponding entries in header_text_dict
                    else:                
                        if len(self.header_text_dict) == 0:
                            # content_set.add(c.text)
                            key = 'opening'

                        else:
                            # print(header_text_dict)
                            key = tuple(self.header_text_dict.values())
                        print("key:",key)
                        self.add_text(key,c.text)

                        self.previous_is_p = True


    def add_text(self, key, text):
        '''concatenate content text to existing content text at current text section of body'''
        if self.previous_is_p:
            # print(f'content dict {self.content_dict}, text {text}, key {key}')
            self.content_dict[key] += "\n" + text
        else:
            self.content_dict[key] = text
    
    @staticmethod
    def clean_header(text):
        if text.endswith("[edit]"):
            return text[:len(text)-6]
        else:
            return text

    def update_header_text_dict(self, current_header):
            header_index = self.header_order.index(current_header)
            for header in self.header_order[header_index:]:
                # print(header)
                try:
                    del self.header_text_dict[header]
                except:
                    continue

    def save_result(self, file_name):
        pass



def get_wikipedia_links(personal_info_dict:dict) -> dict:        
    """
    This function takes a dictionary in the format of a .personal_info_dict
    attribute of PlayerDataScraperClass and returns a dictionary with 
    assumed wikipedia links as keys and ids as values.

    Parameters
    ----------
    personal_info_dict: dict
        dictionary in the format of a .personal_info_dict attribute
        of PlayerDataScraperClass. A .personal_info_dict is a dictionary
        with ids as keys and dictionaries as values. The value 
        dictionaries should contain a key "name".    

    """       
    
    # fix to return only valid wiki links and log errors in some other
    # data structure

    names_dict = {id:personal_info_dict[id]['name'] for id in personal_info_dict.keys()}
    wiki_urls_dict = {}
    errors_dict = {}

    for id in names_dict:
        name = names_dict[id]

        url = f'https://api.duckduckgo.com/?q={name}&format=json&pretty=1'
        response = requests.get(url)
        response_json = response.json()
        response_html = response.text
        # player_id = 10

        if "footballer" not in response_html:
            errors_dict[names_dict[id]] = "no \"footballer\" in response"
            continue

        print("url:", url)
        print("xxx:",response_json["RelatedTopics"][0]["FirstURL"])

        if "footballer" in response_json["RelatedTopics"][0]["FirstURL"]\
        and "footballers" not in response_json["RelatedTopics"][0]["FirstURL"]:
            print("triggered")
            wiki_link  = response_json["RelatedTopics"][0]["FirstURL"]\
                .replace("duckduckgo.com", "en.wikipedia.org/wiki")\
                .replace("%2C", ",")
                  
        # elif "footballer" in response_html:
        else:
            abstract_url = response_json["AbstractURL"]
            if "wikipedia" in abstract_url:
                wiki_link =  abstract_url
            else:
                errors_dict[names_dict[id]] = "No wiki link"
            
        # else:
        #     errors_dict[names_dict[id]] = "no \"footballer\" in response"
        #     # errors_dict[names_dict[id]] = "Unknown error"

        wiki_urls_dict[wiki_link] = id

    return wiki_urls_dict, errors_dict

    

