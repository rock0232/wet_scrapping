import json

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template #, request, session, redirect

proxies = {
    "http": "http://36.67.45.71:8080",
}

def soup():
    requesturl = "https://www.cricbuzz.com/cricket-news"

    r = requests.get(requesturl, proxies=proxies)
    htmlcontent = r.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    return soup


# get the new title
def getnewstitle():
    titles = []
    links = []
    title = soup().select("a.cb-nws-hdln-ancr.text-hvr-underline")
    for i in range(10):
        titledata = title[i].string
        titles.append(titledata)
        link = title[i].get("href")
        links.append("https://www.cricbuzz.com" + link)
    return titles, links


# get the news subtitle
def getnewssubtitle():
    subs = []
    subtitles = soup().select("div.cb-nws-intr")
    for subtitle in subtitles:
        subtitledata = subtitle.string
        subs.append(subtitledata)
    return subs

# get news time
def getnewstype():
    newstimes = []
    categorylist = []
    newstime = soup().select("div.cb-nws-time")
    for newstype in newstime:
        newsdate = newstype.text
        newstimes.append(newsdate)
        for ntype in newsdate:
            if ntype != '\xa0':
                categorylist.append(ntype)
            else:
                categorylist.append("+")
        categorylist.append("+")

    # get news category
    categories = ("".join(categorylist).split("+"))
    data = [cat for cat in categories if cat != "•"]
    category = data[::2]
    event = data[1::2]

    return category, event


# get news image
def getnewsimage():
    imgs = []
    images = soup().select("img.cb-lst-img")
    for i in range(len(images)):
        img = images[i].get("src")
        try:
            imgs.append("https://www.cricbuzz.com" + img)
        except:
            img = images[i].get("source")
            imgs.append("https://www.cricbuzz.com" + img)
    return imgs

# get next url
titles, links = getnewstitle()
nexturl = int((links[0].split("/")[-2])) - 9
page = 2


app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/coding"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'coding'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route("/")
def home():
    category, event = getnewstype()
    subs = getnewssubtitle()
    newstimes = getnewstype()
    imgs = getnewsimage()

    return render_template("index.html", titles=titles, links=links, subs=subs, newstimes=newstimes, imgs=imgs,
                           category=category, event=event)


@app.route("/newsdetils", methods=["GET"])
def details():
    return render_template("newsdetail.html")


@app.route("/demo", methods=["GET"])
def news():
    category, event = getnewstype()
    subs = getnewssubtitle()
    newstimes = getnewstype()
    imgs = getnewsimage()
    # titles.clear(), links.clear(), subs.clear(), newstimes.clear(), imgs.clear(), categorylist.clear(), category.clear(), event.clear()
    url = f"https://www.cricbuzz.com/cricket-news/api-paginate/news-list/all/{nexturl}/{page}"
    # print(categorylist)
    nr = requests.get(url, proxies=proxies)
    conent = nr.content
    soup2 = BeautifulSoup(conent, 'html.parser')
    pg2title = soup2.select("a.cb-nws-hdln-ancr.text-hvr-underline")
    for i in range(10):
        titledata = pg2title[i].string
        titles.append(titledata)
        link = pg2title[i].get("href")
        links.append("https://www.cricbuzz.com" + link)

    pg2images = soup2.select("img.cb-lst-img")
    imgs2 = []
    # print(pg2images)
    for i in range(len(pg2images)):
        img = pg2images[i].get("src")
        try:
            imgs2.append("https://www.cricbuzz.com" + img)
        except:
            img = pg2images[i].get("source")
            imgs2.append("https://www.cricbuzz.com" + img)

    pg2subtitle = soup2.select("div.cb-nws-intr")
    subs2 = []
    for subtitle in pg2subtitle:
        subtitledata = subtitle.string
        subs2.append(subtitledata)

    pg2categories = []
    pg2newstime = soup2.select("div.cb-nws-time")
    newstimes2 = []
    # print(pg2newstime)
    for newstype in pg2newstime:
        newsdate = newstype.text
        newstimes2.append(newsdate)
        for ntype in newsdate:
            if ntype != '\xa0':
                pg2categories.append(ntype)
            else:
                pg2categories.append("+")
        pg2categories.append("+")

    pg2categorieslist = ("".join(pg2categories).split("+"))
    data = [cat for cat in pg2categorieslist if cat != "•"]
    pgcategory = data[::2]
    pgcategory = category[:10] + pgcategory[:10]
    pgevent = event + data[1::2]
    print(len(pgevent))
    print(len(titles))
    print(len(links))
    print(len(subs))
    print(len(newstimes))
    print(len(imgs))
    print(len(pgcategory))





    jsondata = {
        'titles': titles,
        'links': links,
        'subs': subs,
        'newstimes': newstimes,
        'imgs': imgs,
        'category': pgcategory,
        'event': pgevent
    }
    json_data = json.dumps(jsondata)
    return json_data
    # return titles, links, subs,newstimes , imgs, category, event


if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
