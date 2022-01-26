import re

from scrapers import abstract_scraper as a

class WikiContentScraper(a.AbstractScraper):
    def __init__(self) -> None:
        self.url = "https://en.wikipedia.org/wiki/Lionel_Messi"
        self.previous_is_p = False
        content = re.compile('(h[2-9])|p')
        # heading = re.compile('(h[2-9])')
        self.header_order = ['h2','h3','h4','h5']
        self.content_set = set()
        # header_dict = {}
        self.content_dict = {}
        self.header_text_dict = {}
        self.header_stack = []
        self.exclude_set = {"Contents", "See also", "Notes", "References", "External links", "Navigation menu"}




    def extract_content(self):
        self.body = self.soup.find("div", class_="mw-parser-output")
        h2 = self.soup.find("h2") ### delete if not needed

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

    def update_header_text_dict(self):
            header_index = self.header_order.index(self.current_header)
            for header in self.header_order[header_index:]:
                # print(header)
                try:
                    del self.header_text_dict[header]
                except:
                    continue