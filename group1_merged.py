#!/usr/bin/env python
# coding: utf-8




#Capstone
#Group 1
import webbrowser
import requests
import flask
import sqlite3
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen




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

    def db(self):

        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        select_query = """select * from Users """
        cursor.execute(select_query)
        records = cursor.fetchall()
        return records

    def userCreate(self):
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        first=input('enter a name\n')
        token=input('enter a password \n')
        typ=input('enter a usertype \n')
        insert_query = """insert or ignore into Users (username,password,usertype) 
                                    VALUES (?,?,?)"""
            
        data_tuples = (first,token,typ)

        cursor.execute(insert_query, data_tuples)

        conn.commit()
        cursor.close()
        conn.close()
    
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
        
        if results==[]:
            print("YEE")
            if term not in records[i][0]:
                print("YeeT")
                results.append(records[i][0])
            if term.lower() in records[i][0]:
                print("Y")
                results.append(records[i][0])
            
            
        return results

    def locSearch(self,term):#find location of jobs
        'searches backend for whatever search term'
        results=[]
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        select_query = """select * from JOBS """        #change JOBS to whatever table you want to see
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        for i in range(len(records)):
            if term in records[i][0]:
                results.append(records[i][0])
                continue
            if term.lower() in records[i][0]:
                print("Y")
                results.append(records[i][0])
        #print(len(results))
        return results


    def searchUsers(self,term):#need to properly capitalize or there is double count bug
        'searches backend for whatever search term'
        results=[]
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        select_query = """select * from Users """        #change JOBS to whatever table you want to see
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        lCase=term.lower()
        for i in range(len(records)):
            if lCase in records[i][0]:#this is here to make sure that it picks up uppercase/lowercase problems
                results.append((records[i][0],records[i][2]))
                continue
            if term in records[i][0]:
                results.append(records[i])
        return results



    def findSeekers(self):#need to properly capitalize or there is double count bug
        'searches backend for whatever search term'
        results=[]
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        select_query = """select * from Users """        #change JOBS to whatever table you want to see
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        for i in range(len(records)):
            if "seeker" in records[i][2]:#this is here to make sure that it picks up uppercase/lowercase problems
                results.append(records[i])
            if "Seeker" in records[i][2]:#this is here to make sure that it picks up uppercase/lowercase problems
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
            

    # TODO
    #going to be a list of dictionaries ***TBA
    #for now prints out several dictionaries for each job post on the page (50)
    def create(self,loc,numPages):
        
        self.jobLst = self.getJobLLP (loc, numPages)
        self.testing()
        print("create done")
            
       

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
    def addCol(self):
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        addColumn = "ALTER TABLE Users ADD COLUMN Education text"
        cursor.execute(addColumn)
        conn.close()
        return 

    def gamePoints(self,user,points):
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        curr="SELECT * FROM Users WHERE username="+'@'+str(user)+'@'
        curr=curr.replace("@",'"')
        cursor.execute(curr)
        records = cursor.fetchall()
        points+=records[0][3]

        #update to users part
        state='UPDATE Users SET Points ='+"@"+str(points)+'@ '+'WHERE username='"@"+str(user)+"@" #only accepts it like this so far
        state=state.replace("@",'"')
        with conn:
            cursor.execute(state)
        conn.close()
        return 
        






