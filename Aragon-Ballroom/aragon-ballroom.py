from bs4 import BeautifulSoup # HTML parsing
from urllib.request import urlopen
import re # regex for sub
import json # for data export

url = "https://www.livenation.com/venue/KovZpZAFdJnA/byline-bank-aragon-ballroom-events"
page = urlopen(url)
html = page.read().decode("utf-8")

soup = BeautifulSoup(html, "html.parser")

# venue name == Aragon Ballroom
venue = "Aragon Ballroom"
# livenation uses this class name to separate shows
show_info = soup.select(".css-re1cpl") 
# results found on web
print(len(show_info), "shows found at", venue)

data = {}
i = 0
for show in show_info:
    
    data[i] = {}
    data[i]["title"] = show.select(".css-1ptng6s")[0].text
    data[i]["location"] = venue
    data[i]["genre"] = show.select(".css-1rr5jlm")[0].text
    data[i]["link"] = show.find("a")["href"]
    data[i]["image"] = show.select(".css-1pdwaq0")[0].find("img")["src"]
    # instead of text, could do ["datetime"] to get full/unformatted date
    data[i]["date"] = show.select(".css-qjpp58")[0].find("time").text

    i += 1

# export to json file
with open("aragon-ballroom.json", "w") as outfile:
    # json.dumps formats from python dict to json 
    outfile.write(json.dumps(data, indent=4)) 