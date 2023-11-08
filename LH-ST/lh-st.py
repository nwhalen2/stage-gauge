from bs4 import BeautifulSoup # HTML parsing
from urllib.request import urlopen
import re # regex for sub

url = "https://lh-st.com"
page = urlopen(url)
html = page.read().decode("utf-8")

soup = BeautifulSoup(html, "html.parser")
images = soup.find_all("img")
for image in images:
    #print(image["src"])
    pass

images = re.findall("<img.*?>", html)
title = re.findall("<title.*?>.*?</title.*?>", html, re.IGNORECASE)
for t in title:
    print(re.sub("<.*?>", "", t))

show_info = soup.select(".col")
for show in show_info:
    title = str(show.select(".card-title"))
    title = re.sub(r"<.*?>", "", title)
    title = title.strip("[]")
    print(title)