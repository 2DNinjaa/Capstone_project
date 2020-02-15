"""
Routes and views for the flask application.
"""

from datetime import datetime

from flask import render_template, redirect, request, session, make_response, jsonify

from TestFlaskJadeWeb import app
from TestFlaskJadeWeb.models import PollNotFound
from TestFlaskJadeWeb.models.factory import create_repository
from TestFlaskJadeWeb.settings import REPOSITORY_NAME, REPOSITORY_SETTINGS

import sqlite3
import requests

repository = create_repository(REPOSITORY_NAME, REPOSITORY_SETTINGS)

#Testing
#import random
#heading = "{Lorem ipsum dolor sit amet.}"
#content = """
#[Lorem ipsum dolor sit amet consectetur, adipisicing elit. 
#Repellat inventore assumenda laboriosam, 
#obcaecati saepe pariatur atque est? Quam, molestias nisi].
#"""
testJob = {
    'Title': 'Experienced JavaScript Front End Developer', 
    'Company': 'Combinaut',
    'Contract-Type': 'Full Time', 
    'Time-Posted': '7 days ago', 
    'Location': 'Chicago',
    'Apply-To': 'mailto:alex@combinaut.com', 
    'Skills': ['team'], 
    'Desc': """Combinaut is seeking an experienced JavaScript Front End Developer. Combinaut has an immediate need for a developer who has a minimum of  5 years’ professional experience working in JavaScript as a front end developer. We are looking for someone who will be able to work with near autonomy toward agreed goals, with the occasional need for material direction or implementation changes. Ideal candidates will have experience following established patterns and approaches within existing code bases with ease. We are looking for candidates experienced with Backbone.js, Git, and who have a strong understanding of system design. Preference will be given to candidates with Ruby on Rails experience. Our ideal candidate has a team-first mindset, collaborating with our internal and client-side stakeholders to solve problems, design new features, and deliver solid technical solutions. Combinaut - What we Make Combinaut creates tools for healthcare providers to help patients find care. It is important work, and we believe in what we do. We are seeking a full-time Chicago-based staff developer to join our Chicago and remote team. Working With Combinaut We are a very lean crew, with six developers and a handful of support positions. Our developers must work well both independently and collaboratively, each team member is responsible for building and maintaining our end-to-end software stack. We’re a self-organizing team that moves quickly together and contributes across the stack as needed (regardless of specialized knowledge or experience). Every team member is expected to be able to communicate with clarity and professionalism with internal team members as well as with clients. Combinaut believes diversity and inclusion make the workplace better and our product stronger. Every applicant for this position will be considered."""
    }
db = list()  # The mock database
posts = 200  # num posts to generate
quantity = 10  # num posts to return per request
for x in range(posts):
        """
        Creates messages/posts by shuffling the heading & content 
        to create random strings & appends to the db
        """
        #heading_parts = None
        #heading_parts = heading.split(" ")
        #random.shuffle(heading_parts)

        #content_parts = content.split(" ")
        #random.shuffle(content_parts)

        db.append([x, testJob])
print('-- DB LEN --')
print(len(db))


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page, which varies depending on the type of user."""
    #print('--- SEARCH SESSION') # debug stuff, testing what session returns
    #print(session.get('UserType', None))

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

    return redirect('/')

@app.route('/tmpGraph')
def graph():
    """Renders the temp graph page"""
    return render_template(
        'tmpGraph.jade',
        title="Graph",
        year=datetime.now().year,
    )

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

@app.route('/jobPage/<cnt>')
def jobPage(cnt):
    #print('-- TEST JOB LOAD --')
    #print(cnt)
    #print(db[int(cnt)])
    print(db[int(cnt)][1])
    #print('-- END TEST --')
    return render_template(
        'pageJob.jade',
        title = db[int(cnt)][1]['Title'],
        jobTitle = db[int(cnt)][1]['Title'],
        jobCompany = db[int(cnt)][1]['Company'],
        jobContract = db[int(cnt)][1]['Contract-Type'],
        jobLoc = db[int(cnt)][1]['Location'],
        jobDesc = db[int(cnt)][1]['Desc']
    )

@app.route('/load')
def load():
    counter = int(request.args.get("c"))  # The 'counter' value sent in the QS
    print(counter)

    if counter == 0:
        print(f"Returning posts 0 to {quantity}")
        # Slice 0 -> quantity from the db
        res = make_response(jsonify(db[0: quantity]), 200)

    elif counter == posts:
        print("No more posts")
        res = make_response(jsonify({}), 200)

    else:
        print(f"Returning posts {counter} to {counter + quantity}")
        # Slice counter -> quantity from the db
        res = make_response(jsonify(db[counter: counter + quantity]), 200)
        #https://pythonise.com/categories/javascript/infinite-lazy-loading#the-example
        #https://www.youtube.com/watch?v=AuBai920D0E
    return res

@app.route('/jobSearch') # routes from menu links
def jobSearch():
    return render_template(
            'searchPageJob.jade',
            title = 'Search',
            quickSearch = None,
            distance = None,
            pay = None,
            fTime = None,
            pTime = None
        )

@app.route('/jobFilter', methods=['POST']) # routes from filter list update
def jobFilter():
    return render_template(
            'searchPageJob.jade',
            title = 'Search',
            distance = request.form.get('Distance', None),
            pay = request.form.get('Pay', None),
            fTime = request.form.get('FullTime', None),
            pTime = request.form.get('PartTime', None),
            quickSearch = None
        )

@app.route('/quickSearch', methods=['POST']) # routes from the quick search
def quickSearch():
    return render_template(
            'searchPageJob.jade',
            title = 'Search',
            quickSearch = request.form.get('QuickSearch', None),
            distance = None,
            pay = None,
            fTime = None,
            pTime = None
        )

@app.route('/seed', methods=['POST'])
def seed():
    conn = sqlite3.connect('Users.db')
    cursor = conn.cursor()

    registerStat = request.form.get('Register', None)
    if registerStat == None: # login, determine usertype, and route page
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

        # page routing
        pageName = ""
        if (session['UserType'] == "Seeker"):
            pageName = 'indexJob.jade'
        elif (session['UserType'] == "Manager"):
            pageName = 'indexManager.jade'
        
        # load page
        return render_template(pageName, title='Home', name=session['UserName']) # redirect to home page, depends on user type
    
    #table_query = "drop table USERS"
    #cursor.execute(table_query)
    #conn.commit()

    # safety - if table doesn't exist create it
    table_query = "create table if not exists USERS (userName text, passWord text, userType text)"
    cursor.execute(table_query)
    conn.commit()

    sqlite_select_query = """SELECT * from USERS"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    #print("Total rows are:  ", len(records))
    #print("Printing each row")
    for row in records:
        if row[0] == request.form['UserName']: # don't allow duplicate entries
            print("REGISTRATION ERROR: username already exists")
            return redirect('/')

        #print("name: ", row[0])
        #print("pass: ", row[1]) 
        #print("type: ", row[2])
        #print("\n")

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
    insert_query = "INSERT INTO USERS (UserName, Password, UserType) VALUES (?, ?, ?);"
    data_tuple = (request.form['UserName'], request.form['PassWord'], typeOfUser)
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
