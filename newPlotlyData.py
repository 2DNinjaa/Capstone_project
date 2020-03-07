import plotly.offline as pyo
import pandas as pd             
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import csv
import xlrd
import sqlite3
import unicodecsv as csv
import plotly.express as px
import numpy as np
from collections import Counter
import chart_studio.tools as tls
import chart_studio.plotly as py
import statistics

def connect():
        conn = sqlite3.connect("Flask_Jade_Sample/TestFlaskJadeWeb/Users.db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM JOBS')
        with open('output.csv','wb') as out_csv_file:
            csv_out = csv.writer(out_csv_file)
  # write header                        
            csv_out.writerow([d[0] for d in cursor.description])
  # write data                          
            for result in cursor:
                csv_out.writerow(result)
        conn.close()
        
        
#----------NOT AS GOOD AS NEWSKILLS()0-------
def skillGraph():
     jobs = pd.read_csv(r'C:\Users\lilyk\Desktop\Capstone_project-master\output.csv')
     skills = (jobs['skills'])
     
     count = skills.value_counts()
     count = (count.head(10))
     skillset = (count.axes)
     skillsNew = []
     
     for i in range (0,10):
         skillsNew.append(skillset[0][i])
     

     fig = px.bar(jobs, x= skillsNew, y = count, color = skillsNew, labels={'y': 'Frequency', 'x': 'Skill Set'}, title = 'Top 10 Most Desired Skill Sets')
     fig.show()




#FREQ OF JOB CAT GRAPH
def catCount():
     jobs= pd.read_csv(r'C:\Users\lilyk\Desktop\Capstone_project-master\output.csv')
     cat = jobs['category']
     count = (cat.value_counts())
     a = ['Artificial Inetlligence', 'Software Engineer', 'Deep Learning', 'Machine Learning']
     t = []
     t.append(count['Artificial Intelligence'])
     t.append(count['Software Engineer'])
     t.append(count['Deep Learning'])
     t.append(count['Machine Learning'])
     

     fig2 = px.bar(jobs, x = a, y= t, color = a, labels={'y': 'Frequency', 'x': 'Category'}, title= ' Frequency of Job Categories')
     fig2.show()


     #This puts it in your cloud for your Chart Studios Account
     #You can switch it to be your account/api_key from your account.
     tls.set_credentials_file(username = 'lbecker7', api_key = '3ztc7kdqWPHtPtkhusiy')

     url = py.plot(fig2, filename = 'categoryFig', auto_open = True)

     return (tls.get_embed(url))
     


#-----------Kind of Working---------
    #thots: maybe try separating them and making different graphs for hourly/salary jobs?
def salaries():
    jobs= pd.read_csv(r'C:\Users\lilyk\Desktop\Capstone_project-master\output.csv')

    salary = jobs['salary'].dropna()
    category = jobs['category'].dropna().head(200)
    salary = np.array(salary)
    titles = jobs['jobTitle'].dropna().head(200)
    sals = []
    for i in range (len(salary)):

        test = (salary[i].split())
        nums = []
        
        for i in test:
            if  i.startswith('$'):

                number = (i.strip('$'))
                number = number.replace(",",'')
                number = float(number)
                nums.append(number)
            else:
                sals.append(0.0)

        sals.append(statistics.mean(nums))


    fig3 = px.bar(jobs, x=category, y = sals, color = sals,
                  labels={'y': 'Salaries', 'x': 'Category'},title = 'Salaries for Different Job Categories'
                  , height=400)

    
    tls.set_credentials_file(username = 'lbecker7', api_key = '3ztc7kdqWPHtPtkhusiy')

     
    url = py.plot(fig3, filename = 'salFig', auto_open = True)

    return (tls.get_embed(url))



#SKILLS GRAPH
def newSkills():
     jobs = pd.read_csv(r'C:\Users\lilyk\Desktop\Capstone_project-master\output.csv')

     skills = (jobs['skills'].dropna())
     skills = skills.str.split(',')
     #GETS THE UNIQUE SKILLS
     u = []
     for x in skills:
         for i in x:
             u.append(i)
     countDict =  (Counter(u))
     vals = countDict.values()
     keys = countDict.keys()

     keys,values = zip(*countDict.items())


     
     fig = px.bar(jobs, x= keys, y = values,color = keys, labels={'y': 'Frequency', 'x': 'Skill'}, title = 'Most Desired Skills')
     #fig.show()

     #This puts it in your cloud for your Chart Studios Account
     #You can switch it to be your account/api_key from your account.
     tls.set_credentials_file(username = 'lbecker7', api_key = '3ztc7kdqWPHtPtkhusiy')

     
     url = py.plot(fig, filename = 'skillFig', auto_open = True)

     return (tls.get_embed(url))
     
    
#EDUCATION GRAPH
def edus():
     jobs = pd.read_csv(r'C:\Users\lilyk\Desktop\Capstone_project-master\output.csv')

     edus = (jobs['education'].dropna())
     edus = edus.str.split(',')
 
     #GETS THE UNIQUE EDUS
     u = []
     for x in edus:
         for i in x:
             i = i.replace('bachelors', "bachelor's")
             u.append(i)
     countDict =  (Counter(u))
     vals = countDict.values()
     keys = countDict.keys()

     keys,values = zip(*countDict.items())


     
     fig = px.bar(jobs, x= keys, y = values,color = keys, labels={'y': 'Frequency', 'x': 'Education'}, title = 'Most Desired Education Levels')
     #fig.show()

     #This puts it in your cloud for your Chart Studios Account
     #You can switch it to be your account/api_key from your account.
     tls.set_credentials_file(username = 'lbecker7', api_key = '3ztc7kdqWPHtPtkhusiy')

     
     url = py.plot(fig, filename = 'eduFig', auto_open = True)

     return (tls.get_embed(url))
    

#NOT ACCURATE - DOES NOT WORK
def edu_sal():
     jobs = pd.read_csv(r'C:\Users\lilyk\Desktop\Capstone_project-master\output.csv')
                                                        #makes it so u can graph, but messes up data 
     edus = (jobs['education'].fillna('Not Specified').head(235))
     edus = edus.str.split(',')
     
 
     #GETS THE UNIQUE EDUS
     u = []
     for x in edus:
         for i in x:
             i = i.replace('bachelors', "bachelor's")
             u.append(i)
     print(len(u))

     #keys,values = zip(*countDict.items())
     ##KEYS IS EDUS


     salary = jobs['salary'].dropna()

     salary = np.array(salary)
 
     sals = []
     for i in range (len(salary)):

       # print (salary[i])
         test = (salary[i].split())
         nums = []
        
         for i in test:
             if  i.startswith('$'):

                 number = (i.strip('$'))
                 number = number.replace(",",'')
                #print (number)
                 number = float(number)
                #print (number)
                 nums.append(number)
             else:
                 pass
                 
                
             try:
                 sals.append(statistics.mean(nums))
             except:
                 sals.append(nums)

     #print (sals)
     print (len(sals))

     fig = px.scatter(jobs, x= u, y = sals,color = u, labels={'y': 'Sal', 'x': 'Education'}, title = 'edu/sal', size = sals)
     

     tls.set_credentials_file(username = 'lbecker7', api_key = '3ztc7kdqWPHtPtkhusiy')

     
     url = py.plot(fig, filename = 'scatEduSal', auto_open = True)

     return (tls.get_embed(url))
    
#returns a list of the iframes to send to the front end
def getIframes():
    iframes = []
    iframes.append(newSkills())
    iframes.append(catCount())
    iframes.append(salaries())
    iframes.append(edu_sal())
    return (iframes)
        


