

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
        self.lst={}
        
        # keywords used in skill identification
        self.keyWordSkills = ['python', 'java', 'C++', 'SQL', 'manage', 'javascript', 'linux', 'team', 'problem solving', 'front end', 'back end']
        
    def __repr__(self):
        return self.exp

    #Function to just view the users table
    def db(self):
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        select_query = """select * from JOBS """
        cursor.execute(select_query)
        records = cursor.fetchall()
        return records

    # sets global variables to be fed for the front end
    # user info should be sent back in a standardized list
    def userInfo(self,info):
        self.location=info[0]
        self.jobType=info[1]
        self.skills=info[2]
        self.exp=info[3]
        self.edu=info[4]
        print(self.edu)
        #return sender # TODO: build list?
    
    # gather job info
    def allocation(self,link):
        'gathers basic info about jobs from github'
        r=requests.get(link)
        p=r.json()
        temp=[]
        if p==[]:
            return self.listing
        
        for i in range(len(p)):
            company=p[i]['company'][:] # TODO: remove [:] ? 
            jobLocation=p[i]['location'][:]
            jobType=p[i]["type"]
            jobTitle=p[i]["title"]
            time=p[i]["created_at"][4:11]+p[i]["created_at"][24:28]
            temp.append(company)
            temp.append(jobLocation)
            temp.append(jobType)
            temp.append(jobTitle)
            temp.append(time)
            
        if self.cnt>=10 and self.cnt<100:
            self.cnt+=1
            self.listing.append(temp)
            link=link.replace(link[-2:],cnt)
            return self.allocation(link)
        else:
            print("entered into else" +str(self.cnt))
            self.cnt+=1
            self.listing.append(temp)
            link=link.replace(link[-1],str(self.cnt))
            return self.allocation(link)   
        #return self.testing(jobLocation,company,time,url,jobType,jobTitle,jobDes,app)

    # TODO: remove function?
    # sends the data allocated to the database
    def testing(self):
        q=1 # TODO: remove vars q, w, e, r, t?
        w=0
        e=4
        r=2
        t=3
        return "hi"
        self.allocation("https://jobs.github.com/positions.json?page=1") # TODO: parameterize?
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        table_query = """create table if not exists JOBS
                            (location text, company text, datePosted text, postUrl text, 
                            jobType text, jobTitle text, jobDes text, jobApp text)"""
        cursor.execute(table_query)
        conn.commit()
        
        for i in range(len(self.listing)):
            insert_query = """insert into JOBS (location, company, datePosted, postUrl, 
                                                jobType, jobTitle, jobDes, jobApp) 
                                    VALUES (?,?,?,?,?,?,?,?)"""
            data_tuples = (self.listing[i][q],self.listing[i][w], self.listing[i][e],"", self.listing[i][r], self.listing[i][t], "", "")
            q+=5 # TODO: see previous todo
            w+=5
            e+=5
            r+=5
            t+=5
            cursor.execute(insert_query, data_tuples)
            
        #print("DONE")
        conn.commit()

    # TODO: remove?
    def updateJobsTable(self):
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        #print("I")
        cursor = conn.cursor()
        addColumn = "ALTER TABLE JOBS ADD COLUMN link text"
        addColumn = "ALTER TABLE JOBS ADD COLUMN IDNUM int"

    def getAllJobs(self):
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        select_query = """select * from Jobs"""
        cursor.execute(select_query)
        records = cursor.fetchall()
        return records

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
    # also returns links
    def getJobLLP(self,loc, numPages):
        multPageLocJobsWL = [] # will be populated with job dictionaries
        print("III")
        for i in range (0, numPages): # iterating over pages until numPages
            loc = loc.replace(' ', '+')
            url = 'https://jobs.github.com/positions' + '?page=' + str(i)
            #resolvedURL = url + "?page=" + str(i)
            finalURL = url + '&location='+ loc # including location in filters

            #r=requests.get(finalURL)
            #p=r.json()
            
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
    def create(self,loc = 'chicago', numPages = 1):
        
        self.listing=self.getJobLLP (loc, numPages)
        self.testing()
        print("done")
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


    # returns apply to link and list of skills found on page
    def getPageMeta(self,url):
        newSrc = requests.get(url).text
        newSoup = BeautifulSoup(newSrc, 'lxml')
        jobLink = newSoup.find('div', {'class':'highlighted'}).find('a')
        
        #can add more keywords
        #keywordSkills = ['python', 'java', 'C++', 'SQL', 'manage', 'javascript', 'linux', 'team', 'problem solving', 'front end', 'back end']
        foundSkillsList = []
        
        #url = link
        #src = requests.get(url).text
        #soup = BeautifulSoup(src, 'lxml')

        summary = newSoup.find('div', class_='column main')
        #print (summary)
        sumtext = summary.text
        sumList = sumtext.split()
        #print ('====================================')

        for i in self.keyWordSkills:
            if i in sumList:
                foundSkillsList.append(i)
                #print('found skill!!  ' + i)
        finalLink = url if jobLink == None else jobLink['href']
        
        desc = newSoup.find('div', class_='column main')
        
        return [finalLink, foundSkillsList, desc]


# In[ ]:




