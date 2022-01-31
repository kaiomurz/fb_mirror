from scrapers.fbref_scrapers import ClubURLsScraper, PlayerURLsScraper, PlayerDataScraper
from scrapers.wiki_scrapers import WikiContentScraper, get_wikipedia_links
import random


#### Scrape FBRef ####
club_urls_scraper = ClubURLsScraper()
player_urls_scraper = PlayerURLsScraper()

club_urls_scraper.run()
player_urls_scraper.urls = club_urls_scraper.result[:5]### modify to do complete search
# print(player_urls_scraper.urls)
player_urls_scraper.run()
# print(player_urls_scraper.result)

keys = random.sample(list(player_urls_scraper.result.keys()), 5) ### modify to do complete search

urls_dict = {key:player_urls_scraper.result[key] for key in keys}
pds = PlayerDataScraper()
pds.urls_dict = urls_dict
pds.run()
pds.get_stats() ####should this be in extract data?


#### Scrape Wikipedia ####

#get names, full names, teams, player_id from postgres table or fbref scraper instance
# use ddg api to get wikipedia links (put in dict link:player_id)
# pass urls_dict to scraper and extract self.urls
# crawl and collect content into dict player_id:content_dict
# reinitialise content_dict for every player.
test_info_dict = {
    1:{"name": "Lionel Messi"}, 
    2:{"name": "Fabinho"},
    3:{"name": "Thomas Müller"},
    4:{"name": "Error Test"},
    5:{"name": "Josip Stanišić"}
}
wcs = WikiContentScraper()
wcs.urls_dict, errors = get_wikipedia_links(pds.personal_info_dict)
# wcs.urls_dict, errors = get_wikipedia_links(test_info_dict)
print("errors from get_wikipedia_links", errors)
wcs.set_urls()
wcs.run()
print("bad links", wcs.bad_links)
# wcs.extract_data()

#### Main ####

# def main():
#     scrape_fbref()

# if __name__ == "__main__":
#     main()
