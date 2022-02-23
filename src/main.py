from sys import exit
from os.path import exists
import yaml

from scrapers.fbref_scrapers import ClubURLsScraper, PlayerURLsScraper, PlayerDataScraper
from scrapers.wiki_scrapers import WikiContentScraper, get_wikipedia_links
from scrapers.espn_scraper import ESPNScraper
import random

if not exists('./aws_config.yml'):
    print("please copy aws_config.yml in required format into image before running it")
    exit()

with open('aws_config.yml', 'r') as f:
    aws_credentials = yaml.load(f)

# for key in aws_credentials:
#     print(f'{key}: {aws_credentials[key]}')
# exit()


number_of_clubs = 5
number_of_players = 10

#### Scrape FBRef ####
club_urls_scraper = ClubURLsScraper()
print("club url scraper created")
player_urls_scraper = PlayerURLsScraper()
print("player url scraper created")

club_urls_scraper.run()
print("club url scraper created")



player_urls_scraper.urls = club_urls_scraper.result[:number_of_clubs]### modify to do complete search
# print(player_urls_scraper.urls)
player_urls_scraper.run()
print("player url scraper created")

# print(player_urls_scraper.result)

keys = random.sample(list(player_urls_scraper.result.keys()), number_of_players) ### modify to do complete search

# print(keys)

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
wcs.run()
print("bad links", wcs.bad_links)
wcs.extract_data()



# #### Scrape ESPN ####
esc = ESPNScraper()
# esc.names_dict = test_info_dict
esc.names_dict = pds.personal_info_dict
esc.run()




#### Main ####

# def main():
#     scrape_fbref()

# if __name__ == "__main__":
#     main()
