import requests
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen


def getTitles():
    pnames = []
    source = requests.get('https://www.indeed.com/jobs?q=computer+science&l=').text
    soup = BeautifulSoup(source, 'lxml')

    for pos in soup.find_all('div', class_='title'):
        name = pos.a.get('title')
        #print (name)
        pnames.append(name)
    return (pnames)


def getCompanies():
    companies = []
    source = requests.get('https://www.indeed.com/jobs?q=computer+science&l=').text
    soup = BeautifulSoup(source, 'lxml')
    
    for div in soup.find_all(name='div', attrs={'class':'row'}):
        company = div.find_all(name='span', attrs={'class':'company'})
        if len(company) > 0:
          for b in company:
            companies.append(b.text.strip())
        else:
          sec_try = div.find_all(name='span', attrs={'class':'result-link-source'})
          for span in sec_try:
              companies.append(span.text.strip())
    return(companies)


def getLocations():
    locations = []
    source = requests.get('https://www.indeed.com/jobs?q=computer+science&l=').text
    soup = BeautifulSoup(source, 'lxml')
    spans = soup.findAll('span', attrs={'class': 'location'})
    for span in spans:
        locations.append(span.text)

    return(locations)


def getPay():
    source = requests.get('https://www.indeed.com/jobs?q=computer+science&l=').text
    soup = BeautifulSoup(source, 'lxml')  
    sal = []
    for div in soup.find_all(name='div', attrs={'class':'row'}):
        try:
            sal.append(div.find('nobr').text)
        except:
          try:
            d2 = div.find(name='div', attrs={'class':'sjcl'})
            div3 = div2.find('div')
            sal.append(div3.text.strip())
          except:
            sal.append('N/A')
    return(sal)



#the short description provided
def getShortDesc():
    source = requests.get('https://www.indeed.com/jobs?q=computer+science&l=').text
    soup = BeautifulSoup(source, 'lxml') 
    summaries = []
    spans = soup.find_all('div', class_='summary')
    for span in spans:
        summaries.append(span.text.strip())
    return(summaries)


def getLinks():
    links = []
    source = requests.get('https://www.indeed.com/jobs?q=computer+science&l=').text
    soup = BeautifulSoup(source, 'lxml')

    for pos in soup.find_all('div', class_='title'):
        link = pos.a.get('href')
        links.append("https://www.indeed.com" + link)
    return (links)



#returns some headers (not sure how to fix)
def getFullDesc(link):
    #descs = []
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')
    desc = soup.find('div', class_='jobsearch-jobDescriptionText').findAll('p')
    return  (desc)




#need getSkills, getCategory, Create()







