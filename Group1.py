#Capstone
#Group 1
import webbrowser
import requests

class data:

    def __init__(self):

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
        

    def __repr__(self):
        return self.exp

    
    
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
        
    def sender(self):
        'send data to front end'
        return

    
    def allocation(self):
    
        #x=webbrowser.open('https://jobs.github.com/positions.json?description=python&location=new+york')
        r=requests.get('https://jobs.github.com/positions.json?description=python&location=new+york')
        p=r.json()
        self.company=p[0]['company'][8:]#simulating so change to proper keys later
        print(self.company)
        return p[0]['company'].keys

    
