"""
Routes and views for the flask application.
"""

from datetime import datetime

from flask import render_template, redirect, request, session, make_response, jsonify

from TestFlaskJadeWeb import app
from TestFlaskJadeWeb.models import PollNotFound
from TestFlaskJadeWeb.models.factory import create_repository
from TestFlaskJadeWeb.settings import REPOSITORY_NAME, REPOSITORY_SETTINGS

from .github_jobs import *
from .PlotlyGraphs import *

import sqlite3
import requests

repository = create_repository(REPOSITORY_NAME, REPOSITORY_SETTINGS)

#posts = 200  # num posts to generate
#quantity = 10  # num posts to return per request

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page, which varies depending on the type of user."""

    # sets the page to load depending on the type of user
    # if none specified the login screen will be displayed
    pageName = ''
    userType = session.get('UserType', None)
    if userType == None:
        pageName = 'anonHome.jade'
    elif userType == 'Seeker':
        pageName = 'indexJob.jade'
    elif userType == 'Manager':
        pageName = 'indexManager.jade'

    uName = session.get('UserName', 'Unknown') # load a default value if retrieval fails
    return render_template(
        pageName,
        title='Home',
        name=uName,
        year=datetime.now().year,
    )

@app.route("/logout")
def logout():
    # logs out users, removes session info and redirects to home page
    # home page will display the login screen

    session['UserType'] = None
    session['UserName'] = None
    session['offset'] = 0

    return redirect('/')

@app.route('/tmpGraph')
def graph():
    """Renders the temp graph page"""
    port_to_csv()
    return render_template(
        'tmpGraph.jade',
        title="Graph",
        year=datetime.now().year,
        src=s_modular(request.form.get('GraphType', ''), '')
    )

@app.route('/graphOptions', methods=['POST'])
def graphOptions():
    return render_template('tmpGraph.jade', title = 'Graph', 
                           src = s_modular(request.form.get('GraphType', ''), '', 
                                           request.form.get('xAxis', ''), request.form.get('yAxis', '')))

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.jade',
        title='Contact',
        year=datetime.now().year,
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.jade',
        title='About',
        year=datetime.now().year,
        repository_name=repository.name,
    )

def getRank():
    userDict = data().getUserByName(session['UserName'])

    rank = ''
    if userDict['Points'] >= 0 and userDict['Points'] <= 100:
        rank = 'Bronze'
    elif userDict['Points'] > 100 and userDict['Points'] <= 150:
        rank = 'Silver'
    elif userDict['Points'] > 150 and userDict['Points'] <= 200:
        rank = 'Gold'
    else:
        rank = 'Platinum'

    return rank

@app.route('/seekerProfile')
def userProfile():
    userDict = data().getUserByName(session['UserName'])
    return render_template('profileUser.jade', 
                           title = 'Profile', 
                           name = userDict['userName'], 
                           points = userDict['Points'],
                           frogRank = getRank(),
                           skills = str_to_lst(userDict['skills']) if not userDict['skills'] == None else '')

@app.route('/UpdateUserProfile', methods=['POST'])
def updateUserProfile():
    if not request.form.get('UserName', '') == '':
        data().updateColumn(session['UserName'], 'username', request.form['UserName'])

    if not request.form.get('email', '') == '':
        data().updateColumn(session['UserName'], 'email', request.form['email'])

    if not request.form.get('Location', '') == '':
        data().updateColumn(session['UserName'], 'location', request.form['Location'])

    userDict = data().getUserByName(session['UserName'])
    if not request.form.get('skill', '') == '':
        uSkills = userDict['skills']
        skillsLst = str_to_lst(uSkills) if not uSkills == None else [request.form['skill']]
        skillsLst.append(request.form['skill'])
        uSkills = lst_to_str(skillsLst)
        data().updateColumn(session['UserName'], 'skills', uSkills)

    if not request.form.get('Skills', 'None') == 'None':
        uSkills = userDict['skills']
        skillsLst = str_to_lst(uSkills) if not uSkills == None else [request.form['skill']]
        print(request.form['Skills'])
        print(skillsLst)
        skillsLst.remove(request.form['Skills'])
        uSkills = lst_to_str(skillsLst)
        data().updateColumn(session['UserName'], 'skills', uSkills)

    userDict = data().getUserByName(session['UserName']) # value changed
    return render_template('profileUser.jade', 
                           title = 'Profile', 
                           name = userDict['userName'], 
                           points = userDict['Points'],
                           frogRank = getRank(),
                           skills = str_to_lst(userDict['skills']) if not userDict['skills'] == None else '')

@app.route('/post')
def postJobs():
    return render_template('postJobs.jade', title = 'Post')

@app.route('/PostJobs', methods=['POST'])
def submitJob():
    print('test')
    #TODO: add job to jobs table

@app.route('/bookmark/<ind>')
def bookmark(ind):
    userRecords = data().getUserByName(session['UserName'])
    bookmarks = userRecords['Bookmarks']
    bmLst = str_to_lst(bookmarks)

    if not ind in bmLst:
        bmLst.append(str(ind))
    bookmarks = lst_to_str(bmLst)
    data().updateBookmarks(session['UserName'], bookmarks)

    data().gamePoints(session['UserName'], 5)
    return render_template('searchPageJob.jade', title = 'Search')

@app.route('/jobPage/<cnt>')
def jobPage(cnt):
    if session['UserType'] == 'Seeker':
        job = data().getNthJob(cnt)
        return render_template(
            'pageJob.jade',
            title = job['jobTitle'],
            jobTitle = job['jobTitle'],
            jobCompany = job['company'],
            jobContract = job['jobType'],
            jobLoc = job['location'],
            jobDesc = job['jobDes'],
            applyTo = job['jobApp'],
            pay = job['salary'],
            spanApply = 'Apply at ' + job['company'],
            jobIndex = cnt
        )
    else:
        user = data().getNthUser(cnt)
        return render_template('pageJob.jade',
                               title = user['userName'],
                               jobTitle = user['userName'],
                               jobCompany = user['skills'],
                               jobDesc = user['bio'],
                               applyTo = user['email'],
                               jobLoc = user['location'],
                               spanApply = 'Contact ' + user['email'],
                               jobIndex = cnt)

@app.route('/load')
def load():
    counter = int(request.args.get("c"))  # The 'counter' value sent in the QS
    session['offset'] = counter

    d = data()

    #if counter < posts: # TODO: change posts value
    print(f"2) Returning posts {counter} to {counter + 10}")
        
    if session['UserType'] == 'Seeker':
        if session.get('search', '') == '':
            res = make_response (jsonify (d.getNJobs(session['offset'], 10)), 200)
        else:
            res = make_response (jsonify (d.getNJobsByQuery(session['search'], session['column'], session['offset'], 10)), 200)
            #print('OFFSET ' + str(session['offset']))
    
    elif session['UserType'] == 'Manager':
        if session.get('search', '') == '':
            users = [row for row in d.getNUsers(session['offset'], 10) if row[1]['userType'] == 'Seeker']
            res = make_response (jsonify (users), 200)
        else:
            users = [row for row in d.getNUsersByQuery(session['search'], session['column'], session['offset'], 10) if row[1]['userType'] == 'Seeker']
            res = make_response (jsonify (users), 200)

    #else:
    #    print("No more posts")
    #    res = make_response(jsonify({}), 200)

    return res

@app.route('/managerSearch')
def userSearch():
    session['offset'] = 0
    return render_template('searchPageUser.jade', title = 'Search')

@app.route('/jobSearch') # routes from menu links
def jobSearch():
    #session['filteredJobs'] = []
    session['offset'] = 0
    return render_template(
            'searchPageJob.jade',
            title = 'Search'
            #quickSearch = None,
            #distance = None,
            #pay = None,
            #fTime = None,
            #loc = None,
            #pTime = None
        )

@app.route('/jobFilter', methods=['POST']) # routes from filter list update
def jobFilter():
    session['column'] = request.form.get('colTitle', '')
    session['column2'] = request.form.get('colTitle2', '')
    session['column3'] = request.form.get('colTitle3', '')

    session['search'] = request.form.get('jobFullSearch', '')
    session['search2'] = request.form.get('jobFullSearch2', '')
    session['search3'] = request.form.get('jobFullSearch3', '')

    loc = ''
    if session['column'] == 'location':
        loc = session['column']
    if session['column2'] == 'location':
        loc = session['column2']
    if session['column3'] == 'location':
        loc = session['column3']

    filtersDict = { 'Location':loc }

    # set to None if all vals are ''
    filtersDict = None if all(val == '' for val in filtersDict.values()) else filtersDict

    #if request.form.get('jobFullSearch', '').lower() == 'all':
    #    searchJobs('ALL JOBS', None)

    if not request.form.get('jobFullSearch', '') == '':
        searchJobs(
            request.form.get('jobFullSearch', ''), 
            filtersDict)

    #fd = ''
    #if filtersDict == None:
    #    fd = 'None'
    #else:
    #    for key, val in filtersDict.items():
    #        fd = fd + key + ': ' + val + ', '

    return render_template(
            'searchPageJob.jade',
            title = 'Search'
            #pay = request.form.get('Pay', '~~~'),
            #fTime = request.form.get('FullTime', '~~~'),
            #pTime = request.form.get('PartTime', '~~~'),
            #loc = request.form.get('Location', '~~~'),
            #quickSearch = None
            #FiltersDesc = fd
        )

# API call to get jobs, populates allJobs
# uses search params to filter jobs, filtered jobs added to filteredJobs
# param filters is a dictionary
def searchJobs(search, filters):
    #loc = 'chicago'
    #if filters != None and 'Location' in filters.keys():
    #    loc = filters['Location']

    jobsData = data()
    jobsData.create(request.form.get('jobFullSearch', ''), '', 1)

    #jobsPage = []
    #if request.form.get('QuickSearch', '') == '':
    #    jobsPage = jobsData.getNJobsByQuery(request.form.get('jobFullSearch', ''), request.form.get('colTitle', ''), session['offset'], 10)
    #else:
    #    jobsPage = jobsData.getNJobsByQueryQuickly(request.form.get('QuickSearch', ''), session['offset'], 10)

    #filteredJobs = []

    #print('SEARCH: ', search)
    #for job in jobsPage:
    #    #if search == 'ALL JOBS': # display all available jobs
    #    #    session['filteredJobs'].append(job)
    #    #    continue

    #    if search == 'CLEAR':
    #        #session['filteredJobs'] = []
    #        break

    #    #print(job)
        #jobL = dict((key, tryLow(val)) for key, val in job[1].items()) # convert all vals in the dict to lower
        ##if filters == None: # no filters used, search by search query
        #if any(search.lower() in val for val in jobL.values()):
        #    job[0] = len(filteredJobs) # index correction
        #    filteredJobs.append(job)
        #    continue # added job, don't need to keep checking this job

        #else: # include filters in search
        #    if any(search.lower() in val for val in jobL.values()):
        #        if searchFilters(job[1], filters): 
        #            job[0] = len(filteredJobs) # index correction
        #            filteredJobs.append(job)
        #            continue # added job, don't need to keep checking this job

        # filter logic
        # if all or any subset of filters then add if it also matches the search criteria
        # else if no filters set search exclusively by the search criteria

# converts the given string to lowercase 
# assumes that the input may be a list 
#   in this case it will convert all the strings in the list to lowercase
def tryLow(string):
	try:
		return string.lower()
	except:
		return [x.lower() for x in string]

# searches the given list of skills with the given search string
def searchSkills (search, skills):
    for skill in skills:
        if search.lower() in skill.lower():
            return True

    return False

@app.route('/quickSearch', methods=['POST']) # routes from the quick search
def quickSearch():
    session['offset'] = 0
    if not request.form.get('jobFullSearch', None) == '':
        searchJobs(request.form.get('QuickSearch', ''), None)
    #else:
        #print('-- QUICKSEARCH CLEARING SEARCH --')
        #session['filteredJobs'] = []

    return render_template(
            'searchPageJob.jade',
            title = 'Search',
            quickSearch = request.form.get('QuickSearch', None)
            #distance = None,
            #pay = None,
            #fTime = None,
            #loc = None,
            #pTime = None
        )

@app.route('/seed', methods=['POST'])
def seed():
    conn = sqlite3.connect('Users.db')
    cursor = conn.cursor()

    enterStat = request.form.get('Enter', None) # L for login or R for register
    if enterStat == 'L': # login, determine usertype, and route page
        #get form values, search table, return results
        select_query = """select * from USERS where userName = ?"""
        cursor.execute(select_query, (request.form['UserName'],))
        records = cursor.fetchall()
        
        # check if none or multiple rows were returned
        # assumed name was incorrect
        if len(records) != 1:
            print("ERROR: Invalid user credentials")
            return redirect('/')

        # password matching with the value stored in the db
        # if match set session data otherwise incorrect password was supplied in login
        if records[0][1] == request.form['PassWord']:
            session['UserName'] = records[0][0]
            session['UserType'] = records[0][2]
        else:
            print("LOGIN ERROR: No such user found, incorrect credentials")
            return redirect('/')

        data().gamePoints(session['UserName'], 5)

        # page routing
        pageName = ""
        if (session['UserType'] == "Seeker"):
            pageName = 'indexJob.jade'
        elif (session['UserType'] == "Manager"):
            pageName = 'indexManager.jade'
        
        # load page
        return render_template(pageName, title='Home', name=session['UserName']) # redirect to home page, depends on user type
    
    
    # Register new user
    data().creatUsersTable() # only creates table if it doesn't already exist
    
    # check if the username is already in use
    if data().checkIfUserExist(request.form['UserName']):
        print("REGISTRATION ERROR: username already exists")
        return redirect('/')

    """ retrieve user input """
    seekerStat = request.form.get('Seeker', None) # get user input from the form safely
    managerStat = request.form.get('Manager', None) # returns None if user didn't input anything for that field
    typeOfUser = ""
    pageName = ""

    if seekerStat == 'on' and managerStat == 'on':
        typeOfUser = 'Both'
        pageName = 'indexManager.jade' #TODO: redirect for user type BOTH
    elif seekerStat == 'on':
        typeOfUser = 'Seeker'
        pageName = 'indexJob.jade'
    elif managerStat == 'on':
        typeOfUser = 'Manager'
        pageName = 'indexManager.jade'

    # store values for the session
    # similar to cookies but does not persist - will be deleted when the session ends
    session['UserName'] = request.form['UserName']
    session['UserType'] = typeOfUser

    # insert new user info into table
    insert_query = "INSERT INTO USERS (UserName, Password, UserType, Points) VALUES (?, ?, ?, ?);"
    data_tuple = (request.form['UserName'], request.form['PassWord'], typeOfUser, 20)
    cursor.execute(insert_query, data_tuple)
    conn.commit()
    cursor.close()

    # redirects to home page
    return render_template(pageName, title='Home', name=session['UserName']) 

@app.route('/results/<key>')
def results(key):
    """Renders the results page."""
    poll = repository.get_poll(key)
    poll.calculate_stats()
    return render_template(
        'results.jade',
        title='Results',
        year=datetime.now().year,
        poll=poll,
    )

@app.route('/poll/<key>', methods=['GET', 'POST'])
def details(key):
    """Renders the poll details page."""
    error_message = ''
    if request.method == 'POST':
        try:
            choice_key = request.form['choice']
            repository.increment_vote(key, choice_key)
            return redirect('/results/{0}'.format(key))
        except KeyError:
            error_message = 'Please make a selection.'

    return render_template(
        'details.jade',
        title='Poll',
        year=datetime.now().year,
        poll=repository.get_poll(key),
        error_message=error_message,
    )

@app.errorhandler(PollNotFound)
def page_not_found(error):
    """Renders error page."""
    return 'Page does not exist.', 404
