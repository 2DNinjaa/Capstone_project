#!/usr/bin/env python
# coding: utf-8

# In[79]:


#Capstone
#Group 1
import webbrowser
import requests
import flask
import sqlite3
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen


# In[20]:


class data:
    def __init__(self):
        print("MAKE SURE VM MESSAGES ARE DELETED")
        #create table if not exists Jobs (jobTitle text, passWord text, userType text)
        #info given by user
        self.location="none"
        self.jobType="no type"
        self.skills=[]
        self.exp="none"
        self.edu="none"

        self.cnt=1
        
        #info given by api
        self.age=[]#how old is the job listing
        self.jobLst=[]
        self.jobDist=[]
        self.jobLocation="none"
        self.company="none"
        self.listing=[]
        
         # keywords used in skill identification (ADDED SKILLS)
        self.keyWordSkills = ['python', 'java', 'c++', 'sql', 'manage', 'javascript', 'linux', 'team', 'problem solving', 'front end', 'back end', 'html', 'css','json', 'xml','api', 'linux', 'nodejs', 'c#', 'spark', 'sas', 'matlab', 'excel', 'spark', 'hadoop', 'azure', 'spss', 'git']


        #ADDED
        self.keyWordEdu = ['masters', 'bachelors', "master's", "bachelor's", 'phd', 'undergrad', 'graduate', 'undergraduate', 'ged', "graduate's", "undergraduate's", "associate's", 'doctoral']
                
    def __repr__(self):
        return self.exp
    
    # TODO: remove function?
    # sends the data allocated to the database
    def testing(self):
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()        
        # create table if not exists
        # columns used for the primary key implicitly cannot be null
        table_query = """create table if not exists JOBS
                            (location text, company text, datePosted text, postUrl text, 
                            jobType text, jobTitle text, jobDes text, jobApp text, 
                            PRIMARY KEY (company, jobTitle))"""
        cursor.execute(table_query)
        conn.commit()
        
        for i in range(len(self.jobLst)):
            insert_query = """insert or ignore into JOBS (location, company, datePosted, postUrl, 
                                                jobType, jobTitle, jobDes, jobApp) 
                                    VALUES (?,?,?,?,?,?,?,?)"""
            
            data_tuples = (self.jobLst[i]['Location'], self.jobLst[i]['Company'], 
                           self.jobLst[i]['Time-Posted'], self.jobLst[i]['Apply-To'], self.jobLst[i]['Contract-Type'], 
                           self.jobLst[i]['Title'], self.jobLst[i]['Desc'],"")

            cursor.execute(insert_query, data_tuples)

        conn.commit()
        cursor.close()
        conn.close()


    def searchJobs(self,term):
        'searches backend for whatever search term'
        results=[]
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        select_query = """select * from JOBS """        #change JOBS to whatever table you want to see
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        #term="Seeker"
        for i in range(len(records)):
            if term in records[i]:
                results.append(records[i])
        print(len(results))
        print("DDD")
        return results


    def searchUsers(self,term):
        'searches backend for whatever search term'
        results=[]
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        select_query = """select * from Users """        #change JOBS to whatever table you want to see
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        #term="Seeker"
        for i in range(len(records)):
            if term in records[i]:
                results.append(records[i])
        return results

    
        

    # returns tuple list of all records in jobs table sorted by the job title in ascending order
    def getAllJobs(self):
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        select_query = """select * from JOBS order by jobTitle ASC"""
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(row) for row in records]

    # returns tuple list of jobs starting from the offset and getting as many as amount
    # 0 based indexing means offset at 1 will start at second index
    def getNJobs(self, offset, amt):
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        select_query = """select * from Jobs order by jobTitle ASC"""
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [dict(row) for row in records[offset:offset+amt]]
    
    # deletes the jobs table entirely
    def destroyJobs(self):
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        table_query = 'DROP TABLE JOBS'
        cursor.execute(table_query)
        cursor.close()
        conn.close()
    
    def getOwnListing(self):
        return self.listing
    








###CAN CHANGE TO RUN LINKS THROUGH METHODS (have links as method parameters)

    #prints links of positions by location (city or state)
    def getLocationLinks(self,local):
        loc = local.replace(' ', '+')
        url = 'https://jobs.github.com/positions?utf8=%E2%9C%93&description=&location=' + loc
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')

        locationLinks = []
        for link in soup.find_all('a'):
            links = link.get('href')
            if "http" in links and '/positions/' in links:
                locationLinks.append(links)
        return locationLinks


    #returns list of links of positions without location specification 
    def onlylinks(self):
        linklist = []
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
    def linksMultPages(self,x):
        for i in range (1,x):
            url = 'https://jobs.github.com/positions'
            finalurl = url + "?page=" + str(i)
            source = requests.get(url).text
            soup = BeautifulSoup(source, 'lxml')
            
            for link in soup.find_all('a'):
                links = link.get('href')
                if "http" in links and '/positions/' in links:
                    print (links) # TODO: replace with return?


    #prints links for positions through page x in location loc
    #for this website there usually isnt multiple pages so this might not be necessary.
    def linksMultPagesLoc(self,x, loc):
        url = 'https://jobs.github.com/positions'
        loc = loc.replace(' ', '+')
        for i in range (1,x):
            finalurl = url + "?page=" + str(i) + loc
            source = requests.get(url).text # TODO: should this say finalurl not url?
            soup = BeautifulSoup(source, 'lxml')
            
            for link in soup.find_all('a'):
                links = link.get('href')
                if "http" in links and '/positions/' in links:
                    print (links) # TODO: replace with return?



    #prints out all job titles, locations, company, and fulltime or not full time
    def PositionList(self):
        source = requests.get('https://jobs.github.com/positions').text
        soup = BeautifulSoup(source, 'lxml')

        for pos in soup.find_all('table', class_='positionlist'):
            desc = pos.text
            print (desc) # TODO: replace with return?


    #returns list of the titles of all the positions on the page    
    def positionNamesOnly(self):
        pnames = []
        source = requests.get('https://jobs.github.com/positions').text
        soup = BeautifulSoup(source, 'lxml')

        for pos in soup.find_all('tr', class_='job'):
            name = pos.td.h4.text
            #print (name)
            pnames.append(name)
        return (pnames)


    #returns list of the company names 
    def company(self):
        cos = []
        source = requests.get('https://jobs.github.com/positions').text
        soup = BeautifulSoup(source, 'lxml')

        for co in soup.find_all('a', class_='company'):
            coname = co.text
            #print (coname)
            cos.append(coname)
            
        return (cos)


    #returns list of the locations
    def getLocation(self):
        locs = []
        source = requests.get('https://jobs.github.com/positions').text
        soup = BeautifulSoup(source, 'lxml')

        for pos in soup.find_all('span', class_='location'): #td, meta
            loc = pos.text
            #print (loc)
            locs.append(loc)
        return (locs)

    #returns list of the times created
    def timeCreated(self):
        tcr = []
        source = requests.get('https://jobs.github.com/positions').text
        soup = BeautifulSoup(source, 'lxml')

        for pos in soup.find_all('span', class_='when relatize relatized'):
            time = pos.text
            tcr.append(time)
        return (tcr)

    #returns list of full/parttime
    def FullTime(self):
        ft = []
        source = requests.get('https://jobs.github.com/positions').text
        soup = BeautifulSoup(source, 'lxml')

        for pos in soup.find_all('strong', class_='fulltime'):
            time = pos.text
            ft.append(time)
        return (ft)
        
    #returns list of the skills found (as part of the preset skill list) and creates a list for those skills found
    def getSkills(self,link):
        #can add more keywords
        #keyWordSkills = ['python', 'java', 'C++', 'SQL', 'manage', 'javascript', 'linux', 'team', 'problem solving', 'front end', 'back end']
        foundSkillsList = []
        
        url = link
        src = requests.get(url).text
        soup = BeautifulSoup(src, 'lxml')

        summary = soup.find('div', class_='column main')
        #print (summary)
        sumtext = summary.text
        sumList = sumtext.split()
        #print ('====================================')

        for i in self.keyWordSkills:
            if i in sumList:
                foundSkillsList.append(i)
                #print('found skill!!  ' + i)
                
        return foundSkillsList


    #goes through multiple pages using getSkillS
    def findallSkills(self):
        urls = []
        #30 just sample
        for i in range (1,30):
            url ='https://jobs.github.com/positions'
            finalurl = url + "?page=" + str(i)
            urls.append(finalurl)

        for x in urls:  #add print?
            getSkills(x)
            
    # searches multiple pages and the given location
    # returns list of all jobs found
    # also returns links and other info
    def getJobLLP(self,loc, numPages):
        
        lst=[]
        #r=requests.get("'https://jobs.github.com/positions?page=1")
        #p=r.json()
        
        multPageLocJobsWL = [] # will be populated with job dictionaries
        print("ENTERED GET_JOB_LLP")
        print('parameters: ', loc, ', ', numPages)
        for i in range (0, numPages): # iterating over pages until numPages
            loc = loc.replace(' ', '+')
            url = 'https://jobs.github.com/positions' + '?page=' + str(i)
            #resolvedURL = url + "?page=" + str(i)
            finalURL = url + '&location='+ loc # including location in filters
            
            source = requests.get(finalURL).text
            soup = BeautifulSoup(source, 'lxml')
            
            for job in soup.find_all('tr', {'class':'job'} ): # iterating over individual job data
                tmp = job.text.strip().split('\n')
                jb = {}
                for x in range (0, len(tmp)):
                    y = tmp[x].strip()
                    if len(y) > 1 and not "\t" in y:
                        if x == 0:
                            jb['Title'] = y
                        
                        elif x == 2:
                            jb['Company'] = y
                        
                        elif x == 4:
                            jb['Contract-Type'] = y
                        
                        elif x == 7:
                            jb['Location'] = y
                        
                        elif x == 8:
                            jb['Time-Posted'] = y
                        
                jobMeta = self.getPageMeta (job.find('td', {'class':'title'}).find('h4').find('a')['href']) # gets job info (applyto link and skills)
                jb['Apply-To'] = jobMeta[0]
                jb['Skills'] = jobMeta[1]
                jb['Desc'] = jobMeta[2]
                jb['Page-Addr'] = jobMeta[3]
                jb['Education'] = jobMeta[4]
                
                multPageLocJobsWL.append(jb)
            print("Page: "+str(i))
        return multPageLocJobsWL
            
    #makes a dictionary of the return of the url loc,co,time,title,type,skills (some dictionaries do not have skills if job didnt have any of the keyword skills)
    #runs on the first page only (no location specified) (doesnt go through multiple pages) url used ='https://jobs.github.com/positions'
    #the try/excepts are there because some jobs do not have those fields specified in a normal way
    def makeDict(self,x):
        Dict = {}
        companyList = company()
        locList = location()
        TitleList = positionNamesOnly()
        times = []
        try:
            times = timeCreated()
        except:
            pass
            
        full = FullTime()
        links = onlylinks()
        jobSkills = []
        
        try:
            jobSkills = getSkills(links[x])
            #print (jobSkills)
        except:
            pass
        
        #print (locList)
        
        try:
            Dict = dict({'Company': companyList[x], 'Location': locList[x], 'Title': TitleList[x], 'Time Created': times[x], 'Type': full[x]})
        except:
            pass

        try: #it is only adding first skill found, not sure why --->this might be messing it up actually some returns only give skills
            if (len(jobSkills) > 0):
                Dict.update({'Skills': jobSkills})
        except:
            pass

        return (Dict)


    # TODO
    #going to be a list of dictionaries ***TBA
    #for now prints out several dictionaries for each job post on the page (50)
    def create(self,loc,numPages):
        
        self.jobLst = self.getJobLLP (loc, numPages)
        self.testing()
        print("create done")
        #source = requests.get('https://jobs.github.com/positions').text
        #soup = BeautifulSoup(source, 'lxml')
        
        #the length of the list of jobs
        #length = len(soup.find_all('tr', {'class':'job'} ))
        #for i in range (0, length):
        #for job in soup.find_all('tr', {'class':'job'} ):
            #source = requests.get('https://jobs.github.com/positions').text
            #soup = BeautifulSoup(source, 'lxml')
            #print (makeDict(job))
            
       


    # helper function for getJobWLnks
    # assumes url is a job page on the github jobs api
    # returns the link where the user can apply to the company
    # or this page (as specified by url) if none provided
    # do not use, redundant
    def getLink(self,url):
        newSrc = requests.get(url).text
        newSoup = BeautifulSoup(newSrc, 'lxml')
        jobLink = newSoup.find('div', {'class':'highlighted'}).find('a')
        return url if jobLink == None else jobLink['href']


    # returns 4 pieces of the specified page
    #   [string:applyTo_link, list:skills, string:description, string:page_url]
    def getPageMeta(self, url):
        foundEduList=[]
        newSrc = requests.get(url).text
        newSoup = BeautifulSoup(newSrc, 'lxml')
        
        jobLink = ''
        try:
            jobLink = newSoup.find('div', {'class':'highlighted'}).find('a')['href']
        except:
            jobLink = url
        
        #can add more keywords
        #keywordSkills = ['python', 'java', 'C++', 'SQL', 'manage', 'javascript', 'linux', 'team', 'problem solving', 'front end', 'back end']
        foundSkillsList = []

        summary = newSoup.find('div', class_='column main')
        sumtext = summary.text#got rid of .text bc gave attribute error
        sumtext = sumtext.lower()
        sumList = sumtext.split()
        
        #ADDED
        for i in self.keyWordEdu:
            if i in sumList:
                foundEduList.append(i)
                
        for i in self.keyWordSkills:
            if i in sumList:
                foundSkillsList.append(i)
                #print('found skill!!  ' + i)
        
        desc = newSoup.find('div', class_='column main').text
        
        return [jobLink, foundSkillsList, desc, url, foundEduList]








