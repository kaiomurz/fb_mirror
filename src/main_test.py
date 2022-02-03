from scrapers.wiki_scrapers import WikiContentScraper, get_wikipedia_links
import random

test_info_dict = {
    1:{"name": "Josip Stanišić"},
    2:{"name": "Fabinho"},
    3:{"name": "Thomas Müller"},
    4:{"name": "Neymar Jr."},
    5:{"name": "Lionel Messi"}, 
    6:{"name": "Jordan Henderson"}
}
wcs = WikiContentScraper()
# wcs.urls_dict, errors = get_wikipedia_links(pds.personal_info_dict)
wcs.urls_dict, errors = get_wikipedia_links(test_info_dict)
print("errors from get_wikipedia_links", errors)
wcs.set_urls()
wcs.run()
print("bad links", wcs.bad_links)