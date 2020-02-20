import requests
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen


def getDict(loc):
    baselink = 'https://www.indeed.com/jobs?q=computer+science&l='
    loc = loc = loc.replace(' ', '+')
    link = (baselink + loc)
    
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
    
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')

    #titles and links
    for pos in soup.find_all('div', class_='title'):
        titList.append(pos.a.get('title'))
        link = pos.a.get('href')
        linkList.append("https://www.indeed.com" + link)
    
    #companies
    for div in soup.find_all(name='div', attrs={'class':'row'}):
        company = div.find_all(name='span', attrs={'class':'company'})
        if len(company) > 0:
            for b in company:
                coList.append(b.text.strip())
        else:
            sec_try = div.find_all(name='span', attrs={'class':'result-link-source'})
            for span in sec_try:
                coList.append(span.text.strip())


    #locations
    spans = soup.findAll(['div', 'span'], attrs={'class': 'location'})
    for span in spans:
        locList.append(span.text)


    #dates
    spans = soup.findAll('span', attrs={'class': 'date'})
    for span in spans:
        dateList.append(span.text)


    #pay
    for div in soup.find_all(name='div', attrs={'class':'row'}):
        try:
            payList.append(div.find(name='span', attrs={'class':'salaryText'}).text.replace('\n', ''))
        except:
            try:
                payList.append(div.find(name='span', attrs={'class':'sjcl'}).text.replace('\n', ''))
            except:
                payList.append('N/A')

    
    dic ={}
    length = len(titList)


    #go into job links
    for l in linkList:

        #description
        source = requests.get(l).text
        soup = BeautifulSoup(source, 'lxml')
        desc = soup.find('div', class_='jobsearch-jobDescriptionText')
        desc = desc.text
        descList.append(desc)


        #skills
        skills = ['python', 'java', 'c++', 'sql', 'manage', 'javascript', 'linux', 'team', 'problem solving', 'front end', 'back end', 'html', 'css','json', 'xml','api', 'linux', 'nodejs', 'c#', 'spark', 'sas', 'matlab', 'excel', 'spark', 'hadoop', 'azure', 'spss', 'git']
        skillList1 = []
        desc = desc.lower().split()
        for i in desc:
            if i in skills and i not in skillList1:
                skillList1.append(i)
        skillList.append(skillList1)

        #category
        aiKeys = ['ai', 'a.i.', 'artificial intelligence', 'artificial']
        dlKeys= ['deep learning', 'neural networks', 'big data', 'deep', 'statistics']
        mlKeys = ['data mining', 'machine learning', 'cnn', 'rbm', 'machine', 'natural language', 'regression', 'fault diagnosis', 'intrusion detection']
        seKeys = ['software engineer', 'software development','code']

        sumList = desc

        for i in sumList:
            if i in aiKeys:
                catList.append('Artificial Intelligence')
        for i in sumList:
            if i in dlKeys:
                catList.append('Deep Learning')
        for i in sumList:
            if i in mlKeys:
                catList.append('Machine Learning')
        for i in sumList:
            if i in seKeys:
                catList.append('Software Engineer')
            else:
                catList.append('Other')

    
    for i in range (0, length):
        dicList.append(dict({'Company':coList[i], 'Location': locList[i], 'Title': titList[i], 'Date Created': dateList[i], 'Salary': payList[i], 'Link':linkList[i],'Skills': skillList[i], 'Description': descList[i], 'Category': catList[i]}))

    return (dicList)


getDict('chicago')
