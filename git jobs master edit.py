#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen


# In[23]:


###CAN CHANGE TO RUN LINKS THROUGH METHODS (have links as method parameters)

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


#returns list of links of positions without location specification 
def onlylinks():
    linklist =[]
    url = 'https://jobs.github.com/positions'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    for link in soup.find_all('a'):
        links = link.get('href')
        if "http" in links and '/positions/' in links:
           #print (links)
            linklist.append(link['href'])
    return linklist


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



#prints out all job titles, locations, company, and fulltime or not full time
def PositionList():
    source = requests.get('https://jobs.github.com/positions').text
    soup = BeautifulSoup(source, 'lxml')

    for pos in soup.find_all('table', class_='positionlist'):
        desc = pos.text
        print (desc)


#returns list of the titles of all the positions on the page    
def positionNamesOnly():
    pnames = []
    source = requests.get('https://jobs.github.com/positions').text
    soup = BeautifulSoup(source, 'lxml')

    for pos in soup.find_all('tr', class_='job'):
        name = pos.td.h4.text
        #print (name)
        pnames.append(name)
    return (pnames)


#returns list of the company names 
def company():
    cos = []
    source = requests.get('https://jobs.github.com/positions').text
    soup = BeautifulSoup(source, 'lxml')

    for co in soup.find_all('a', class_='company'):
        coname = co.text
        #print (coname)
        cos.append(coname)
        
    return (cos)


#returns list of the locations
def location():
    locs = []
    source = requests.get('https://jobs.github.com/positions').text
    soup = BeautifulSoup(source, 'lxml')

    for pos in soup.find_all('span', class_='location'): #td, meta
        loc = pos.text
        #print (loc)
        locs.append(loc)
    return (locs)
        
    


#returns list of the times created
def timeCreated():
    tcr = []
    source = requests.get('https://jobs.github.com/positions').text
    soup = BeautifulSoup(source, 'lxml')

    for pos in soup.find_all('span', class_='when relatize relatized'):
        time = pos.text
        tcr.append(time)
    return (tcr)


#returns list of full/parttime
def FullTime():
    ft = []
    source = requests.get('https://jobs.github.com/positions').text
    soup = BeautifulSoup(source, 'lxml')

    for pos in soup.find_all('strong', class_='fulltime'):
        time = pos.text
        ft.append(time)
    return (ft)
    


#returns list of the skills found (as part of the preset skill list) and creates a list for those skills found
def getSkills(link):
    #can add more keywords
    skills = ['python', 'java', 'C++', 'SQL', 'manage', 'javascript', 'linux', 'team', 'problem solving', 'front end', 'back end']
    foundSkillsList = []
    
    url = link
    src = requests.get(url).text
    soup = BeautifulSoup(src, 'lxml')

    summary = soup.find('div', class_='column main')
    #print (summary)
    sumtext = summary.text
    sumList = sumtext.split()
    #print ('====================================')

    for i in skills:
        if i in sumList:
            foundSkillsList.append(i)
            #print('found skill!!  ' + i)
            
    return foundSkillsList


#goes through multiple pages using getSkillS
def findallSkills():
    urls = []
    #30 just sample
    for i in range (1,30):
        url ='https://jobs.github.com/positions'
        finalurl = url + "?page=" + str(i)
        urls.append(finalurl)

    for x in urls:  #add print?
        getSkills(x)
        
# searches multiple pages and the given location
# also returns links
def getJobLLP(loc, numPages):
    multPageLocJobsWL = [] # will be populated with job dictionaries
    
    for i in range (0, numPages): # iterating over pages until numPages
        loc = loc.replace(' ', '+')
        url = 'https://jobs.github.com/positions' + '?page=' + str(i)
        #resolvedURL = url + "?page=" + str(i)
        finalURL = url + '&location='+ loc # including location in filters
        source = requests.get(finalURL).text
        soup = BeautifulSoup(source, 'lxml')
        
        for job in soup.find_all('tr', {'class':'job'} ): # iterating over individual job data
            #link = getLink(job.find('td', {'class':'title'}).find('h4').find('a')['href']) # get apply to link
            tmp = job.text.strip().split('\n')
            jb = {}
            for x in range (0, len(tmp)):
                y = tmp[x].strip()
                if len(y) > 1 and not "\t" in y:
                    if x == 0:
                        jb['Title'] = y
                    elif x == 1:
                        jb['Company'] = y
                    elif x == 2:
                        jb['Contract-Type'] = y
                    elif x == 3:
                        jb['Location'] = y
                    elif x == 4:
                        jb['Time-Posted'] = y
                    else:
                        jb['Other'] = y
                    
            jobMeta = getPageMeta (job.find('td', {'class':'title'}).find('h4').find('a')['href']) # gets job info (applyto link and skills)
            jb['Apply-To'] = jobMeta[0]
            jb['Skills'] = jobMeta[1]
            jb['Desc'] = jobMeta[2]
            
            multPageLocJobsWL.append(jb)
    return multPageLocJobsWL
        
#makes a dictionary of the return of the url loc,co,time,title,type,skills (some dictionaries do not have skills if job didnt have any of the keyword skills)
#runs on the first page only (no location specified) (doesnt go through multiple pages) url used ='https://jobs.github.com/positions'
#the try/excepts are there because some jobs do not have those fields specified in a normal way
def makeDict(x):
    Dict = {}
    companyList = company()
    locList = location()
    TitleList = positionNamesOnly()
    try:
        times = timeCreated()
    except:
        times=[]
    full = FullTime()
    links = onlylinks()
    try:
        skills = getSkills(links[x])
        #print (skills)
    except:
        pass
    #print (locList)
    try:
        Dict = dict({'Company': companyList[x], 'Location': locList[x], 'Title': TitleList[x], 'Time Created': times[x], 'Type': full[x]})
    except:
        pass

    try: #it is only adding first skill found, not sure why --->this might be messing it up actually some returns only give skills
        if (len(skills) > 0):
            Dict.update({'Skills': skills})
    except:
        pass

    return (Dict)



#going to be a list of dictionaries ***TBA
#for now prints out several dictionaries for each job post on the page (50)
def create(loc = 'chicago', numPages = 1):
    print (getJobLLP (loc, numPages))
    
    #source = requests.get('https://jobs.github.com/positions').text
    #soup = BeautifulSoup(source, 'lxml')
    
    #the length of the list of jobs
    #length = len(soup.find_all('tr', {'class':'job'} ))
    #for i in range (0, length):
    #for job in soup.find_all('tr', {'class':'job'} ):
        #source = requests.get('https://jobs.github.com/positions').text
        #soup = BeautifulSoup(source, 'lxml')
        #print (makeDict(job))
        
    
    
 


#for testing purposes
def testsummary():
    print('----------Positions------------')
    positionNamesOnly()
    print('----------Companies------------')
    company()
    print('----------Locations------------')
    location()
    print('----------Locations------------')
    onlylinks()
     



# In[19]:


# helper function for getJobWLnks
# assumes url is a job page on the github jobs api
# returns the link where the user can apply to the company
# or this page (as specified by url) if none provided
# do not use, redundant
def getLink(url):
    newSrc = requests.get(url).text
    newSoup = BeautifulSoup(newSrc, 'lxml')
    jobLink = newSoup.find('div', {'class':'highlighted'}).find('a')
    return url if jobLink == None else jobLink['href']


# returns apply to link and list of skills found on page
def getPageMeta(url):
    newSrc = requests.get(url).text
    newSoup = BeautifulSoup(newSrc, 'lxml')
    jobLink = newSoup.find('div', {'class':'highlighted'}).find('a')
    
    #can add more keywords
    skills = ['python', 'java', 'C++', 'SQL', 'manage', 'javascript', 'linux', 'team', 'problem solving', 'front end', 'back end']
    foundSkillsList = []
    
    #url = link
    #src = requests.get(url).text
    #soup = BeautifulSoup(src, 'lxml')

    summary = newSoup.find('div', class_='column main')
    #print (summary)
    sumtext = summary.text
    sumList = sumtext.split()
    #print ('====================================')

    for i in skills:
        if i in sumList:
            foundSkillsList.append(i)
            #print('found skill!!  ' + i)
    finalLink = url if jobLink == None else jobLink['href']
    
    desc = newSoup.find('div', class_='column main')
    
    return [finalLink, foundSkillsList, desc]


# In[24]:


create()


# In[ ]:




