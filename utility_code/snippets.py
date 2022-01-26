#############################################################
######################## FBREF ##############################
#############################################################


################################################################
########### NEW functions to get and parse club urls ###########

def parse_club_urls(soup):
    table = soup.find('tbody')
    links = table.find_all('a')
    club_urls = ["https://fbref.com" + link['href'] for link in links if 'squads' in link['href']]
    return club_urls


def get_club_urls():
    url = 'https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    club_urls = parse_club_urls(soup)
    return club_urls

################################################################
########## NEW functions to get and parse player urls ##########
def parse_player_url(soup):
    global counter
    global player_url_dict 


    table = soup.find('tbody')
    links = table.find_all('a')
    player_urls = ["https://fbref.com" + link['href']\
        for link in links if\
        'players' in link['href'] and\
        'matchlogs' not in link['href']]
    
    for url in player_urls:
        counter += 1
        player_url_dict[counter] = url



def get_player_urls(club_url): #output should be a url
    # time.sleep(2*random.random) #use throttle as class attribute
    soup = BeautifulSoup(requests.get(club_url).text, 'html.parser')
    parse_player_url(soup)

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor: 
    counter = 0
    player_url_dict = {}
    executor.map(get_player_urls, club_urls[:2])###remove slicing









#### extracting player personal data and stats from fbref#### 
url = "https://fbref.com/en/players/21a66f6a/Harry-Kane"
soup = BeautifulSoup(requests.get(url).text)

################################################################
############ bundle into get_personal_data function ############

# def get_personal_info()
name_tag = soup.find("h1",attrs={"itemprop":"name"})
name = name_tag.text.strip("\n")
full_name = name_tag.next_sibling.next_sibling.text


birth_place = soup.find(attrs={"itemprop":"birthPlace"}).text
birth_date = soup.find(attrs={"itemprop":"birthDate"})["data-birth"]
height = soup.find(attrs={"itemprop":"height"}).text.strip("\n")
weight = soup.find(attrs={"itemprop":"weight"}).text.strip("\n")

## finding twitter handle 
links = soup.findAll("a")
for link in links:
    if link.has_attr("href") and \
    "twitter.com" in link["href"] and \
    "FBref" not in link["href"]:            
        print(link["href"])
#############################################################

################## getting headshot ##################

img = requests.get("https://fbref.com/req/202005121/images/headshots/d70ce98e_2018.jpg", stream=True)

################## getting list of tables ##################

url = 'https://fbref.com/en/players/e06683ca/Virgil-van-Dijk'
tables = pd.read_html(url) #in app, pass self.html

################# table locations in tables #################

table_dict = {
    0:'scouting_report',
    1:'similar_players',
    2:'standard_stats',
    3:'shooting_stats',
    4:'passing_stats',
    5:'pass_type_stats',
    6:'gsc_stats',
    7:'defensive_stats',
    8:'possession_stats',
    9:'playing_time_stats',
    10:'misc_stats'    
}

################## Cleaning 'stats' tables ##################

df = tables[2]

def clean_df(df):
    df = df.drop('Matches', axis=1, level=1) 

    #drop top level from general data column names
    new_columns = list(df.columns[:6].droplevel()) + list(df.columns[6:]) 
    df.columns = new_columns

    # truncate df after list of seasons
    loc = 0
    for i, season in enumerate(df['Season']):
        if str(season).endswith('Seasons'):
            loc = i
            break

    return df.head(loc)

#Concatenate rest of the tables
for i in range(3, len(tables)):
    # print(tables[i].columns, "\n")
    new_df = clean_df(tables[i]).copy()
    df = pd.concat([df,new_df[new_df.columns[6:]]], axis=1)


# add the player_id column and concatenate into main stats df
# store main stats df as postgres table

#     return df
# # truncate df after list of seasons
# def truncate_df(df):
#     loc = 0
#     for i, season in enumerate(df['Season']):
#         if str(season).endswith('Seasons'):
#             loc = i
#             break

#     return df.head(loc)

#############################################################
###################### WIKIPEDIA ############################
#############################################################

#############################################################

####### Extract text from body and retain structure #######

### figure out how to convert to json ###
import re
url = "https://en.wikipedia.org/wiki/Emile_Smith_Rowe"
# url = "https://fbref.com/en/players/21a66f6a/Harry-Kane"
soup = BeautifulSoup(requests.get(url).text)


def make_dict_entry(header_text_dict, text):
    # global content_dict
    pass

def append_dict_entry(header_text_dict, text):
    # global content_dict
    pass

def add_text(key, text):
    '''concatenate content text to existing content text at current text section of body'''
    global content_dict
    if previous_is_p:
        content_dict[key] += "\n" + text
    else:
        content_dict[key] = text

def clean_header(text):
    if text.endswith("[edit]"):
        return text[:len(text)-6]
    else:
        return text

exclude_set = {"Contents", "See also", "Notes", "References", "External links", "Navigation menu"}

body = soup.find("div", class_="mw-parser-output")
h2 = soup.find("h2")
content = re.compile('(h[2-9])|p')
# heading = re.compile('(h[2-9])')
header_order = ['h2','h3','h4','h5']
content_set = set()
# header_dict = {}
content_dict = {}
header_text_dict = {}
header_stack = [] # create function to pop all the headers equal to and including current one

previous_is_p = False

def update_header_text_dict(current_header):
    global header_text_dict
    header_index = header_order.index(current_header)
    for header in header_order[header_index:]:
        # print(header)
        try:
            del header_text_dict[header]
        except:
            continue

for c in body.children:
    if c.name is not None and \
        c.text not in exclude_set and\
        content.match(c.name):
            if c.name[0] == 'h':
                # if current header smaller than or equal to last header in header_stack
                # remove lower order headers from header text dict
                update_header_text_dict(c.name)
                header_text_dict[c.name] = clean_header(c.text)
                previous_is_p = False
                # print(header_text_dict)
                # if not, pop header stack till one above current and delete corresponding entries in header_text_dict
            else:                
                if len(header_text_dict) == 0:
                    # content_set.add(c.text)
                    key = 'opening'

                else:
                    # print(header_text_dict)
                    key = tuple(header_text_dict.values())
                add_text(key,c.text)

                previous_is_p = True
                

#############################################################
####### Get all images from Wikipedia page #######

img_list = soup.find_all("img")

thumb_list = []
im_count = 1
if len(img_list) > 0:
    for img in img_list:
        if "/thumb/" in img['src'] and "svg" not in img["src"]:
            url = "https:"+img["src"]
            file_name = "test_images/" + str(im_count)
            get_and_save_image(url, file_name)
            im_count+=1

#############################################################


#############################################################
################### COMMON FUNCTIONS ########################
#############################################################

def get_and_save_image(img_url, file_name):
    img = requests.get(img_url, stream=True)
    with open(file_name, "wb") as f:
        img.raw.decode_content = True
        shutil.copyfileobj(img.raw, f)








######## REDUNDANT ############
#### creating dictionary from data in infobox #### 

info_dict={} 
for i, tag in enumerate(infobox):
    if tag.name == "tr":        
        label_tag = tag.find(class_="infobox-label")
        try: 
            label = label_tag.text
            # print(label)    
            # print("xx")
            data_tag = tag.find(class_="infobox-data")
            data = data_tag.text
            info_dict[label] = data
            # print(data.text)
        except:
            continue
        # print ("\n XXXXXXXXXXXXXXXX \n")


