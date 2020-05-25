#!/usr/bin/env python3
# coding: utf-8

from time import sleep
from bs4 import BeautifulSoup as bs
from requests import Session
from urllib.parse import urlparse
from sys import argv, stdout, stderr
from getpass import getpass
import logging
from subprocess import Popen
from os import environ

formatter = "[%(levelname)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=formatter)
global_proxy = None
external_download_command = "aria2c {}"
# global_proxy = {
#     "http": "172.24.2.60:15080",
#     "https": "172.24.2.60:15080"
# }


def get(url, s=Session()):
    dom = urlparse(url).netloc
    if dom == "megaup.net":
        stderr.write("TYPE : MEGAUPLOAD\n")
        resurl = megaup(url=url, s=s)
    elif dom == "uploadhaven.com":
        stderr.write("TYPE : UploadHaven\n")
        resurl = uploadhaven(url=url, s=s)
    elif dom == "drive.google.com":
        stderr.write("TYPE : Google Drive\n")
        resurl = gdrive(url=url, s=s)
    elif dom.split(".")[-2:] == ["zippyshare", "com"]:
        stderr.write("TYPE : Zippyshare\n")
        resurl = zippyshare(url=url, s=s)
    elif dom.split(".")[-2:] == ['mediafire', 'com']:
        stderr.write("TYPE : MediaFire\n")
        resurl = mediafire(url=url, s=s)
    elif dom == "ux.getuploader.com":
        stderr.write("TYPE : uploader.jp\n")
        resurl = uploaderjp(url=url, s=s)
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
    str = f.select_one("div.row script").string.strip()
    for x in str.split("\n"):
        if "href=" in x:
            tag = x.split("\"")[1]
            url = bs(tag, "lxml").a.get("href")
            break
    for x in range(5, -1, -1):
        stderr.write("\rCount: {}".format(x))
        sleep(1)
    stderr.write("\n")
    g = s.get(url, proxies=global_proxy, allow_redirects=False)
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
    f = f.find("div", class_="right").script.string.strip()
    f = f.split("\n")[0].split("=")[1].strip().replace("(", "str(")[:-1]
    url = "https://" + urlparse(url).netloc + eval(f)
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


def external_download(url):
    if "EXDLCOM" in list(environ):
        # Specify download command from args in the future
        com = environ["EXDLCOM"].format(url)
    else:
        com = external_download_command.format(url)
    p = Popen(com)
    p.wait()


def native_download(url, s=Session()):
    logging.info("NativeDownloader start")
    g = s.get(url, stream=True, allow_redirects=True)
    logging.info("Response: %s", g.status_code)
    length = g.headers["Content-Length"]
    for x in [x.strip() for x in g.headers["Content-Disposition"].split(";")]:
        if x[1][:9] == "filename=":
            filename = x[1][10:-1]
            break
    print(length, filename)


def wrapper(url=None, s=Session()):
    try:
        if url is not None:
            pass
        elif len(argv) >= 2:
            url = argv[1]
        else:
            stderr.write("URL>")
            url = input()
        url = get(url=url, s=s)
        if "--download" in argv or "-d" in argv or True:
            native_download(url, s=s)
        elif "--external-download" in argv or "-D" in argv:
            external_download(url)
        else:
            stdout.write(url)
    except Exception as e:
        stderr.write("Error :", e, "\n")


if __name__ == '__main__':
    wrapper()
