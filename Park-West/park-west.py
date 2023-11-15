from bs4 import BeautifulSoup # HTML parsing
from urllib.request import urlopen
import re # regex for sub
import json # for data export

url = "https://www.jamusa.com/park-west"
page = urlopen(url)
html = page.read().decode("utf-8")

soup = BeautifulSoup(html, "html.parser")

# website's title == Park West | Jam Productions
venue = re.sub("<.*?>", "", re.findall("<title.*?>.*?</title.*?>", html, re.IGNORECASE)[0])
# park-west uses this class name to separate shows
show_info = soup.select(".eventItem") 
# results found on web:
print(len(show_info), "shows found at", venue)

data = {}
i = 0
for show in show_info:
    data[i] = {}
    data[i]["date"] = show.select(".m-date__weekday")[0].text.strip() + " " + show.select(".m-date__month")[0].text.strip() + " " + show.select(".m-date__day")[0].text.strip()
    data[i]["link"] = show.find("a")["href"]
    data[i]["image"] = show.find("img")["src"]
    data[i]["title"] = show.select(".title")[0].text.strip()

    # append title if there are secondary artists
    try:
        data[i]["title"] += ", " + show.select(".tagline")[0].text.strip()
    except:
        pass

    # split time string
    times = show.select(".time")[0].text.strip().split(" / ")
    data[i]["doors-time"] = re.sub("Doors: ", "", times[0])
    data[i]["show-time"] = re.sub("Show: ", "", times[1])

    i += 1

# export to json file
with open("park-west.json", "w") as outfile:
    # json.dumps formats from python dict to json 
    outfile.write(json.dumps(data, indent=4)) 

