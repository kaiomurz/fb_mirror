from scrapers import abstract_scraper as a

class ClubURLsScraper(a.AbstractScraper):
    def __init__(self) -> None:
        self.url = "https://en.wikipedia.org/wiki/Lionel_Messi"

        