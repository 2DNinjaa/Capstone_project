#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen


# In[18]:


source = requests.get('https://jobs.github.com/positions').text
soup = BeautifulSoup(source, 'lxml')
summary = ""

#--> prints out all job titles, locations, company, and fulltime or not full time


# In[3]:


#summary = soup.find('div', class_='column main').text (does same thing)


#the "table" and "positionlist" strings were found using inspect element on the website (f12)
def positionList():
    try:
        summary = soup.find('table', class_='positionlist').text
    except:
        summary = soup.find('table', class_='positionlist')


# In[4]:


#prints the location of each job
#print(soup.find_all('span', class_='location'))

def getLocations():
    locations = []
    for loc in soup.find_all('span', class_='location'):
        locations.append(loc.text)
    print(locations)


# In[5]:


#prints the time the job was posted
#print(soup.find_all('span', class_='relatized'))

def getTimes():
    timePosted = []
    for time in soup.find_all('span', class_='relatized'):
        timePosted.append(time.text)
    print(timePosted)


# In[6]:


#prints the company name
#print(soup.find_all('a', class_='company'))

def getCompany():
    allCompany = []
    for co in soup.find_all('a', class_='company'):
        allCompany.append(co.text)
    print(allCompany)


# In[7]:


#prints all the job titles
#title container doesn't have class so it searches nearest parent container's class

def getTitles():
    for table in soup.find_all('td', {'class':'title'} ):
        links.append(table.find_all('h4'))
    #print(links)

    jobTitles = []
    for title in links:
        try:
            jobTitles.append(title.text)
        except: #titles are returned strangely, some results are returned as lists
            jobTitles.append(title[0].text)

    print(jobTitles)


# In[8]:


#prints full time or contract work
#class names vary
def getWork():
    print(soup.find_all('strong', class_='fulltime'))
    print(soup.find_all('strong', class_='contract'))


# In[31]:


# returns a list which contains sublists for each job entry
jobs = []
links = []

def getJobsFormatted():
    for job in soup.find_all('tr', {'class':'job'} ):
        tmp = job.text.strip().split('\n')
        jb = []
        for x in tmp:
            y = x.strip()
            if len(y) > 1 and not "\t" in y:
                jb.append(x.strip())
        jobs.append(jb)        
    print(jobs)


# In[4]:


# helper function for getJobWLnks
# assumes url is a job page on the github jobs api
# returns the link where the user can apply to the company
# or this page (as specified by url) if none provided
def getLink(url):
    newSrc = requests.get(url).text
    newSoup = BeautifulSoup(newSrc, 'lxml')
    jobLink = newSoup.find('div', {'class':'highlighted'}).find('a')
    return url if jobLink == None else jobLink['href']


# In[19]:


jobsWL = []

# similar to getJobsFormatted
# however it also includes a link where the user can apply to the company
def getJobWLnks():
    for job in soup.find_all('tr', {'class':'job'} ):
        link = getLink(job.find('td', {'class':'title'}).find('h4').find('a')['href'])
        tmp = job.text.strip().split('\n')
        jb = []
        for x in tmp:
            y = x.strip()
            if len(y) > 1 and not "\t" in y:
                jb.append(x.strip())
        jb.append(link)
        jobsWL.append(jb) 
        
#getJobWLnks()
#print(jobsWL)


# In[21]:


#getJobWLnks()
#print(jobsWL)


# In[14]:


multPageJobsWL = []

# includes links and searches multiple pages
def getJobLP(numPages):
    for i in range (1, numPages):
        url = 'https://jobs.github.com/positions'
        finalurl = url + 'page=' + str(i)
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        
        for job in soup.find_all('tr', {'class':'job'} ):
            link = getLink(job.find('td', {'class':'title'}).find('h4').find('a')['href'])
            tmp = job.text.strip().split('\n')
            jb = []
            for x in tmp:
                y = x.strip()
                if len(y) > 1 and not "\t" in y:
                    jb.append(x.strip())
            jb.append(link)
            multPageJobsWL.append(jb) 


# In[16]:


#getJobLP(2)
#print(multPageJobsWL)


# In[2]:


multPageLocJobsWL = []

# searches multiple pages and the given location
# also returns links
def getJobLLP(loc, numPages):
    for i in range (1, numPages):
        loc = loc.replace(' ', '+')
        url = 'https://jobs.github.com/positions' + '?page=' + str(i)
        #resolvedURL = url + "?page=" + str(i)
        finalURL = url + '&location='+ loc
        source = requests.get(finalURL).text
        soup = BeautifulSoup(source, 'lxml')
        
        for job in soup.find_all('tr', {'class':'job'} ):
            link = getLink(job.find('td', {'class':'title'}).find('h4').find('a')['href'])
            tmp = job.text.strip().split('\n')
            jb = []
            for x in tmp:
                y = x.strip()
                if len(y) > 1 and not "\t" in y:
                    jb.append(x.strip())
            jb.append(link)
            multPageLocJobsWL.append(jb) 


# In[5]:


#getJobLLP('chicago', 3)
#print(multPageLocJobsWL)


# In[ ]:




