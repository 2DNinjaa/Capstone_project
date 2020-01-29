"""
Routes and views for the flask application.
"""

from datetime import datetime

from flask import render_template, redirect, request

from TestFlaskJadeWeb import app
from TestFlaskJadeWeb.models import PollNotFound
from TestFlaskJadeWeb.models.factory import create_repository
from TestFlaskJadeWeb.settings import REPOSITORY_NAME, REPOSITORY_SETTINGS

import sqlite3
import requests
from bs4 import BeautifulSoup

repository = create_repository(REPOSITORY_NAME, REPOSITORY_SETTINGS)

# defines what type of user is currently active
# placeholder for later
userType = "Anon"

@app.route('/')
@app.route('/home')
def home():
    pageName = ""
    if (userType == "Seeker"):
        pageName = 'indexJob.jade'
    elif (userType == "Manager"):
        pageName = '#'
    elif (userType == "Anon"):
        pageName = 'anonHome.jade'

    """Renders the home page, which varies depending on the type of user."""
    return render_template(
        pageName,
        title='Home',
        year=datetime.now().year,
        polls=repository.get_polls(),
    )

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

@app.route('/seed', methods=['POST'])
def seed():
    """Seeds the database with sample polls."""
    conn = sqlite3.connect('Users.db')
    cursor = conn.cursor()

    registerStat = request.form.get('Register', None)
    print("--- REGISTER STAT ---")
    print(registerStat)
    if registerStat == None:
        #login, determine usertype, and route page

        #get form values, search table, return results
        returningUserType = "Anon"
        select_query = """select * from USERS where userName = ?"""
        cursor.execute(select_query, (request.form['UserName'],))
        records = cursor.fetchall()
        for row in records:
            if row[1] == request.form['PassWord']:
                returningUserType = row[2]
            print("name: ", row[0])
            print("pass: ", row[1]) 
            print("type: ", row[2])
            print("\n")

        print("--- USER TYPE: " + returningUserType)
        if returningUserType == "Anon":
            print("No such user found, incorrect credentials")
            return redirect("/")

        pageName = ""
        if (returningUserType == "Seeker"):
            pageName = 'indexJob.jade'
        elif (returningUserType == "Manager"):
            pageName = '#'
        
        return render_template(pageName) 
    
    #table_query = "drop table USERS"
    #cursor.execute(table_query)
    #conn.commit()

    table_query = "create table if not exists USERS (userName text, passWord text, userType text)"
    cursor.execute(table_query)
    conn.commit()

    sqlite_select_query = """SELECT * from USERS"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    print("Total rows are:  ", len(records))
    print("Printing each row")
    for row in records:
        if row[0] == request.form['UserName']:
            print("username already exists")
            return redirect('/')

        print("name: ", row[0])
        print("pass: ", row[1]) 
        print("type: ", row[2])
        print("\n")

    """ retrieve user input """
    print('--- TEST INFO ---')
    print(request.form['UserName'])

    seekerStat = request.form.get('Seeker', None)
    managerStat = request.form.get('Manager', None)
    typeOfUser = ""
    pageName = ""

    if seekerStat == 'on' and managerStat == 'on':
        typeOfUser = 'Both'
    elif seekerStat == 'on':
        typeOfUser = 'Seeker'
        pageName = 'indexJob.jade'
    elif managerStat == 'on':
        typeOfUser = 'Manager'
        pageName = '#'

    insert_query = "INSERT INTO USERS (UserName, Password, UserType) VALUES (?, ?, ?);"
    data_tuple = (request.form['UserName'], request.form['PassWord'], typeOfUser)
    cursor.execute(insert_query, data_tuple)
    conn.commit()
    cursor.close()

    """used to redirect to different page, however this just returns to the current page"""
    return render_template(pageName) 

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
