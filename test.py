import requests
from bs4 import BeautifulSoup
import html5lib
import json
import jsonpath

# requesturl = "https://www.cricbuzz.com/cricket-news/api-paginate/news-list/all/126749/2"
requesturl = "https://www.cricbuzz.com/cricket-news"

proxies = {
    "http": "http://36.67.45.71:8080",
}
r = requests.get(requesturl, proxies=proxies)
htmlcontent = r.content
soup = BeautifulSoup(htmlcontent, 'html.parser')

dct = {
    "class": "cb-nws-hdln-ancr text-hvr-underline"
}
links = soup.find_all('a', attrs=dct)
hrefs = []
newsids = []

for link in links:
    lnks = (link.get("href"))
    hrefs.append(lnks)
s = 0
for id in hrefs[0]:
    if s == 2:
        if id != "/":
            newsids.append(id)
    if s == 3:
        break
    if id == "/":
        s += 1
newsid = ("".join(newsids))
imgs = []
images = soup.find_all(attrs="cb-lst-img")

for image in images:
    img = image.get("src")
    imgs.append(img)
print(imgs)
print(hrefs)
page = 2
newsid = int(newsid) - 10
urlid = f"https://www.cricbuzz.com/cricket-news/api-paginate/news-list/all/{newsid}/{page}"
newrequest = requests.get(urlid)
content = newrequest.content
soup2 = BeautifulSoup(content, 'html.parser')
print(soup2.prettify())
hrfs = soup2.find_all()
# print(hrfs)
next = (soup2.find_all(attrs={"class": "ajax-pagination"}))
for nxt in next:
    print(nxt.get("url"))

"""    
    "https://180.180.171.121",
    "https://61.7.138.107",
    "https://12.218.209.130",
    "https://1.20.100.227",
    "https://145.253.188.132",
    "https://118.173.233.149",
    "https://195.201.61.51",
    "https://217.79.181.109",
    "https://140.227.61.25",
    "https://91.202.240.208",
    "https://194.36.145.18",
    "https://51.159.24.172",
    "https://176.113.209.145",
    "https://157.230.86.93",
    "https://1.1.189.58",
    "https://158.51.201.249",
    "https://186.225.46.90",
    "https://121.125.54.228",
    "https://69.65.65.178",
    "https://187.33.208.120",
    "https://151.22.181.223",
    "https://131.108.118.27",
    "https://141.98.134.2",
    "https://88.198.24.108",
    "https://184.181.217.210",
    "https://207.144.111.230",
    "https://115.75.1.184",
    "https://65.184.156.234",
    "https://200.52.148.194",
    "https://143.55.57.18",
    "https://5.252.161.48",
    "https://102.129.249.120",
    "https://167.172.191.249",
    "https://176.9.75.42",
    "https://128.199.202.122",
    "https://139.59.1.14",
    "https://87.107.146.20",
    "https://184.178.172.14",
    "https://103.85.232.146",
    "https://151.22.181.213",
    "https://150.129.151.62",
    "https://66.135.227.181",
    "https://70.185.68.155",
    "https://198.199.86.11",
    "https://109.127.82.66",
    "https://161.35.70.249",
    "https://13.36.233.195",
    "https://1.20.166.142",
    "https://103.250.166.4",
    "https://98.184.33.205" """
proxies = {
    "http": "http://36.67.45.71:8080",
    # "https":"http://36.67.45.71:8080"
}
# s = requests.get("https://www.javatpoint.com/proxy-server-list", proxies=proxies)

from urllib.parse import quote

post_slug = "cricket-news/127120/mis-project-brevis-reaches-american-checkpoint-dewald-brevis-mumbai-indians"
encoded_slug = quote(post_slug)

anchor_tag = f'<a href="/newsdetils/{encoded_slug}">Link</a>'
print(anchor_tag)