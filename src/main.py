from scrapers.fbref_scrapers import ClubURLsScraper, PlayerURLsScraper, PlayerStatsScraper
from scrapers.wiki_scrapers import WikiContentScraper
import random


#### Scrape FBRef ####
# def scrape_fbref():
# club_urls_scraper = ClubURLsScraper()
# player_urls_scraper = PlayerURLsScraper()

# club_urls_scraper.run()
# player_urls_scraper.urls = club_urls_scraper.result[:2]
# # print(player_urls_scraper.urls)
# player_urls_scraper.run()
# # print(player_urls_scraper.result)

# keys = random.sample(list(player_urls_scraper.result.keys()), 3)

# urls_dict = {key:player_urls_scraper.result[key] for key in keys}
# pss = PlayerStatsScraper()
# pss.urls_dict = urls_dict
# pss.set_urls()
# pss.run()
# pss.create_personal_info_df() ####should this be in extract data?
# pss.get_stats() ####should this be in extract data?


#### Scrape Wikipedia ####

#get names, full names, teams, player_id from postgres table or fbref scraper instance
# use ddg api to get wikipedia links (put in dict link:player_id)
# pass urls_dict to scraper and extract self.urls
# crawl and collect content into dict player_id:content_dict
# reinitialise content_dict for every player.
wcs = WikiContentScraper()
wcs.urls_dict = {'https://en.wikipedia.org/wiki//Fabinho_(footballer%2C_born_1993)':1, "https://en.wikipedia.org/wiki/Lionel_Messi":2}
wcs.set_urls()
wcs.run()
# wcs.extract_data()

#### Main ####

# def main():
#     scrape_fbref()

# if __name__ == "__main__":
#     main()
