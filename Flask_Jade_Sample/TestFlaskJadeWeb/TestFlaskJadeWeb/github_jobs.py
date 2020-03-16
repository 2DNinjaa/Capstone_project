#!/usr/bin/env python
# coding: utf-8

# In[48]:


#Capstone
#Group 1
import webbrowser
import requests
import flask
import sqlite3
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen


# converts the given list to a string
def lst_to_str(lst):
    return ','.join(lst)

# converts the given string to a list
def str_to_lst(stri):
    return stri.split(',')

class data:
    def __init__(self):
        #create table if not exists Jobs (jobTitle text, passWord text, userType text)
        #info given by user
        self.location="none"
        self.jobType="no type"
        self.skills=[]
        self.exp="none"
        self.edu="none"
        
        #info given by api
        self.age=[]#how old is the job listing
        self.jobLst=[]
        self.jobDist=[]
        self.jobLocation="none"
        self.company="none"
        self.listing=[]
        
        # keywords used in skill identification
        self.keyWordSkills = ['python', 'java', 'c++', 'sql', 'manage', 'javascript', 'linux', 'team', 'problem solving', 'front end', 'back end', 'html', 'css','json', 'xml','api', 'linux', 'nodejs', 'c#', 'spark', 'sas', 'matlab', 'excel', 'spark', 'hadoop', 'azure', 'spss', 'git', 'aws']
        self.keyWordEdu = ['masters', 'bachelors', "master's", "bachelor's", 'phd', 'undergrad', 'graduate', 'undergraduate', 'ged', "graduate's", "undergraduate's", "associate's", 'doctoral']
        self.aiKeys = ['ai', 'a.i.', 'artificial intelligence', 'artificial']
        self.dlKeys= ['deep learning', 'neural networks', 'big data', 'deep', 'statistics']
        self.mlKeys = ['data mining', 'machine learning', 'cnn', 'rbm', 'machine', 'natural language', 'regression', 'fault diagnosis', 'intrusion detection']
        self.seKeys = ['software engineer', 'software development','code']
        
    def __repr__(self):
        return self.exp
    
    def creatUsersTable(self):
        conn = sqlite3.connect("Users.db")
        cursor = conn.cursor()
        table_query = """create table if not exists Users
                            (userName text, passWord text, userType text,
                            Points integer NOT NULL, email text, skills text, 
                            bio text, location text,
                            PRIMARY KEY (userName))"""
        cursor.execute(table_query)
        conn.commit()
        cursor.close()
        conn.close()

    def checkIfUserExist(self, user):
        conn = sqlite3.connect("Users.db")
        cursor = conn.cursor()
        
        select_query = 'select * from Users where userName = ?'
        cursor.execute(select_query, (user,))
        records = cursor.fetchall()
        
        return True if len(records) == 1 else False

    def gamePoints(self,user,points):
        conn = sqlite3.connect("Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        curr='SELECT * FROM Users WHERE username="'+str(user)+'"'
        cursor.execute(curr)
        records = cursor.fetchall()
        points = points + records[0]['Points']
        
        #print([dict(row) for row in records])
        
        #update to users part
        state='UPDATE Users SET Points ='+str(points)+' WHERE username="'+str(user)+'"'
        print(state)
        cursor.execute(state)
        conn.commit()
        
        cursor.close()
        conn.close()

    def getUserBookmarks(self, user):
        conn = sqlite3.connect("Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        select_query = 'SELECT * FROM Bookmarks WHERE User = "' + user + '" ORDER BY title ASC'
        cursor.execute(select_query)
        
        records = cursor.fetchall()
        
        conn.commit()
        cursor.close()
        conn.close()
        return [dict(row) for row in records]

    # inserts into the bookmarks table a new row with the following information
    # user for retrieval, and the following three items because they're the primary key in the jobs table
    def updateBookmarks(self, user, title, comp, loc):
        conn = sqlite3.connect("Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        update_query = 'INSERT OR IGNORE INTO Bookmarks (User, title, company, location) VALUES (?, ?, ?, ?)'
        cursor.execute(update_query, (user, title, comp, loc,))
        
        conn.commit()
        cursor.close()
        conn.close()

    def updateColumn(self, user, col, val):
        conn = sqlite3.connect("Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        update_query = 'UPDATE Users SET ' + col + ' = "' + val + '" WHERE username = "' + user + '"'
        cursor.execute(update_query)
        conn.commit()
        
        cursor.close()
        conn.close()

    # sends the data allocated to the database
    def testing(self, allJobs):
        conn = sqlite3.connect("Users.db")
        cursor = conn.cursor()
        
        # create table if not exists
        # columns used for the primary key implicitly cannot be null
        # columns skills and education are comma separated string representations of lists
        table_query = """create table if not exists JOBS
                            (location text, company text, datePosted text, postUrl text, 
                            jobType text, jobTitle text, jobDes text, jobApp text, salary text,
                            skills text, category text, education text,
                            PRIMARY KEY (company, jobTitle, location))"""
        cursor.execute(table_query)
        conn.commit()
        
        for i in range(len(allJobs)):
            insert_query = """insert or ignore into JOBS (location, company, datePosted, postUrl, 
                                                jobType, jobTitle, jobDes, jobApp, salary, skills,
                                                category, education) 
                                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
            
            #print(self.jobLst[i]['Skills'])
            data_tuples = (allJobs[i]['Location'], 
                           allJobs[i]['Company'], 
                           allJobs[i]['Time-Posted'], 
                           allJobs[i]['Page-Addr'], 
                           allJobs[i]['Contract-Type'], 
                           allJobs[i]['Title'], 
                           allJobs[i]['Desc'], 
                           allJobs[i]['Apply-To'], 
                           allJobs[i]['Salary'],
                           lst_to_str(allJobs[i]['Skills']), 
                           allJobs[i]['Category'], 
                           lst_to_str(allJobs[i]['Education']))

            cursor.execute(insert_query, data_tuples)

        conn.commit()
        cursor.close()
        conn.close()

    # returns tuple list of all records in jobs table sorted by the job title in ascending order
    def getAllJobs(self):
        conn = sqlite3.connect("Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        select_query = """select * from JOBS order by jobTitle ASC"""
        cursor.execute(select_query)
        records = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return [dict(row) for row in records]

    def getNUserBookmarks(self, user, offset, amt):
        conn = sqlite3.connect("Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        select_query = 'SELECT * FROM Bookmarks WHERE User = "' + user + '" ORDER BY title ASC'
        cursor.execute(select_query)
        
        records = cursor.fetchall()
        
        conn.commit()
        cursor.close()
        conn.close()

        return [[records.index(row), data().getJobByKey(dict(row)['title'], dict(row)['company'], dict(row)['location']), 'Jobs'] for row in records[offset:offset+amt]]

    def getJobByKey(self, title, com, loc):
        conn = sqlite3.connect("Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        select_query = """SELECT * FROM Jobs 
                            WHERE jobTitle = ? and company = ? and location = ?"""
        cursor.execute (select_query, (title, com, loc,))
        
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [dict(row) for row in records][0]

    # returns tuple list of jobs starting from the offset and getting as many as amount
    # 0 based indexing means offset at 1 will start at second index
    def getNJobs(self, offset, amt):
        conn = sqlite3.connect("Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        select_query = """select * from Jobs order by jobTitle ASC"""
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        
        #print('-- LENGTH: ' + str(len(records)))
        return [[records.index(row), dict(row), 'Jobs'] for row in records[offset:offset+amt]]

    # modification of getNJobs
    # similar design but will search the specified column (col) for the search term (term)
    # return is the same
    # col MUST BE a column header
    def getNJobsByQuery (self, term, col, offset, amt):
        conn = sqlite3.connect("Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if col[1] == 'None' and col[2] == 'None':
            select_query = 'select * from Jobs where '+ col+ ' like ? order by jobTitle ASC'
            cursor.execute(select_query, ('%'+term+'%',)) # pattern matching
        
        elif not col[1] == 'None' and col[2] == 'None':
            select_query = 'select * from Jobs where '+ col[0] + ' like ? and ' + col[1] + ' like ? ' + ' order by jobTitle ASC'
            cursor.execute(select_query, ('%'+term[0]+'%', '%'+term[1]+'%')) # pattern matching
        
        elif not col[1] == 'None' and not col[2] == 'None':
            select_query = 'select * from Jobs where '+ col[0] + ' like ? and ' + col[1] + ' like ? and ' + col[2] + ' like ? ' + ' order by jobTitle ASC'
            cursor.execute(select_query, ('%'+term[0]+'%', '%'+term[1]+'%', '%'+term[2]+'%',)) # pattern matching
        
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [[records.index(row), dict(row)] for row in records[offset:offset+amt]]

    # would be used by quicksearch, searches multiple columns at once
    def getNJobsByQueryQuickly (self, term, offset, amt):
        conn = sqlite3.connect("Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        select_query = 'select * from Jobs where jobTitle, company, location, skills, jobType like ? order by jobTitle ASC'
        cursor.execute(select_query, ('%'+term+'%',)) # pattern matching
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [[records.index(row), dict(row)] for row in records[offset:offset+amt]]

    # returns a single job as a dictionary based on its index when sorting by title
    def getNthJob(self, n):
        conn = sqlite3.connect("Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        select_query = """select * from Jobs order by jobTitle ASC"""
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [dict(row) for row in records][int(n)]

    def getNthUser(self, n):
        conn = sqlite3.connect("Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        select_query = """select * from Users order by userName ASC"""
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [dict(row) for row in records][int(n)]

    def getNUsers(self, offset, amt):
        conn = sqlite3.connect("Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        select_query = """select * from Users order by userName ASC"""
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        conn.close()

        return [[records.index(row), dict(row), 'Users'] for row in records[offset:offset+amt]]

    def getNUsersByQuery (self, term, col, offset, amt):
        conn = sqlite3.connect("Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        select_query = 'select * from Users where '+ col+ ' like ? order by userName ASC'
        cursor.execute(select_query, ('%'+term+'%',)) # pattern matching
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        
        #print('-- LENGTH Q: ' + str(len(records)))
        return [[records.index(row), dict(row), 'Users'] for row in records[offset:offset+amt]]

    def getUserByName(self, name):
        conn = sqlite3.connect("Users.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        select_query = 'select * from Users where userName = ?'
        cursor.execute(select_query, (name,))
        records = cursor.fetchall()
        if len(records) == 1:
            return [dict(row) for row in records][0]
        else:
            print('-- ERROR: COULD NOT FIND USER: ' + name + ' --')
            return None

    # deletes the jobs table entirely
    def destroyJobs(self):
        conn = sqlite3.connect("Users.db")
        cursor = conn.cursor()
        table_query = 'DROP TABLE JOBS'
        cursor.execute(table_query)
        cursor.close()
        conn.close()

###CAN CHANGE TO RUN LINKS THROUGH METHODS (have links as method parameters)

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
            
    # searches multiple pages and the given location
    # returns list of all jobs found
    # also returns links and other info
    def hubJobs(self, jobX, loc, numPages):
        print('entering github jobs')
        multPageLocJobsWL = [] # will be populated with job dictionaries
        for i in range (0, numPages): # iterating over pages until numPages
            loc = '' if loc == '' else ('&location=' + loc.replace(' ', '+'))
            jobX = '' if jobX == '' else ('&description=' + jobX.replace(' ', '+'))
            finalURL = 'https://jobs.github.com/positions?utf8=✓' + loc + '&page=' + str(i) + jobX
            print(finalURL)
            #finalURL = url + loc # including location in filters
            
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
                        
                jb['Salary'] = 'N/A' # salary not listed on github
                jobMeta = self.getPageMeta (job.find('td', {'class':'title'}).find('h4').find('a')['href']) # gets job info (applyto link and skills)
                jb['Apply-To'] = jobMeta[0]
                jb['Skills'] = jobMeta[1]
                jb['Desc'] = jobMeta[2]
                jb['Page-Addr'] = jobMeta[3]
                jb['Education'] = jobMeta[4]
                jb['Category'] = jobMeta[5]
                
                multPageLocJobsWL.append(jb)
                
        print('github jobs length ', len(multPageLocJobsWL))
        return multPageLocJobsWL

    # TODO
    #going to be a list of dictionaries ***TBA
    #for now prints out several dictionaries for each job post on the page (50)
    def create(self, job = '', loc = '', numPages = 1):
        return self.testing(self.hubJobs (job, loc, numPages) + self.indeedJobs(job, loc, numPages))
        #print("create done")

    # returns 4 pieces of the specified page
    #   [string:applyTo_link, list:skills, string:description, string:page_url, list:education]
    def getPageMeta(self, url):
        newSrc = requests.get(url).text
        newSoup = BeautifulSoup(newSrc, 'lxml')
        
        # apply-to link
        jobLink = ''
        try:
            jobLink = newSoup.find('div', {'class':'highlighted'}).find('a')['href']
        except:
            jobLink = url
        
        foundSkillsList = []
        foundEduList = []

        # parsing summary
        summary = newSoup.find('div', class_=['column main', 'jobsearch-jobDescriptionText'])
        sumtext = summary.text if not summary == None else 'N/A'
        sumtext1 = sumtext.lower()
        sumList = sumtext1.split()
        
        # education
        for i in self.keyWordEdu:
            if i in sumList and not i in foundEduList:
                foundEduList.append(i)
                
        # skills
        for i in self.keyWordSkills:
            if i in sumList and not i in foundSkillsList:
                foundSkillsList.append(i)
        
        # primitive text classification
        # sums up occurunces of keywords and then appends the category tag associated with the highest count
        cat = ''
        aiCNT = 0
        dlCNT = 0
        mlCNT = 0
        seCNT = 0
        otherCNT = 0
        for x in sumList:
            if x in self.aiKeys:
                aiCNT += 1
                continue
            elif x in self.dlKeys:
                dlCNT += 1
                continue
            elif x in self.mlKeys:
                mlCNT += 1
                continue
            elif x in self.seKeys:
                seCNT += 1
                continue
                
        mx = max(aiCNT, dlCNT, mlCNT, seCNT, otherCNT)
        if aiCNT == mx:
            cat = 'Artificial Intelligence'
        elif dlCNT == mx:
            cat = 'Deep Learning'
        elif mlCNT == mx:
            cat = 'Machine Learning'
        elif seCNT == mx:
            cat = 'Software Engineer'
        elif otherCNT == mx: # consider difference of counts?
            cat = 'Other'
        
        return [jobLink, foundSkillsList, sumtext, url, foundEduList, cat]

    ### Indeed ###
    
    # gets a list of dictionaries limited by the input parameters through indeed
    def indeedJobs(self, job, location, maxPages):
        print('entering indeed jobs')
        baseLink = 'https://www.indeed.com/q-computer-science-jobs'
        webAddr = baseLink + ('' if job == '' else '?q=' + job.replace (' ', '+'))
        webAddr = webAddr + ('' if location == '' else '&l=' + location) + '&start=0'

        jbPages = []
        for x in range(0, maxPages):
            link=webAddr.replace(webAddr[-1], str(x))
            #jbPages.append(self.getDictNew(link))
            source = requests.get(link).text
            soup = BeautifulSoup(source, 'lxml')
            print(link)

            for div in soup.find_all ('div', class_='row', attrs={'class':'row'}):
                linkElem = div.find('div', class_='title').a
                title = linkElem.get('title') # TITLE
                link = "https://www.indeed.com" + linkElem.get('href')   # LINK

                payRAW = div.find(name='span', class_=['salaryText', 'sjcl', 'salary'])
                pay = payRAW.text.replace('\n', '') if not payRAW == None else 'N/A' # salary

                co = div.find(name='span', class_=['company', 'result-link-source']).text.strip() # company
                loc = div.find(['div', 'span'], attrs={'class': 'location'}).text # location
                date = div.find('span', attrs={'class': 'date'}).text # date

                jobMeta = self.getPageMeta(link)
                newDict = {
                    'Company':co, 'Location':loc, 'Title':title, 
                    'Time-Posted':date, 'Salary':pay, 'Link':link,
                    'Contract-Type':'N/A'
                }
                newDict['Apply-To'] = jobMeta[0]
                newDict['Skills'] = jobMeta[1]
                newDict['Desc'] = jobMeta[2]
                newDict['Page-Addr'] = jobMeta[3]
                newDict['Education'] = jobMeta[4]
                newDict['Category'] = jobMeta[5]

                jbPages.append(newDict)
        
        print('indeed jobs length ', len(jbPages))
        return jbPages
    
    # TODO: delete this
    def getDictNew(self, url):
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')

        tmpLst = []
        for div in soup.find_all ('div', class_='row', attrs={'class':'row'}):
            linkElem = div.find('div', class_='title').a
            title = linkElem.get('title') # TITLE
            link = "https://www.indeed.com" + linkElem.get('href')   # LINK

            payRAW = div.find(name='span', class_=['salaryText', 'sjcl', 'salary'])
            pay = payRAW.text.replace('\n', '') if not payRAW == None else 'N/A' # salary

            co = div.find(name='span', class_=['company', 'result-link-source']).text.strip() # company
            loc = div.find(['div', 'span'], attrs={'class': 'location'}).text # location
            date = div.find('span', attrs={'class': 'date'}).text # date
            
            jobMeta = self.getPageMeta(link)
            newDict = {
                'Company':co, 'Location':loc, 'Title':title, 'Time-Posted':date, 'Salary':pay, 'Link':link
            }
            newDict['Apply-To'] = jobMeta[0]
            newDict['Skills'] = jobMeta[1]
            newDict['Desc'] = jobMeta[2]
            newDict['Page-Addr'] = jobMeta[3]
            newDict['Education'] = jobMeta[4]
            
            tmpLst.append(newDict)
        return tmpLst


