from scrapers.fbref_scrapers import ClubURLsScraper, PlayerURLsScraper, PlayerStatsScraper
import random

club_urls_scraper = ClubURLsScraper()
player_urls_scraper = PlayerURLsScraper()

club_urls_scraper.run()
player_urls_scraper.urls = club_urls_scraper.result[:2]
# print(player_urls_scraper.urls)
player_urls_scraper.run()
# print(player_urls_scraper.result)

keys = random.sample(list(player_urls_scraper.result.keys()), 3)

urls_dict = {key:player_urls_scraper.result[key] for key in keys}
pss = PlayerStatsScraper()
pss.urls_dict = urls_dict
pss.set_urls()
pss.run()
pss.create_personal_info_df()
pss.get_stats()