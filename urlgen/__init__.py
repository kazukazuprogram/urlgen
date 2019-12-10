#!/usr/bin/env python3
# coding: utf-8

from time import sleep
from bs4 import BeautifulSoup as bs
from requests import Session
from urllib.parse import urlparse
from sys import argv

global_proxy = None
# global_proxy = {
#     "http": "172.24.2.60:15080",
#     "https": "172.24.2.60:15080"
# }


def get(url):
    dom = urlparse(url).netloc
    # print("Domain :", dom)
    # print("Type : ", end="")
    if dom == "megaup.net":
        # print("MEGAUP")
        return megaup(url=url)
    elif dom == "uploadhaven.com":
        # print("UPLOADHAVEN")
        return uploadhaven(url=url)
    elif dom == "www.mediafire.com" or dom == "mediafire.com":
        # print("MediaFire")
        return mediafire(url=url)
    else:
        pass
        # print("UNKNOWN")


def uploadhaven(url, s=Session()):
    t = s.get(url, proxies=global_proxy).text
    f = bs(t, "lxml")
    size = f.find("td", class_="responsiveInfoTable").text.split("\n")[2].strip()
    # print(size)
    f = f.find("form", class_="contactForm")
    postdata = {
        "_token": f.find("input", attrs={"name": "_token"}).get("value"),
        "key": f.find("input", attrs={"name": "key"}).get("value"),
        "time": f.find("input", attrs={"name": "time"}).get("value"),
        "hash": f.find("input", attrs={"name": "hash"}).get("value")
    }
    for x in range(6, 0, -1):
        # print("\r" + str(x), end="")
        sleep(1)
    # print()
    p = s.post(url, data=postdata).text
    f = bs(p, "lxml").find("div", class_="download-timer").a.get("href")
    return f


def megaup(url, s=Session()):
    # print("URL :", url)
    f = bs(s.get(url, proxies=global_proxy).text, "lxml")
    clink = f.find("div", class_="row").script.text.split("href='")[1].split("'")[0]
    size = f.find("td", class_="responsiveInfoTable").text.split("\n")[2].strip()
    # print(size)
    for x in range(6, 0, -1):
        # print("\r"+str(x), end="")
        sleep(1)
    # print()
    # print(clink)
    # print("GO!")
    g = s.get(clink, proxies=global_proxy, allow_redirects=False)
    # print("OK")
    return g.headers["location"]


def mediafire(url, s=Session()):
    f = bs(s.get(url, proxies=global_proxy).text, "lxml")
    f = f.find("div", id="download_link", class_="download_link").find("a", class_="input")
    size = f.text.split()[1][1:-1]
    link = f.get("href")
    # print("Size :", size)
    return link


if __name__ == '__main__':
    try:
        url = get(argv[-1])
        # print()
        print(url)
    except Exception as e:
        pass
        # print("Error :", e)
