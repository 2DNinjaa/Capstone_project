"""
Routes and views for the flask application.
"""

from datetime import datetime

from flask import render_template, redirect, request

from TestFlaskJadeWeb import app
from TestFlaskJadeWeb.models import PollNotFound
from TestFlaskJadeWeb.models.factory import create_repository
from TestFlaskJadeWeb.settings import REPOSITORY_NAME, REPOSITORY_SETTINGS

repository = create_repository(REPOSITORY_NAME, REPOSITORY_SETTINGS)

# defines what type of user is currently active
# placeholder for later
userType = "Seeker"

@app.route('/')
@app.route('/home')
def home():
    pageName = ""
    if (userType == "Seeker"):
        pageName = 'indexJob.jade'
    elif (userType == "Manager"):
        pageName = '#'

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
    repository.add_sample_polls()
    return redirect('/')

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
