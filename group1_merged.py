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

    #Function to just view the users table
    def db(self):
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        select_query = """select * from JOBS """        #change JOBS to whatever table you want to see
        cursor.execute(select_query)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        #print(len(records))
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
    # TODO: remove?
    def allocation(self,link):
        'gathers basic info about jobs from github'
        r=requests.get(link)
        p=r.json()
        return p
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
            self.jobLst.append(temp)
            link=link.replace(link[-2:],cnt)
            return self.allocation(link)
        else:
            print("entered into else" +str(self.cnt))
            self.cnt+=1
            self.jobLst.append(temp)
            link=link.replace(link[-1],str(self.cnt))
            return self.allocation(link)   

    # TODO: remove function?
    # sends the data allocated to the database
    def testing(self):
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()



        entry=[{'Title': 'Experienced JavaScript Front End Developer',
  'Company': 'Combinaut',
  'Contract-Type': 'Full Time',
  'Location': 'Chicago',
  'Time-Posted': '17 days ago',
  'Apply-To': 'mailto:alex@combinaut.com',
  'Skills': ['team'],
  'Desc': '\nCombinaut is seeking an experienced JavaScript Front End Developer.\nCombinaut has an immediate need for a developer who has a minimum of  5 years’ professional experience working in JavaScript as a front end developer. We are looking for someone who will be able to work with near autonomy toward agreed goals, with the occasional need for material direction or implementation changes. Ideal candidates will have experience following established patterns and approaches within existing code bases with ease. We are looking for candidates experienced with Backbone.js, Git, and who have a strong understanding of system design. Preference will be given to candidates with Ruby on Rails experience.\nOur ideal candidate has a team-first mindset, collaborating with our internal and client-side stakeholders to solve problems, design new features, and deliver solid technical solutions.\nCombinaut - What we Make\nCombinaut creates tools for healthcare providers to help patients find care. It is important work, and we believe in what we do. We are seeking a full-time Chicago-based staff developer to join our Chicago and remote team.\nWorking With Combinaut\nWe are a very lean crew, with six developers and a handful of support positions. Our developers must work well both independently and collaboratively, each team member is responsible for building and maintaining our end-to-end software stack. We’re a self-organizing team that moves quickly together and contributes across the stack as needed (regardless of specialized knowledge or experience). Every team member is expected to be able to communicate with clarity and professionalism with internal team members as well as with clients.\nCombinaut believes diversity and inclusion make the workplace better and our product stronger. Every applicant for this position will be considered.\n'},
 {'Title': 'Sr. Java J2EE Developer',
  'Company': 'Peterson Technology Partners',
  'Contract-Type': 'Contract',
  'Location': 'Chicago, IL',
  'Time-Posted': '26 days ago',
  'Apply-To': 'http://bit.ly/ptp-srjava-so',
  'Skills': ['SQL', 'manage', 'javascript', 'team'],
  'Desc': "\nBecome a Senior Java Developer with Peterson Technology Partners today!\nApply at:\n\nSummary:\nThis key position will be the primary Java Developer supporting Master Data Management software (MDM a.k.a GEM). This software is the key component of our customer solutions (CRM). GEM provides a comprehensive view of the Guest profile and preference information to interfacing systems like RESERVE, Gold Passport, etc.\nThis position reports directly to the Director of Customer Data Management\nRequirements:\n\nKnowledge of Service-Oriented Architectures\nKnowledge of Web-based Architectures\nKnowledge of database design and file management techniques\nTechnically fluent in the Java programming language\nHands-on experience with Java Spring MVC, spring boot and SOAP services\nExperience with app servers, JBOSS, DOCKER desired\nProduction support experience is desired\nExperience using javascript is plus\n\nResponsibilities:\n\nSupport Envision Opera Interface and Guest Customer Service applications.\nWork with offsite contract developers to manage the development of new reports and also assist in supporting existing reports and cubes.\nSupport for application maintenance or other system related maintenance events on an on-call basis.\nDevelop applications leveraging J2EE and Web technologies from start to finish on their own. This includes but is not limited to; customer interaction, validating requirements, system design, full-stack development using standard APIs.\nDevelop complex SQL queries, direct interaction with J2EE and Web application servers, build/deployment automation and application performance measurement and tuning.\nCollaborate with Project Managers and Stakeholders to execute on projects.\nOutline specific technical deliverables, provide input to project plans and milestones.\nProvide Technical leadership for projects to design effective solutions.\nMentor other developers on the team.\nLead key project activities - architecture, design, development, QA/QC and deployment of new J2ee/Web applications.\nCommunicate project plans and status with Supervisor.\nEnsure that applications adhere to Application Engineering guidelines, processes and procedures.\nDevelop technical deliverables and review technical documents.\nProvide required development or operational support.\nProvide support outside of business hours.\nWork closely with the IT liaisons and external services providers to improve and optimize applications to deliver superb performance and end-user experience.\n\nThese position responsibilities are not necessarily all-encompassing.\nOther duties, responsibilities, and qualifications may be required and/or assigned as necessary.\nExperience and Qualifications:\n\n7 years or more of progressively responsible application development experience.\nExperience with front end development in large-scale Enterprise Java applications.\nDemonstrated ability to create reusable components that can be leveraged across multiple applications.\nDemonstrated ability to support, review application logs and dive into root cause analysis.\nExceptional attention to detail, organization, planning and project management skills.\nStrong quantitative, analytical, critical-thinking and problem-solving skills.\nProven ability to influence and work with cross-functional teams.\nSignificant skill required to work effectively across internal functional areas in situations where clear parameters may not exist.\nProven record of being a strong team player - a whatever-it-takes attitude to complete a project successfully for the team.\nStrong work ethic and personal integrity; self-directed and self-motivated with a highly developed curiosity and willingness to learn and to teach.\nExcellent verbal and written communication skills as well as interpersonal and influencing skills.\nAbility to define and capture business needs along with articulating strategic implications of analytic results with clarity and persuasiveness in an audience-appropriate manner.\nSoftware development in language pertinent to project (Java, HTML5, CSS3, node.js, JavaScript (JQuery).\nStrong front end and backend development skills. Solid experience in Java design, coding, testing and debugging techniques.\nSolid experience in enterprise-level J2EE platforms using J2EE design patterns. Solid experience in SOAP/REST web service development.\nStrong SQL knowledge - especially on DB2 preferred.\nSpring Framework, JMS, DOJO, AJAX, Eclipse, Hibernate, JUnit, Struts.\nXML/JSON data interchange formats. Subversion/Git. JBoss, Tomcat is required.\nFamiliarity with IBM DB2 and Oracle databases.\nHighly motivated self-starter who is very good at learning and mastering new technologies without much guidance.\n\nPreferred Skills:\n\nPrevious consulting experience desired\nFamiliarity with Informatica's ETL/MDM\n\nEducation:\n\nBachelor's degree, preferably in computer science, engineering, mathematics, statistics or related discipline.\nGraduate degree preferred.\nJava Certification is a plus.\nAWS Developer certification is a plus.\n\nApply today on:\n\nOr learn more at ptechpartners.com\nAbout Peterson Technology Partners\nPeterson Technology Partners (PTP) is proud to be Chicago's premier Information Technology (IT) staffing, consulting, and recruiting firm for over 22+ years.\nOur 250+ employees have a narrow focus on a single market (Chicago) and have expertise in 4 innovative technical areas:\n\n\nArtificial Intelligence/Machine Learning/Data Science\n\n\nRobotics/Robotic Process Automation (RPA)\n\n\nCyber/Data/Information Security\n\n\nDevOps/DevSecOps\n\n\nConnect: LinkedIn | Facebook | Twitter | YouTube | All Social Links\nApply: Stack Overflow | Dice | LinkedIn | Glassdoor | All Job Openings\nReview: Google | Glassdoor | Yelp | All Review Links\nListen: iTunes | Spotify | Stitcher | All Podcast Links\nPeterson Technology Partners is an Equal Opportunity Employer\n\n"},
 {'Title': 'Front End Developer',
  'Company': 'WHQ',
  'Contract-Type': 'Full Time',
  'Location': 'Chicago',
  'Time-Posted': 'over 1 year ago',
  'Apply-To': 'https://worldhqinc.com/join/front-end-developer/',
  'Skills': ['team'],
  'Desc': "\nYou’re always looking at new technologies and you push to innovate. WHQ is where you need to be. We’re a team of designers, developers, and strategists who work on web, mobile, environmental and brand projects. Tough problems demand big ideas. We think quickly and are always looking for ways to push our clients and ourselves. Think you'd fit in? Read on.\nResponsibilities:\n\nWrite solid HTML, CSS and JavaScript for web sites and applications\nBuild responsive web sites that function perfectly on any device or browser size\nPerform cross-browser compatibility tests and iterate to work through bugs\nJump into existing JavaScript applications, or start them from the ground up\nLearn new technologies and share ideas\n\nQualifications:\n\nExpert skills in HTML, CSS and JavaScript\nExperience with JavaScript frameworks\nExperience will Less or Sass\nSolid command of responsive layouts\nExperience with Git and version control tools\nTesting experience is a plus\n3+ years within the industry\n\n"},
 {'Title': 'Senior Python Engineer',
  'Company': 'Squirro',
  'Contract-Type': 'Full Time',
  'Location': 'Zurich',
  'Time-Posted': 'over 1 year ago',
  'Apply-To': 'mailto:jobs@squirro.com',
  'Skills': ['team'],
  'Desc': '\nWe’re looking for senior engineers with solid Python skills to join our team, which is building a platform, called Squirro, for unstructured data analysis.\nSquirro can ingest data from anywhere, be it public on the web or social medium or internal, such as a CRM, database or ITSM system, and add structure to it so that it can be delivered to business users using our dashboard visualisations or consumed by other systems using our APIs. We add structure to unstructured data by employing a range of techniques, from statistical and Bayesian models to supervised and unsupervised machine learning which we serve to our customers as a unified and patented technology we call Smartfilters. Meanwhile, for our users, we provide a simple interface to access these technologies so that anyone with basic analytical skills can get value out of their companies unstructured data.\nOur customers are some of the largest banks and financial institutions in the world, across the US, UK, EU, Switzerland and Asia. Many of our customers are just beginning to discover the potential of unstructured data analysis and we’re excited by the opportunity as an early mover in this young market. While we host some of these customers in the cloud, the majority prefer to install Squirro on-premise for security reasons.\nWe need you to help us build out and scale this platform, as our customers apply it to ever growing volumes of data and discover new ways to structure and analyse that data.\nRequired Qualifications\n\nExceptional programming experience in Python\nExtensive knowledge of UNIX/Linux from a developers perspective\nStrong track record in software systems design, from initial implementation to performance optimisation and scaling\nExperience developing professionally as part of a team, giving and receiving code reviews, test-driven development etc.\nGood communication skills with fluency in English\nSwiss citizenship or work permit in Switzerland, or living and working in UK, EU or EFTA member state. We’d love to hire people worldwide but Swiss immigration law makes this problematic except in rare cases.\n\nNice to Have\n\nBS, MS or PhD in Computer Science or related technical field\nExperience with information retrieval technologies (Elasticsearch, Lucene)\nComfortable working with large datasets and designing systems able to process and scale up to large data volumes\nFamiliarity with RESTful web services and microservices architectures\nExperience with MySQL, Redis, nginx, Zookeeper and other technologies in the Squirro stack\nFamiliarity with AWS, Terraform, Prometheus, Grafana, Ansible and other DevOps related tools\nAwareness of machine learning as applied to text analysis\n\nWorking with Us\nSquirro is a Swiss startup with an international flavour. Our team of passionate technology geeks and entrepreneurs mix local “Swissness” with American, German, French, Russian, Indian, Portuguese, Polish and British into an all-round startup team that combines the excellence of the ETH and EPFL with experience from technology companies such as Microsoft and Google as well as Swiss players such as local.ch and DeinDeal.\nWe love Python and ElasticSearch on the server side and JavaScript, backbone.js, React, D3 and more on the client side. We work with git, believe in testing, code reviews, continuous integration and continuous deployment. Our work is structured loosely around scrum with help from Jira and the Atlassian tool suite. We take design and user experience seriously and apply machine learning in the context of text analysis.\nMost of all we’re serious about building a world-class company and our compensation package includes shares because we believe our employees should be rewarded for their hard work and dedication.\nOur engineering office is in the heart of Zürich, with easy access to public transport.\n'}]
        
        self.jobLst=entry
        
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
            print(records[0][0])
            if term in records[i]:
                results.append(records[i])
                return records[i]
        return records
        

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








