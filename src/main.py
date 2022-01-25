from scrapers.fbref_scrapers import ClubURLsScraper, PlayerURLsScraper

club_urls_scraper = ClubURLsScraper()
player_urls_scraper = PlayerURLsScraper()

club_urls_scraper.run()
player_urls_scraper.urls = club_urls_scraper.result[:2]
print(player_urls_scraper.urls)
player_urls_scraper.run()
print(player_urls_scraper.result)
