from scrapers.fbref_scrapers import ClubURLsScraper, PlayerURLsScraper, PlayerDataScraper
# from scrapers.wiki_scrapers import WikiContentScraper, get_wikipedia_links
from scrapers.espn_scraper import ESPNScraper
import random



#### Scrape FBRef ####

# club_urls_scraper = ClubURLsScraper()
# print("club url scraper created")
# player_urls_scraper = PlayerURLsScraper()
# print("player url scraper created")

# club_urls_scraper.run()
# print("club url scraper created")

# player_urls_scraper.urls = club_urls_scraper.result[:5]### modify to do complete search
# # print(player_urls_scraper.urls)
# player_urls_scraper.run()
# print("player url scraper created")

# print(player_urls_scraper.result)

# keys = random.sample(list(player_urls_scraper.result.keys()), 5) ### modify to do complete search

# urls_dict = {key:player_urls_scraper.result[key] for key in keys}
urls_dict = {'https://fbref.com/en/players/d70ce98e/Lionel-Messi':1}

pds = PlayerDataScraper()
pds.urls_dict = urls_dict
pds.run()


#### Scrape Wikipedia ####
# test_info_dict = {
        # 1:{"name": "Josip Stanišić"},
        # 2:{"name": "Fabinho"},
        # 3:{"name": "Thomas Müller"},
        # 4:{"name": "Neymar Jr."},
        # 5:{"name": "Lionel Messi"}, 
        # 6:{"name": "Jordan Henderson"},
        # 7:{"name": "Andriy Lunin"},      
        # 8:{"name": "Deliberate error"}
# }
# wcs = WikiContentScraper()

# wcs.urls_dict, errors = get_wikipedia_links(pds.personal_info_dict)
# wcs.urls_dict, errors = get_wikipedia_links(test_info_dict)
# urls_dict, errors_dict = (get_wikipedia_links(test_info_dict))
# print(urls_dict)
# print("\n")
# print(errors_dict)

# print("errors from get_wikipedia_links", errors)
# wcs.run()
# name = test_info_dict[key]
# print(name)
# with open('tests/wiki_scraper_data/')
# print("bad links", wcs.bad_links)

#individual and combined

# print(wcs.urls_dict)