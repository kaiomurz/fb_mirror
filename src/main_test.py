from re import U
from scrapers.wiki_scrapers import WikiContentScraper, get_wikipedia_links
import random

test_info_dict = {
        1:{"name": "Josip Stanišić"},
        2:{"name": "Fabinho"},
        3:{"name": "Thomas Müller"},
        4:{"name": "Neymar Jr."},
        5:{"name": "Lionel Messi"}, 
        6:{"name": "Jordan Henderson"},
        7:{"name": "Andriy Lunin"},      
        8:{"name": "Deliberate error"}
}
wcs = WikiContentScraper()

# wcs.urls_dict, errors = get_wikipedia_links(pds.personal_info_dict)
# wcs.urls_dict, errors = get_wikipedia_links(test_info_dict)
urls_dict, errors_dict = (get_wikipedia_links(test_info_dict))
print(urls_dict)
print("\n")
print(errors_dict)

# print("errors from get_wikipedia_links", errors)
# wcs.run()
# name = test_info_dict[key]
# print(name)
# with open('tests/wiki_scraper_data/')
# print("bad links", wcs.bad_links)

#individual and combined

# print(wcs.urls_dict)