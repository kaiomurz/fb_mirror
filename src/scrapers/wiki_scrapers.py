import re

from scrapers import abstract_scraper as a

class WikiContentScraper(a.AbstractScraper):       
    def __init__(self) -> None:
        self.urls_dict = None
        self.content_set = set()
        self.consolidated_dict = {}
        self.content_dict = {}
        self.header_text_dict = {}
        self.header_stack = []
        self.exclude_set = {"Contents", "See also", "Notes", "References", "External links", "Navigation menu"}
        self.previous_is_p = False
        self.content = re.compile('(h[2-9])|p')
        self.header_order = ['h2','h3','h4','h5']

        self.max_workers = 1

    def set_urls(self):
        self.urls = list(self.urls_dict.keys())

    def extract_data(self):
        self.get_wiki_content()
        self.consolidated_dict[self.urls_dict[self.current_url]] = self.content_dict
        print(f'{self.urls_dict[self.current_url]} - {self.current_url}: added' )

    def get_wiki_content(self):
        self.body = self.soup.find("div", class_="mw-parser-output")

        for c in self.body.children:
            if c.name is not None and \
                c.text not in self.exclude_set and\
                self.content.match(c.name):
                    if c.name[0] == 'h':
                        # if current header smaller than or equal to last header in header_stack
                        # remove lower order headers from header text dict
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
                        self.add_text(key,c.text)

                        self.previous_is_p = True


    def add_text(self, key, text):
        '''concatenate content text to existing content text at current text section of body'''
        if self.previous_is_p:
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

def get_names_dict(personal_info_dict):
    return {id:personal_info_dict[id]['name'] for id in personal_info_dict.keys()}

def get_wikipedia_links(names_dict):
    wiki_urls_dict = {}

    for id in names_dict:
        name = names_dict[id]

        url = f'https://api.duckduckgo.com/?q={name}&format=json&pretty=1'
        response = requests.get(url)
        response_json = response.json()
        response_html = response.text
        # player_id = 10

        if "footballer" not in response.text:
            wiki_link =  "No footballer reference"
        elif "footballer" in response_json["RelatedTopics"][0]["FirstURL"]:
            wiki_link  = response_json["RelatedTopics"][0]["FirstURL"].replace("duckduckgo.com", "en.wikipedia.org/wiki/")

        elif "footballer" in response_html:
            abstract_url = response_json["AbstractURL"]
            if "wikipedia" in abstract_url:
                wiki_link =  abstract_url
            else:
                wiki_link =  "No wiki link"
        else:
            wiki_link =  "Unknown error"

        wiki_urls_dict[id] = wiki_link
    return wiki_urls_dict

