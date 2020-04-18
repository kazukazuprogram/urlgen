#!/usr/bin/env python3
# coding: utf-8

from time import sleep
from bs4 import BeautifulSoup as bs
from requests import Session
from urllib.parse import urlparse
from sys import argv, stderr
from getpass import getpass

global_proxy = None
# global_proxy = {
#     "http": "172.24.2.60:15080",
#     "https": "172.24.2.60:15080"
# }


def get(url):
    dom = urlparse(url).netloc
    if dom == "megaup.net":
        stderr.write("TYPE : MEGAUPLOAD\n")
        resurl = megaup(url=url)
    elif dom == "uploadhaven.com":
        stderr.write("TYPE : UploadHaven\n")
        resurl = uploadhaven(url=url)
    elif dom == "drive.google.com":
        stderr.write("TYPE : Google Drive\n")
        resurl = gdrive(url=url)
    elif dom.split(".")[-2:] == ["zippyshare", "com"]:
        stderr.write("TYPE : Zippyshare\n")
        resurl = zippyshare(url=url)
    elif dom.split(".")[-2:] == ['mediafire', 'com']:
        stderr.write("TYPE : MediaFire\n")
        resurl = mediafire(url=url)
    elif dom == "ux.getuploader.com":
        stderr.write("TYPE : uploader.jp\n")
        resurl = uploaderjp(url=url)
    else:
        pass
    return resurl


def uploadhaven(url, s=Session()):
    t = s.get(url, proxies=global_proxy).text
    f = bs(t, "lxml")
    f = f.find("form", class_="contactForm")
    postdata = {
        "_token": f.find("input", attrs={"name": "_token"}).get("value"),
        "key": f.find("input", attrs={"name": "key"}).get("value"),
        "time": f.find("input", attrs={"name": "time"}).get("value"),
        "hash": f.find("input", attrs={"name": "hash"}).get("value")
    }
    for x in range(6, 0, -1):
        sleep(1)
    p = s.post(url, data=postdata).text
    f = bs(p, "lxml").find("div", class_="download-timer").a.get("href")
    return f


def megaup(url, s=Session()):
    f = bs(s.get(url, proxies=global_proxy).text, "lxml")
    clink = f.find("div",
                   class_="row").script.text.split("href='")[1].split("'")[0]
    for x in range(6, 0, -1):
        sleep(1)
    g = s.get(clink, proxies=global_proxy, allow_redirects=False)
    return g.headers["location"]


def mediafire(url, s=Session()):
    f = bs(s.get(url, proxies=global_proxy).text, "lxml")
    f = f.find("div", id="download_link",
               class_="download_link").find("a", class_="input")
    link = f.get("href")
    return link


def gdrive(url, s=Session()):
    p = urlparse(url).path.split("/")[1:]
    if p[0:2] == ["file", "d"]:
        id = p[2]
    elif p[-1] == "uc":
        id = urlparse(url).query.split("id=")[1].split("&")[0]
    url = "https://drive.google.com/uc?id={}&export=download".format(id)
    g = s.get(url)
    f = bs(g.text, "lxml")
    url = "https://drive.google.com" + \
        f.find("a", id="uc-download-link").get("href")
    o = s.head(url, allow_redirects=True)
    return o.url


def zippyshare(url, s=Session()):
    g = s.get(url)
    f = bs(g.text, "lxml")
    url = "https://" + urlparse(url).netloc + \
        f.find("a", id="dlbutton").get("href")
    return url


def uploaderjp(url, pw=None, s=Session()):
    g = s.get(url)
    f = bs(g.text, "lxml")
    f = f.find("form", attrs={"name": "agree"})
    if f.input.get("name") == "password":
        if pw is None:
            try:
                pw = argv[argv.index("--password") + 1]
            except ValueError:
                password = getpass("Enter password:")
                uploaderjp(url=url, pw=password, s=s)
        pdata = {
            "password": pw
        }
        p = s.post(g.url, data=pdata)
        f = bs(p.text, "lxml")
        f = f.find("form", attrs={"name": "agree"})
    pdata = {
        "token": f.input.get("value")
    }
    p = s.post(g.url, data=pdata)
    f = bs(p.text, "lxml")
    res = f.find("div", class_="text-center").a.get("href")
    return res


def wrapper():
    try:
        if len(argv) >= 2:
            url = argv[1]
        else:
            url = input()
        url = get(url)
        print(url)
    except Exception as e:
        print("Error :", e)


if __name__ == '__main__':
    wrapper()
