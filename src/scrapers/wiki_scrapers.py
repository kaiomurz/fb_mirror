from operator import ne
import shutil
import json
from typing import Tuple
import os
import re
import concurrent.futures

import requests
from bs4 import BeautifulSoup
try:
    from src.scrapers import abstract_scraper as a  # works for unittest
except:
    from scrapers import abstract_scraper as a # works for run main.py



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
    content_dict: dict
        wikipedia content for a single player with keys as heading
        tuples and values as content text. The reason it's an instance 
        attribute instead of a disposable return value from 
        get_wiki_content is that it can be inspected in the repl while
        debugging in case of the code failing while processing current 
        player's content
    consolidated_dict: dict
        consolidated dictionary of content with ids as keys and 
        content_dict as values
    consolidated_json:
        json object representing consolidated_dict
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

    (ADD ATTRIBUTES USED IN JSONIFYING CONTENT DICT)


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
    --------------------------------------------   
    get_wiki_content():
        cycle through body of wikipedia page and organise content in a dictionary
        where the keys are tuples of heading hierarchies and values are the1
        contents of the paragraphs.
    add_text(text)
        concatenate content text to existing content text at current text section of body
    clean_header(text): static method
        extracts relevant header text from all the header text
    update_header_text_dict(current_header):
        modify current header tuple to incorporate current header and eliminate lower
        order headers.
    scrape_images(self):
        Scrape images, if any, from player's Wikipedia site.

    Static Methods
    --------------
    structure_as_dict(content_dict: dict)->dict:    
        uses the tree-like structure of Wikipedia articlerepresented in the 
        tuple keys of content dict to return a correponding nested dictionary    
    merge(a: dict,b: dict)->dict:
        merge dictionaries a and b so that items with identical keys in the two dicts
        are combined under a dict under that key.
    get_and_save_image(img_url: str, file_name: str)->None:
        Downloads image at img_url and saves in file_name
    

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
 

    def run(self) -> None:
        """
        creates ThreadPoolExecutor with list of URLs and calls crawl().
        """
        #validate whether there's a URL
        
        self.urls = list(self.urls_dict.keys())

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor: 
            executor.map(self.crawl, self.urls)
        print("after run:", self.consolidated_dict.keys())
        self.consolidated_json = json.dumps(self.consolidated_dict, indent = 4)

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
            print('to extract data', self.current_url)
            self.extract_data()
        else:
            self.bad_links[self.current_key] = self.current_url
        self.scrape_images()
        

    def extract_data(self):
        """
        Call get_wiki_content and assign resulting  content_dict to consolidated_dict.
        """
        print('in extract before', self.current_key)
        self.get_wiki_content()
        self.new_content_dict = WikiContentScraper.structure_as_dict(self.content_dict.copy())
        # print(self.new_content_dict.keys())
        self.consolidated_dict[self.current_key] = self.new_content_dict
        # print(self.consolidated_dict[self.current_key].keys())
        # self.consolidated_dict[self.current_key] = self.content_dict

        print('in extract after', self.current_key)#, self.consolidated_dict)

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


    @staticmethod
    def structure_as_dict(content_dict: dict)->dict:
        """
        uses the tree-like structure of Wikipedia articlerepresented in the 
        tuple keys of content dict to return a correponding nested dictionary  
        """
        
        cd_keys = list(content_dict.keys())
        # print(cd_keys)
        new_content_list = []
        for key in cd_keys:
            if key == 'opening':
                new_content_list.append({'opening':content_dict['opening']})
                # print(content_dict[key])
                continue
            else:
                key_list = list(key) #key tuple in list form
                temp = key_list.pop()
                temp_content_dict = {temp:content_dict[key]}
                while len(key_list) > 0:
                    temp_content_dict = {key_list.pop():temp_content_dict}
                # print(temp_content_dict, "\n\n")
                new_content_list.append(temp_content_dict)      
        # print('ncl')
        # for item in new_content_list:
            # print(item)    
        #########################################################
        # new_content_list = new_content_list[-5:]#REMOVE!!!
        new_content_dict= new_content_list.pop()
        # print(new_content_dict.keys())
        # print(new_content_dict, "/n/n")
        for item in new_content_list:
            current_key  = list(item.keys())[0]
            d1 = new_content_dict.copy()
            # print('current key', current_key)
            if current_key  in new_content_dict:
                print(True)
                temp = new_content_dict.copy()
                print("before", new_content_dict.keys())
                new_content_dict = WikiContentScraper.merge(d1, item) #[current_key]
                print("after", new_content_dict.keys())
                if len(new_content_dict) < len(temp): # this is a hack to correct an unknown bug where the 
                                                      # all but keys of the top level dictionary disappear
                    new_content_dict = temp

            else:
                print(False)
                new_content_dict.update(item)
            # print("nc keys", new_content_dict.keys())

        return new_content_dict
    
    @staticmethod
    def merge(a: dict, b: dict)-> dict: 
        """
        merge dictionaries a and b so that items with identical keys in the two dicts
        are combined under a dict under that key. This is done recursively to merge nested
        dicts in such a way that even the lower-level values are merged into the right 
        nested structure. 

        Variables:
        a, b: dict
        """
        
        merged = {}
        if len(a) > 0 and len(b) > 0:
            a_keys = list(a.keys())
            b_keys = list(b.keys())
            if a_keys[0] == b_keys[0]:# if b_keys[0] in a_keys - and modify rest of routine accordingly
                merged = {a_keys[0]:WikiContentScraper.merge(a[a_keys[0]],b[b_keys[0]])}
            else:
                merged = a.copy()
                merged.update(b)

        else:
            merged = a.copy()
            merged.update(b)
        
        return merged

    def scrape_images(self):
        """
        Scrape images, if any, from player's Wikipedia site.
        - identify relevant images in soup
        - call get_and_save_image()
        """

        print("in scrape images")
        img_list = self.soup.find_all("img")

        im_count = 1
        print(len(img_list), "images found")
        if len(img_list) > 0:
            for i, img in enumerate(img_list):
                print(i, img['src'])                
                if "/thumb/" in img['src'] and "svg" not in img["src"]:
                    url = "https:"+img["src"]
                    file_name = "test_images/" + str(self.current_key) +  str(im_count) #"test_images/" + "/" +
                    print(file_name)
                    self.get_and_save_image(url, file_name)
                    im_count+=1

    @staticmethod    
    def get_and_save_image(img_url: str, file_name: str)->None:
        """
        Downloads image at img_url and saves in file_name
        """
        
        print("in get and save")
        img = requests.get(img_url, stream=True)
        print("image retrieved", img)
        print("file name outside save", file_name)
        with open(file_name, "wb") as f:
            print("saving file", file_name)
            img.raw.decode_content = True
            shutil.copyfileobj(img.raw, f)

    def save_result(self, file_name = 'wiki_result.json'):
        with open(file_name,'wb') as f:
            f.write(self.consolidated_json)

def get_wikipedia_links(personal_info_dict:dict) -> Tuple[dict, dict]:        
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
        try:
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
        except:
            errors_dict[names_dict[id]] = "unknown error"

    return wiki_urls_dict, errors_dict

    

