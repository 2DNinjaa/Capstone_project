#Capstone
#Group 1
import webbrowser
import requests
import flask
import sqlite3
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
        

    def __repr__(self):
        return self.exp


    def db(self):

        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        select_query = """select * from USERS """
        cursor.execute(select_query)
        records = cursor.fetchall()
        return records

    def userSender(self):#send user info to database
                
        'send data to database'
        name="Bob the builder"
        password="can we do it?"
        user="Both"

        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        insert_query= "INSERT INTO USERS(UserName, Password,UserType) VALUES(?,?,?)"
        cursor.execute(insert_query,(name,password,user))
        conn.commit()
        cursor.close()
        return


    def jobSender(self,jobLocation,company,time,url,jobType,jobTitle,jobDes,app):#send job info to database
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        insert_query = "create table if not exists Jobs (jobLocation text,company text,datePosted text,postUrl text,jobType text,jobTitle text, jobDes text, jobApp text) VALUES(?,?,?,?,?,?,?,?,?)"
        cursor.execute(insert_query,(jobLocation,company,time,url,jobType,jobTitle,jobDes,app))
        conn.commit()
        cursor.close()
        
        return
        

    
    
    def dummy(self):#dummy function to simulate the front end
        #might need to add more variables if i missed any user ones
        info=["Chicago","Software developerr",["Pyton","Java","C"],"3 years","Masters"]
        return self.userInfo(info)        
    
    def userInfo(self,info):#sets global variables to be fed for the front end
        "user info should be sent back in a standardized list"  
        self.location=info[0]
        self.jobType=info[1]
        self.skills=info[2]
        self.exp=info[3]
        self.edu=info[4]
        print(self.edu)
        #return sender
    
    def allocation(self):
    
        #x=webbrowser.open('https://jobs.github.com/positions.json?description=python&location=new+york')
        r=requests.get('https://jobs.github.com/positions.json?description=python&location=new+york')
        p=r.json()
        company=p[0]['company'][:]#simulating so change to proper keys later
        jobLocation=p[0]['location'][:]
        time=p[0]["created_at"]
        url=p[0]["url"]
        jobType=p[0]["type"]
        jobTitle=p[0]["title"]
        jobDes=p[0]["description"]
        app=p[0]["how_to_apply"]

        
        self.listing.append(self.company)
        self.listing.append(self.jobLocation)
        self.listing.append(time)
        self.listing.append(url)
        self.listing.append(jobType)
        self.listing.append(jobTitle)
        self.listing.append(jobDes)
        self.listing.append(app)
        #jobSender
        return self.testing(jobLocation,company,time,url,jobType,jobTitle,jobDes,app)


    def jerb(self):
        return self.listing



    def testing(self,jobLocation,company,time,url,jobType,jobTitle,jobDes,app):
        print("I")
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        print("I")
        cursor = conn.cursor()
        table_query = """create table if not exists JOBS
                            (location text, company text, datePosted text, postUrl text, 
                            jobType text, jobTitle text, jobDes text, jobApp text)"""
        cursor.execute(table_query)
        conn.commit()
        
        insert_query = """insert into JOBS (location, company, datePosted, postUrl, 
                                            jobType, jobTitle, jobDes, jobApp) 
                                VALUES (?,?,?,?,?,?,?,?)"""
        data_tuples = (jobLocation,company, datePosted, postUrl, jobType, jobTitle, jobDes, jobApp)
        cursor.execute(insert_query, data_tuples)
        conn.commit()
        
        

    
