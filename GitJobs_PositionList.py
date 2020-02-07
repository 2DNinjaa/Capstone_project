import requests
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen

source = requests.get('https://jobs.github.com/positions').text
soup = BeautifulSoup(source, 'lxml')

#--> prints out all job titles, locations, company, and fulltime or not full time

#summary = soup.find('div', class_='column main').text (does same thing)


#the "table" and "positionlist" strings were found using inspect element on the website (f12)

def positionList():
    source = requests.get('https://jobs.github.com/positions').text
    soup = BeautifulSoup(source, 'lxml')
    summary = soup.find('table', class_='positionlist').text
    print (summary)
