from typing import Tuple
import os
import re
import requests
from bs4 import BeautifulSoup
from scrapers import abstract_scraper as a

class WikiContentScraper(a.AbstractScraper):
    """
    Scraper designed to extract content from wikipedia page of 
    individual footballer.

    Attributes specific to WikiContentScraper
    ----------------------------------------
    urls_dict: dict
        dictionary with urls as keys and ids as values.
    current_url: str
        url whose soup is being currently processed
    content_set: set
        yet to be implemented.
    consolidated_dict: dict
        consolidated dictionary of content with ids as keys and 
        content_dict as values
    content_dict: dict
        wikipedia content for a single player with keys as heading
        tuples and values as content text. The reason it's an instance 
        attribute instead of a disposable return value from 
        get_wiki_content is that it can be inspected in the repl while
        debugging in case of the code failing while processing current 
        player's content
    header_stack: list
        list of headers hierarchical order that apply to current text
        being considered
    exclude_set: set
        set of headers to be ignored for inclusion into content_dict
    previous_is_p: boolean
        toggle to remember whether previously considered element was 
        paragraph text or a header
    content: re.Pattern
        regex pattern to identify content that ought to be considered 
        for inclusion
    header_order: list
        header names in hierarchical order. used for deciding whether 
        to continue adding headers to current stack or to start a new 
        stack
    current_key: int
        key of current player whose content is being processed
    body: bs4 Element
        body content extracted from wikipedia page, from which the 
        content_dict will be created.
    bad_links: dict
        dictionary of failed links with ids as keys and links as values


    Abstract methods in AbstractScraper written for this class:
    -----------------------------------------------------------     
    extract_data():
        Call get_wiki_content and assign resulting 
        content_dict to consolidated_dict.
        
    save_result(): abstractmethod
        yet to be written

    AbstractScraper methods rewritten for this class
    ------------------------------------------------
    crawl():
        The same as the one in the abstract class but with the addition 
        of
        - Setting the current_key (player_id). 
        - checking the soup for a valid footballer page before 
          extract_data() is called.


    Other methods specific to WikiContentScraper
    -------------
    set_urls():
        create url_list for crawling from urls_dict
    get_wiki_content():
        cycle through body of wikipedia page and organise content in a dictionary
        where the keys are tuples of heading hierarchies and values are the
        contents of the paragraphs.
    add_text(text)
        concatenate content text to existing content text at current text section of body
    clean_header(text): static method
        extracts relevant header text from all the header text
    update_header_text_dict(current_header)
        modify current header tuple to incorporate current header and eliminate lower
        order headers.

    """       
    def __init__(self) -> None:
        self.urls_dict = NotImplemented #to be passed after instantiation
        self.content_set = set()
        self.consolidated_dict = {}
        self.content_dict = {}
        self.header_stack = []
        self.exclude_set = {"Contents", "See also", "Notes", "References",\
                    "External links", "Navigation menu", 'Further reading',\
                    'Honours', 'Works cited','Career statistics', 'External links'}
        self.content = re.compile('(h[2-9])|p')
        self.header_order = ['h2','h3','h4','h5']
        self.bad_links = {}
        self.max_workers = 1

    def set_urls(self):
        self.urls = list(self.urls_dict.keys())

    def crawl(self, url: str):
        """
        Retrieves html from url passed from run(). 
        - Sets the current_key (player_id). 
        - Retrieves HTML and makes soup
        - Checks the soup for a valid footballer page before 
          extract_data() is called.
        
        Parameters
        ----------
        url: str
            url to be processed
        """

        self.current_url = url
        self.current_key = self.urls_dict[self.current_url]
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        if "Club career" in self.html:
            self.extract_data()
        else:
            self.bad_links[self.current_key] = self.current_url
        self.scrape_images()
        

    def extract_data(self):
        """
        Call get_wiki_content and assign resulting  content_dict to consolidated_dict.
        """
        
        self.get_wiki_content()
        self.consolidated_dict[self.current_key] = self.content_dict

    def get_wiki_content(self):
        """
        cycle through body of wikipedia page and organise content in a dictionary
        where the keys are tuples of heading hierarchies and values are the
        contents of the paragraphs.
        The information in the keys could then be used to create a json object.
        """

        self.content_dict = {}
        self.header_text_dict = {}
        self.previous_is_p = False

        self.body = self.soup.find("div", class_="mw-parser-output")
        for c in self.body.children:
            if c.name is not None and \
                c.text not in self.exclude_set and\
                self.content.match(c.name):# i.e. either it's a heading or a paragraph
                    if c.name[0] == 'h':
                        # if current header smaller than or equal to last header in header_stack
                        # remove lower order headers from header text dict
                        if c.text == 'Career statistics':
                            # 'Career statistics' marks the end of the relevant content
                            return
                        self.update_header_text_dict(c.name) 
                        self.header_text_dict[c.name] = self.clean_header(c.text)
                        self.previous_is_p = False
                    else: 
                        if len(self.header_text_dict) == 0:
                            key = 'opening'
                        else:
                            key = tuple(self.header_text_dict.values())
                        # print("key:",key)
                        self.add_text(key,c.text)

                        self.previous_is_p = True

    def add_text(self, key:Tuple[str], text:str):
        """
        concatenate content text to existing content text at current text section of body
        
        Parameters
        ----------
        key: int
            current key of hierarchical headers
        text: str
            Header text to be processed
        """

        if self.previous_is_p:
            # print(f'content dict {self.content_dict}, text {text}, key {key}')
            self.content_dict[key] += "\n" + text
        else:
            self.content_dict[key] = text
    
    @staticmethod
    def clean_header(text:str) -> str:
        """
        extracts relevant header text from all the header text

        text: str
            header text to be processed
        """
        
        if text.endswith("[edit]"):
            return text[:len(text)-6]
        else:
            return text

    def update_header_text_dict(self, current_header:str):
        """        
        Look at where in the hierarchy of the current header tuple the 
        current_header is and 
        - replace header in header tuple at the same level as current_header 
          with current header and
        - eliminate headers in header tuple that are lower order than 
          current_header.
        """
        
        header_index = self.header_order.index(current_header)
        for header in self.header_order[header_index:]:
            # print(header)
            try:
                del self.header_text_dict[header]
            except:
                continue

    def scrape_images(self):
        print("in scrape images")
        img_list = self.soup.find_all("img")

        im_count = 1
        print(len(img_list), "images found")
        if len(img_list) > 0:
            for img in img_list:                
                # if "/thumb/" in img['src'] and "svg" not in img["src"]:
                url = "https:"+img["src"]
                file_name = "test_images/" + str(im_count)
                self.get_and_save_image(url, file_name)
                im_count+=1

    def save_result(self, file_name):
        pass


def get_wikipedia_links(personal_info_dict:dict) -> Tuple[dict,dict]:        
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

    names_dict = {id:personal_info_dict[id]['name'] for id in personal_info_dict.keys()}
    wiki_urls_dict = {}
    errors_dict = {}

    for id in names_dict:
        name = names_dict[id]

        url = f'https://api.duckduckgo.com/?q={name}&format=json&pretty=1'
        response = requests.get(url)
        response_json = response.json()
        response_html = response.text

        if "footballer" not in response_html:
            errors_dict[names_dict[id]] = "no \"footballer\" in response"
            continue

        #the 'and' clause is to weed out links that say 
        # "<country>international_footballers" instead of 
        # "<player_name>footballer"
        if "footballer" in response_json["RelatedTopics"][0]["FirstURL"]\
        and "footballers" not in response_json["RelatedTopics"][0]["FirstURL"]:
            wiki_link  = response_json["RelatedTopics"][0]["FirstURL"]\
                .replace("duckduckgo.com", "en.wikipedia.org/wiki")\
                .replace("%2C", ",")
            wiki_urls_dict[wiki_link] = id
                  
        else:
            abstract_url = response_json["AbstractURL"]
            if "wikipedia" in abstract_url:
                wiki_link =  abstract_url
                wiki_urls_dict[wiki_link] = id

            else:
                errors_dict[names_dict[id]] = "No wiki link"          
       

    return wiki_urls_dict, errors_dict

    

