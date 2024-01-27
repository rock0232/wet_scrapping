import json
import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify  # , request, session, redirect
import pypyodbc as odbc

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-0SBGOOB'
DATABASE_NAME = 'rock_database'

connection_string = f"""
    DRIVER = {{{DRIVER_NAME}}};
    SERVER = {SERVER_NAME};
    DATABASE = {DATABASE_NAME};
    trust_Connection = yes;
"""

app = Flask(__name__)

# import pyodbc
# cnxn = pyodbc.connect('DRIVER={Devart ODBC Driver for SQL Server};Server=myserver;Database=mydatabase;Port=myport;User ID=myuserid;Password=mypassword')


proxies = {
    "http": "http://36.67.45.71:8080",
}
# global page_index
page_index = 2


def soup():
    requesturl = "https://www.cricbuzz.com/cricket-news"

    r = requests.get(requesturl, proxies=proxies)
    htmlcontent = r.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    return soup


def soup2data(url):
    requesturl = url
    r = requests.get(requesturl, proxies=proxies)
    htmlcontent = r.content
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    return soup


# get the new title
def getnewstitle():
    titles = []
    links = []
    title = soup().select("a.cb-nws-hdln-ancr.text-hvr-underline")
    for i in range(len(title)):
        titledata = title[i].string
        titles.append(titledata)
        link = title[i].get("href")
        # links.append("https://www.cricbuzz.com" + link)
        links.append(link)
    return list(titles)[:10], list(links[:-6])


# get the news subtitle
def getnewssubtitle():
    subs = []
    subtitles = soup().select("div.cb-nws-intr")
    for subtitle in subtitles:
        subtitledata = subtitle.string
        subs.append(subtitledata)
    return list(subs)


def getnewstime():
    times = []
    newstime = soup().select('span.cb-nws-time')
    for time in newstime:
        time = time.string
        times.append(time)
    return times


# get news category and event
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
    return list(category)[0:10], list(event)


# get news image
def getnewsimage():
    imgs = []
    images = soup().select("img.cb-lst-img")
    for i in range(len(images)):
        img = images[i].get("src")
        try:
            imgs.append(img)
        except:
            img = images[i].get("source")
            imgs.append(img)
    return list(imgs[:-6])


def getnexturl():
    nexturl = soup().select("div.ajax-pagination")[0].get("url")
    updated_string = "/".join(nexturl.split("/")[:-1])
    # print(updated_string)
    return nexturl


# to connect to mysql
# app = Flask(__name__)
# app.secret_key = 'super-secret-key'
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/coding"
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'coding'
#
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route("/")
def home():
    global page_index
    category, event = getnewstype()
    newstimes = getnewstime()
    subs = getnewssubtitle()
    titles, links = getnewstitle()
    nexturl = getnexturl()
    # newstimes = getnewstype()
    imgs = getnewsimage()
    page_index = 2
    nexturl = ''
    jsondata = {
        'titles': titles,
        'links': links,
        'subs': subs,
        'imgs': imgs,
        'category': category,
        'event': event,
        'newstimes': newstimes
    }
    sp = 0
    # print(sp)
    sp += 1
    return render_template("index.html", titles=titles, links=links, subs=subs, imgs=imgs,
                           category=category, event=event, nexturl=nexturl, newstimes=newstimes)


# <string:url>

@app.route("/newsdetils/<path:slug>", methods=['GET', 'POST'])
def details(slug):
    url = "https://www.cricbuzz.com/" + slug
    nr = requests.get(url)
    # print(url)
    conent = nr.content
    soup = (BeautifulSoup(conent, 'html.parser'))
    # print(soup)
    img = soup.select("img.cursor-pointer")
    img = [img.get('src') for img in img]
    backgroundimage = img[0]
    text = soup.select("p.cb-nws-para")
    para = []
    for texts in text:
        para.append(texts.text)
    return render_template("newsdata.html", data=para, image=backgroundimage)


nexturl = ""


@app.route("/demo", methods=["POST", "GET"])
def news():
    global page_index
    global nexturl
    if page_index > 2:
        nexturl = nexturl
    else:
        nexturl = getnexturl()
    if page_index > 10:
        parts = nexturl.split("/")
        parts2 = nexturl.split("/")[:-2]
        parts2 = ("/".join(parts2[:]))
        value1 = int(parts[-2]) - 10
        value2 = int(parts[-1]) + 1
        lstdata = "/" + str(parts2) + "/" + str(value1) + "/" + str(value2)
        nexturl = "".join(lstdata[1:])

    url = "https://www.cricbuzz.com" + nexturl
    nr = requests.get(url, proxies=proxies)

    conent = nr.content
    soup2 = BeautifulSoup(conent, 'html.parser')

    pg2titles = []
    pg2links = []
    pg2title = soup2.select("a.cb-nws-hdln-ancr.text-hvr-underline")
    for i in range(10):
        titledata = pg2title[i].string
        pg2titles.append(titledata)
        link = pg2title[i].get("href")
        pg2links.append(link)

    pg2images = soup2.select("img.cb-lst-img")
    imgs2 = []
    for i in range(len(pg2images)):
        img = pg2images[i].get("src")
        try:
            imgs2.append(img)
        except:
            img = pg2images[i].get("source")
            imgs2.append(img)

    pg2subtitle = soup2.select("div.cb-nws-intr")
    subs2 = []
    for subtitle in pg2subtitle:
        subtitledata = subtitle.string
        subs2.append(subtitledata)

    pg2categories = []
    pg2newstime = soup2.select("div.cb-nws-time")
    newstimes2 = []
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
    pgcategory = pgcategory[:10]
    pgevent = data[1::2]
    subs = subs2
    imgs = imgs2
    pgcategory = pgcategory

    times = []
    newstime = soup2.select('span.cb-nws-time')
    for time in newstime:
        time = time.string
        times.append(time)
        # return times

    jsondata = {
        'titles': pg2titles,
        'links': pg2links,
        'subs': subs,
        'imgs': imgs,
        'category': pgcategory,
        'event': pgevent,
        'newstimes': times,
        'nexturl': nexturl
    }
    json_data = json.dumps(jsondata)
    page_index += 1
    try:
        nexturl = soup2.select("div.ajax-pagination")[0].get("url")
    except:
        pass
    sp = 0
    # print(sp)
    sp += 1
    return json_data


if __name__ == "__main__":
    app.run(debug=False)
