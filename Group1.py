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

        self.cnt=1
        

        #info given by api
        self.age=[]#how old is the job listing
        self.jobLst=[]
        self.jobDist=[]
        self.jobLocation="none"
        self.company="none"
        self.listing=[]
        

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
    
    def allocation(self,link):#gather job info 
    
        r=requests.get(link)
        p=r.json()
        temp=[]
        if p==[]:
            return self.listing
        for i in range(len(p)):
            company=p[i]['company'][:]
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



    def testing(self):#sends the data allocated to the database
        
        self.allocation("https://jobs.github.com/positions.json?page=1")
        
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        print("I")
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
            data_tuples = (self.listing[i][1],self.listing[i][0], self.listing[i][4],"", self.listing[i][2], self.listing[i][3], "", "")
            cursor.execute(insert_query, data_tuples)
            conn.commit()
        

    def tables(self):
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        select_query = """select * from Jobs """
        cursor.execute(select_query)
        records = cursor.fetchall()
        return records
        
