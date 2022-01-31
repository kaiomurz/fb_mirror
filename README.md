# fb_aggregator

## Project Summary
The objective of the project is to 
- scrape data on footballers from various sources
- aggregate data on so that it can be attributed to individual footballers, and
- store the data in appropriate data sinks. 

The idea is not necessarily to scrape large volumes of data but to demonstrate ways to:  
- scrape data on a single entity from disparate data sources and combine them under the reference of that single entity,  
- scrape different types of data eg. tabular, text, images, etc.  
- store data in more than one database type,  
- scrape different kinds of sites, including ones needing browser interaction and JS execution.  
- deploy the scraper in a Docker container on EC2 and have it run regularly.

#### Intended functionality:  
- Crawl [FBRef](https://fbref.com/) to get a list of players in the top European football leagues and stats on the players. _(crawling, structured data)_
- Based of names of players in the first database, automatically crawl Wikipedia pages of players and scrape images, and the article. Retrieve the article with its headings structure intact so it can be stored as a json object (scraping unstructured data and storing in NoSQL DB, and scraping images)  
- Access the most recent news headlines on player as they appear in the autocomplete in the search box of [ESPN](https://www.espn.co.uk/football/). _(interacting with browser elements and executing JS)_.  
- Access Twitter's API to retrieve the most recent tweets by players. _(using APIs)_  
  
Time permitting, I could build a rudimentary website based on either Flask or FastAPI where one can type in the name of a player and get collated info from all the various sources.

## Project structure

![fb_aggregator tree](tree.jpg)
## Work remaining
use Playwright to scrape ESPN
json of wiki content
store resulting data in Postgres or MongoDB as appropriate.
write tests