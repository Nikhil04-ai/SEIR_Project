import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("Enter URL")
    sys.exit()

url = sys.argv[1]

res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(res.text, "html.parser")

if soup.title:
    print(soup.title.string.strip())
else:
    print("No title")
print()

main = soup.find("div", id="mw-content-text")

if main:
    paras = main.find_all("p")
else:
    paras = soup.find_all("p")

for p in paras:
    t = p.get_text().strip()
    if t:
        print(t)
        print()

for a in soup.find_all("a"):
    href = a.get("href")
    if href:
        print(href)