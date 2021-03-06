# fb_aggregator

![project_chart](project_chart.jpg)

## Objective
The objective of the project is to implement an end-to-end complex and multi-source data collection, transformation, and storage pipeline that can be containerised to periodically run from a cloud server. Key aspects involve:
- scraping data on a single entity from disparate data sources and combining them under the reference of that single entity,  
- automating entity resolution, 
- extracting the structure of text from a Wikipedia page and storing the text in a manner that can make it retrievable using section headings, 
- scraping various types of data - tabular, text, images, and storing it in relevant database types on cloud servers,  
- scraping different kinds of sites, including ones needing browser interaction and JavaScript execution,   
- deploying the scraper in a Docker container on EC2 and have it run at regular intervals, 
- monitoring the operation using tools such as Prometheus and Grafana, and 
- implementing the entire project using robust software engineering principles that include testing and CICD.

#### Intended functionality:  
The aim is to 
- scrape and process data on footballers from various sources, 
- link the data from all the sources to one ```player_id``` per player so that it can be attributed to individual footballers, and    
- store the data in appropriate data sinks on AWS. 
This involves
- Crawling [FBRef](https://fbref.com/) to get a list of players in the top European football leagues and stats on the players. _(structured data)_
- Based of names of players in the first database, infering the correct Wikipedia link for each player using results from DuckDuckGo's API and then scraping the images and the article from the page. Retrieving the article and its headings structure so it can be stored as a json object that can be searched using keys _(using APIs, scraping unstructured data and extracting structure, and scraping images)_  
- Accessing the most recent news headlines on player as they appear in the autocomplete in the search box of [ESPN](https://www.espn.co.uk/football/). _(interacting with browser elements and executing JavaScript)_.  
  

## Project structure

![fb_aggregator tree](tree.jpg)

The meat of the project is in the ```/src``` folder. The ```/scrapers``` folder within it contains an abstract base class for a scraper and also classes to create various scrapers for [FBRef](https://fbref.com/), Wikipedia, and ESPN.  

There are three different scraper classes in ```fbref_scrapers.py```. These include ones for:  
- retrieving the links of teams the Big 5 European leagues,  
- retrieving the links of the player pages of the said teams, and  
- crawling the player pages to retrieve information on individual players.  

The data thus retrieved is stored in two dataframes, one for personal information (one row per player) and one that accumulates all the statistics on the player's page (one row for every season for every player). Both the tables have a ```player_id``` column that could be used to join them for SQL queries. 


## How to run the app

There are two ways to run this app - by cloning this repository or by using a [docker container](https://hub.docker.com/repository/docker/kaiomurz/fb_aggregator). The README on Docker Hub has instructions on how to run the container. Here are the instructions of how to use the code in this repo.  

_Preparing the data sinks_  
The scraper will send the data to a PostgresQL database and S3 bucket. For that, please create an    
- empty PostgresQL database named 'FB_Aggregator' on an AWS RDS instance and  
- an S3 bucket.

Then create a YAML file ```aws_config.yml```  with the following content:  

```# Credentials for S3 (aws\_cli)  
access_key_id: <your AWS access key id>  
secret_access_key: <your AWS secret access key id>  
region_name: <your AWS region name>  

# Credentials for RDS  
DATABASE_TYPE: 'postgresql'  
DBAPI: 'psycopg2'  
ENDPOINT: <your AWS RDS endpoint>  
USER: <username for your database>  
PASSWORD: <password for your database>  
PORT: '5432'  
DATABASE: 'postgres'  
```  


Make sure the required packages are available (easily done by creating a virtual environment using the included ```requirements.txt```).  

Then simply run ```main.py``` from the root folder. The script will instantiate all the necessary scrapers, run them, and sling the data into a PostgreSQL table on an AWS RDS instance or an S3 bucket on AWS as appropriate. 

_Important: to ensure that the script runs quickly enough, by default it will run in demo mode on a small sample of the players. Add the argument ```full``` after ```main.py``` to run the scraper on all the players of the biggest five European football leagues. If you choose the ```full``` option, the process could take several hours to complete._


## Inspecting the objects created
To inspect the sort of data collected, you can run the script in a Python or iPython shell. At the end of the run, three objects will be available to the user:   
- ```pds``` of class ```PlayerDataScraper```,   
- ```wcs``` of class ```WikiContentScraper```, and  
- ```esc``` of class ```ESPNScraper```.  

### _pds_
The results of ```pds``` can be accessed by calling the attributes ```pds.personal_info_df``` and ```pds.stats_df``` which contain the personal information and stats dataframes respectively. 

### _wcs_
The results of ```wcs``` are a bit harder to parse. ```wcs.content_dict``` contains the content extracted for the last player processed. Calling ```wcs.content_dict.keys()``` will give you an idea of the structure extracted from that player's Wikipedia page. Accessing the content of a given key will display the paragraphs under the section the key represents.  

For example if the last processed player was Neymar Jr of of Paris St. Germain, ```content_dict.keys()``` would return  

``` dict_keys(['opening', ('Early life',), ('Club career', 'Santos', 'Youth'), ('Club career', 'Santos', '2009: Debut season'), ('Club career', 'Santos', '2010: Campeonato Paulista success'), ('Club career', 'Santos', '2011: Pusk??s Award'), ('Club career', 'Santos', "2012: South America's best player"), ('International career',), ('International career', '2011 South American Youth Championship and Copa Am??rica'),('Outside football', 'Personal life'), ('Outside football', 'Wealth and sponsorships'), ('Outside football', 'Media'), ('Outside football', 'Music'), ('Outside football', 'Club'), ('Outside football', 'International'), ('Outside football', 'Individual')]) ```  

This represents the structure of the [Wikipedia page](https://en.wikipedia.org/wiki/Neymar) for that particular player. (This output has been truncated for the purposes of presentation.)


Accessing ```wcs.content_dict[('International career', '2011 South American Youth Championship and Copa Am??rica')]``` would return the content:  


```"Neymar was the leading goal scorer of the 2011 South American Youth Championship with nine goals, including two in the final, in Brazil's 6???0 win against Uruguay.[193] He also took part at the 2011 Copa Am??rica in Argentina, where he scored two goals in the first-round game against Ecuador. He was selected 'Man of the Match' in Brazil's first match against Venezuela, which ended a 1???1 draw. Brazil were eliminated in the quarter-finals in a penalty shoot-out against Paraguay (2???2 a.e.t.), with Neymar being substituted in the 80th minute.[194]\n"```

(note: all the keys are tuples except 'opening', which is a string.)  

So, as mentioned, ```wcs.content_dict``` contains the Wikipedia content and structure of the last-processed player. ```new_content_dict``` contains the same information but in a dictionary with a tree structure that reflects the structure of original Wikipedia article. Finally,  ```wcs.consolidated_dict``` simply contains the ```new_content_dicts``` of all players indexed by the same ```player_id``` used in ```pds.personal_info_dict```.  

Additionally, the ```wcs``` object would have also downloaded any images on the Wikipedia site, and uploaded them to an S3 bucket. 

### _esc_
```esc.news_dict``` returns a dictionary with player_id as key and a list containing tuples (news headline, link)

There are comprehensive docstrings available for both these objects that can be accessed by ```help(<object name>)```.

## Packages required

- Requests
- BeautifulSoup4  
- Playwright
- SQLAlchemy
- Psycopg
