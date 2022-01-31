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
- deploy the scraper in a Docker container on EC2 and have it run at regular intervals.

#### Intended functionality:  
- Crawl [FBRef](https://fbref.com/) to get a list of players in the top European football leagues and stats on the players. _(crawling, structured data)_
- Based of names of players in the first database, automatically crawl Wikipedia pages of players and scrape images, and the article. Retrieve the article with its headings structure intact so it can be stored as a json object (scraping unstructured data and storing in NoSQL DB, and scraping images)  
- Access the most recent news headlines on player as they appear in the autocomplete in the search box of [ESPN](https://www.espn.co.uk/football/). _(interacting with browser elements and executing JS)_.  
- Access Twitter's API to retrieve the most recent tweets by players. _(using APIs)_  
  
Time permitting, I could build a rudimentary website based on either Flask or FastAPI where one can type in the name of a player and get collated info from all the various sources.

## Project structure

![fb_aggregator tree](tree.jpg)

The meat of the project is in the ```/src``` folder. The ```/scrapers``` folder within it contains an abstract base class for a scraper and also classes to create various scrapers for [FBRef](https://fbref.com/) and Wikipedia.  

There are three different scraper classes in ```fbref_scrapers.py```. These include ones for:  
- retrieving the links of teams the Big 5 European leagues,  
- retrieving the links of the player pages of the said teams, and  
- crawling the player pages to retrieve information on individual players.  

The data thus retrieved is stored in two dataframes, one for personal information and one that accumulates all the statistics on the player's page. Both the tables have a ```player_id``` column that could be used to join them for SQL queries. 



main.py``` coordinates the entire 


## How to run the project
Only about half the intended functionality has been implemented but that can be accessed simply by running ```main.py``` in a REPL (assuming the required packages are available). 
At the end of the run, two objects will be available to the user: ```pds``` of class ```PlayerDataScraper``` and ```wcs``` of class ```WikiContentScraper```.  

The results of ```pds``` can be accessed by calling the attributes ```pds.personal_info_df``` and ```pds.stats_df``` which contain the personal information and stats dataframes respectively.  

The results of ```wcs``` are a bit harder to parse at this stage. ```wcs.content_dict``` contains the content extracted for the last player processed. Calling ```wcs.content_dict.keys()``` will give you an idea of the structure extracted from that player's Wikipedia page. Accessing the content of a given key will display the paragraphs under the section the key represents.  

For example if the last processed player was Neymar Jr of of Paris St. Germain, ```content_dict.keys()``` would return  
```dict_keys(['opening', ('Early life',), ('Club career', 'Santos', 'Youth'), ('Club career', 'Santos', '2009: Debut season'), ('Club career', 'Santos', '2010: Campeonato Paulista success'), ('Club career', 'Santos', '2011: Puskás Award'), ('Club career', 'Santos', "2012: South America's best player"), ('Club career', 'Santos', '2013: Final season'), ('Club career', 'Barcelona'), ('Club career', 'Barcelona', 'Transfer investigation'), ('Club career', 'Barcelona', '2013–14: Adapting to Spain'), ('Club career', 'Barcelona', '2014–15: The treble and individual success'), ('Club career', 'Barcelona', '2015–16: Domestic double'), ('Club career', 'Barcelona', '2016–17: Final season'), ('Club career', 'Paris Saint-Germain'), ('Club career', 'Paris Saint-Germain', 'Contract breach lawsuit'), ('Club career', 'Paris Saint-Germain', '2017–18: Debut season and domestic treble'), ('Club career', 'Paris Saint-Germain', '2018–19: Injury and league title'), ('Club career', 'Paris Saint-Germain', '2019–20: Suspended season, European final'), ('Club career', 'Paris Saint-Germain', '2020–21: Contract extension'), ('Club career', 'Paris Saint-Germain', '2021–22: 400th career goal'), ('International career',), ('International career', '2011 South American Youth Championship and Copa América'), ('International career', '2012 Summer Olympics and first hat-trick'), ('International career', '2013 Confederations Cup'), ('International career', '2014 World Cup'), ('International career', '2015 Copa América'), ('International career', '2016 Summer Olympics'), ('International career', '2018 World Cup'), ('International career', 'Lead up to the 2022 World Cup and 2021 Copa América'), ('Player profile', 'Style of play and reception'), ('Player profile', 'Comparisons'), ('Outside football', 'Personal life'), ('Outside football', 'Wealth and sponsorships'), ('Outside football', 'Media'), ('Outside football', 'Music'), ('Outside football', 'Club'), ('Outside football', 'International'), ('Outside football', 'Individual')])```

This 
There are comprehensive docstrings available for both these objects that can be accessed by ```help(pds)``` or ```help(wcs)```.

## Work remaining
use Playwright to scrape ESPN
json of wiki content
store resulting data in Postgres or MongoDB as appropriate.
write tests