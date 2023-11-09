from bs4 import BeautifulSoup # HTML parsing
from urllib.request import urlopen
import re # regex for sub
import json # for data export

url = "https://lh-st.com"
page = urlopen(url)
html = page.read().decode("utf-8")

soup = BeautifulSoup(html, "html.parser")

# website's title == Schubas Tavern || Lincoln Hall - Chicago, IL
venue = re.sub("<.*?>", "", re.findall("<title.*?>.*?</title.*?>", html, re.IGNORECASE)[0])
# lh-st uses this class name to separate shows
show_info = soup.select(".col") 
# results found on web:
print(len(show_info), "shows found at", venue)

data = {}
i = 0
for show in show_info:
    data[i] = {}
    '''
        convert
            title = str(show.select(".card-title"))
            title = re.sub(r"<.*?>", "", title)
            title = title.strip("[] ")
        into one line

    '''
    # Ex: Ajani Jones, Wic Whitney, Kweku Collins, DJ Mochi 
    data[i]["title"] = re.sub(r"<.*?>", "", str(show.select(".card-title"))).strip("[]")
    data[i]["title-sub"] = re.sub(r"<.*?>", "", str(show.select(".tessera-additionalArtists"))).strip("[]")
    # Lincoln Hall or Schubas 
    data[i]["location"] = show.select(".tessera-venue")[0].text.strip(" ")
    # Ex: Nov 09
    data[i]["date"] = show.select(".tessera-date")[0].text.strip("\n ")
    # Use image for display with link to venue website
    data[i]["image"] = show.select(".card-img-top")[0]["src"]
    data[i]["link"] = show.select(".tessera-has-inventory")[0].find("a")["href"]
    # additional info
    data[i]["age-group"] = show.select(".showAges")[0].text
    data[i]["doors-time"] = show.select(".tessera-doorsTime")[0].text
    data[i]["show-time"] = show.select(".tessera-showTime")[0].text
    i += 1

# export to json file
with open("lh-st.json", "w") as outfile:
    # json.dumps formats from python dict to json 
    outfile.write(json.dumps(data, indent=4)) 
