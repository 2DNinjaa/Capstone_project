#!/usr/bin/env python
# coding: utf-8

# In[124]:


import requests
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen


# In[131]:


allJobs = [] # list of dictionary for all jobs

# skills and categories
skills = ['python', 'java', 'c++', 'sql', 'manage', 'javascript', 
          'linux', 'team', 'problem solving', 'front end', 'back end', 
          'html', 'css','json', 'xml','api', 'linux', 'nodejs', 'c#', 
          'spark', 'sas', 'matlab', 'excel', 'spark', 'hadoop', 'azure', 
          'spss', 'git', 'aws']

aiKeys = ['ai', 'a.i.', 'artificial intelligence', 'artificial']

dlKeys= ['deep learning', 'neural networks', 'big data', 'deep', 'statistics']

mlKeys = ['data mining', 'machine learning', 'cnn', 'rbm', 
          'machine', 'natural language', 'regression', 'fault diagnosis', 'intrusion detection']

seKeys = ['software engineer', 'software development','code']

keyWordEdu = ['masters', 'bachelors', "master's", "bachelor's", 'phd', 'undergrad', 'graduate', 'undergraduate', 'ged', "graduate's", "undergraduate's", "associate's", 'doctoral']



# In[132]:


def getSomeDict(job, location, maxPages):
    baseLink = 'https://www.indeed.com/'
    webAddr = baseLink + 'jobs?q=' + job.replace (' ', '+')
    webAddr = webAddr + ('' if location == '' else '&l=' + location) + '&start=0'
    
    for x in range(0, maxPages):
        link=webAddr.replace(webAddr[-1], str(x))
        #print(link)
        getDict(link)


# In[133]:


def getDict(url):
    dicList = []
    coList = []
    titList = []
    locList = []
    dateList =[]
    payList = []
    linkList = []
    skillList = []
    descList = []
    catList = []
    
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    #titles and links
    for pos in soup.find_all('div', class_='title'):
        titList.append(pos.a.get('title'))
        link = pos.a.get('href')
        linkList.append("https://www.indeed.com" + link)

    # company
    # 'result-link-source' may not be needed? 
    for span in soup.find_all(name='span', class_=['company', 'result-link-source']):
        coList.append(span.text.strip())
    
    
    # pay
    for div in soup.find_all(name='div', attrs={'class':'row'}):
        try:
            payList.append(div.find(name='span', class_=['salaryText', 'sjcl']).text.replace('\n', ''))
        except:
            payList.append('N/A')
        
        
    #locations
    spans = soup.findAll(['div', 'span'], attrs={'class': 'location'})
    for span in spans:
        locList.append(span.text)


    #dates
    spans = soup.findAll('span', attrs={'class': 'date'})
    for span in spans:
        dateList.append(span.text)
        

    #go into job links
    for l in linkList:

        #description
        newSRC = requests.get(l).text
        newSoup = BeautifulSoup(newSRC, 'lxml')
        desc = newSoup.find('div', class_='jobsearch-jobDescriptionText')
        desc = desc.text
        descList.append(desc)
    
        foundSkills = []
        desc = desc.lower()
        for x in skills:
            if x in desc and x not in foundSkills:
                foundSkills.append(x)
        skillList.append(foundSkills)
        
        # primitive text classification
        # sums up occurunces of keywords and then appends the category tag associated with the highest count
        aiCNT = 0
        dlCNT = 0
        mlCNT = 0
        seCNT = 0
        otherCNT = 0
        for x in desc.split():
            if x in aiKeys:
                aiCNT += 1
                continue
            elif x in dlKeys:
                dlCNT += 1
                continue
            elif x in mlKeys:
                mlCNT += 1
                continue
            elif x in seKeys:
                seCNT += 1
                continue
            # need to improve other because it might always be listed as other
            #otherCNT += 1 # if no other count was incremented increment other

        mx = max(aiCNT, dlCNT, mlCNT, seCNT, otherCNT)
        if aiCNT == mx:
            catList.append('Artificial Intelligence')
        elif dlCNT == mx:
            catList.append('Deep Learning')
        elif mlCNT == mx:
            catList.append('Machine Learning')
        elif seCNT == mx:
            catList.append('Software Engineer')
        elif otherCNT == mx: # consider difference of counts?
            catList.append('Other')
                    
                #Education
        foundEdu = []
        desc = desc.lower()
        for x in desc.split():
            if x in keyWordEdu:
                foundEdu.append(x)
        eduList.append(foundEdu)
            
    
    for i in range (0, len(titList)):
        allJobs.append(dict({'Company':coList[i], 'Location': locList[i], 
                             'Title': titList[i], 'Date Created': dateList[i], 
                             'Salary': payList[i], 'Link':linkList[i],'Skills': skillList[i], 
                             'Description': descList[i], 'Category': catList[i], 'Education': eduList[i]}))


# In[136]:


getSomeDict('data scientist', 'Chicago', 6)


# In[ ]:




