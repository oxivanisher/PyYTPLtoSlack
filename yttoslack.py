#!/usr/bin/env python3

from bs4 import BeautifulSoup
import urllib2
import re

html_page = urllib2.urlopen("http://gdata.youtube.com/feeds/api/playlists/PLy3-VH7qrUZ5IVq_lISnoccVIYZCMvi-8")
soup = BeautifulSoup(html_page)
for i in soup.find_all('link'):
    if "watch" in i['href']:
       print (i)
