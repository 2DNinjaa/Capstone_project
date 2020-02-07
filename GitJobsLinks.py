import requests
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen


#prints links of positions by location (city or state)
def links(local):
    loc = local.replace(' ', '+')
    url = 'https://jobs.github.com/positions?utf8=%E2%9C%93&description=&location=' + loc
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    for link in soup.find_all('a'):
        links = link.get('href')
        if "http" in links and '/positions/' in links:
           print (links)


#prints links of positions without location specification 
def onlylinks():
    url = 'https://jobs.github.com/positions'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    for link in soup.find_all('a'):
        links = link.get('href')
        if "http" in links and '/positions/' in links:
           print (links)


#prints links for positions through page x
def linksMultPages(x):
    x=x           
    for i in range (1,x):
        url = 'https://jobs.github.com/positions'
        finalurl = url + "?page=" + str(i)
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        
        for link in soup.find_all('a'):
            links = link.get('href')
            if "http" in links and '/positions/' in links:
               print (links)


#prints links for positions through page x in location loc
#for this website there usually isnt multiple pages so this might not be necessary.
def linksMultPagesLoc(x, loc):
    x=x
    loc = loc
    for i in range (1,x):
        loc = loc.replace(' ', '+')
        url = 'https://jobs.github.com/positions'
        url2 = url + "?page=" + str(i)
        finalurl = url2 + loc
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        
        for link in soup.find_all('a'):
            links = link.get('href')
            if "http" in links and '/positions/' in links:
               print (links)
