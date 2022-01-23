def get_personal_info(soup):
    print("in get_personal_info")
    
    personal_info = {}
    
    name_tag = soup.find("h1",attrs={"itemprop":"name"})
    personal_info["name"] = name_tag.text.strip("\n")
    personal_info["full_name"] = name_tag.parent.next_sibling.text
    
    

    # birth_place = soup.find(attrs={"itemprop":"birthPlace"}).text
    personal_info["birth_date"] = soup.find(attrs={"itemprop":"birthDate"})["data-birth"]
    personal_info["height"] = soup.find(attrs={"itemprop":"height"}).text.strip("\n")
    personal_info["weight"] = soup.find(attrs={"itemprop":"weight"}).text.strip("\n")

    #get twitter link
    # links = soup.findAll("a")
    # for link in links:
    #     if link.has_attr("href") and \
    #     "twitter.com" in link["href"] and \
    #     "FBref" not in link["href"]:            
    #         twitter_handle = link["href"][20:]
    # print(twitter_handle)
    

    return personal_info


def test():
    print('parser works')

if __name__ == "__main__":
    print("parser imported")