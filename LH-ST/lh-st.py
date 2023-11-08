# following https://realpython.com/python-web-scraping-practical-introduction/#build-your-first-web-scraper

from urllib.request import urlopen # to grab website data
import re # regex

url = "https://lh-st.com/"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")


result = re.findall("<img.*>", html)
print(result)