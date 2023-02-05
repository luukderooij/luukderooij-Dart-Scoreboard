
import logging
import datetime

from flask import Blueprint, render_template

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional


from darts.players import Players
from darts.toneighty import TonEighty
from darts.winners import Winners
from darts.finishes import Finishes


logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)


class RegistrationForm(FlaskForm):
    id = StringField('id')
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired(), Length(min=2, max=20)])
    arcadename = StringField('Arcadename', validators=[Optional(), Length(min=3, max=3)])
    email = StringField('Email', validators=[Optional(), Email()])
    submit = SubmitField('Sign Up')


@main.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/players', methods=['GET', 'POST'])
def players():
    form = RegistrationForm()
    return render_template('players.html',
                            players=Players().fetchall(),
                            form = form)


@app.route('/180', methods=['GET', 'POST'])
def onehunderdandeighty():
    return render_template('180.html')


@app.route('/winner', methods=['GET', 'POST'])
def winner():
    return render_template('winner.html')


@app.route('/finishes', methods=['GET', 'POST'])
def finishes():
    return render_template('finishes.html')


@app.route('/create-tournament')
def createtournament():
    return render_template('create-tournament.html')


@app.route('/tournament')
def tournament():
    return render_template('tournament.html')


@app.route('/playoffs')
def playoffs():
    return render_template('playoffs.html')


@app.route('/winners')
def winners():
    return render_template('winners.html')


@app.route('/rules')
def rules():
    return render_template('rules.html')    


@app.route('/tv/scoreboard')
def scoreboard():
    return render_template('/tv/scoreboard.html',
                            winners=Winners().sorted(),
                            toneightys=TonEighty().sorted(),
                            finishes=Finishes().sorted())


@app.template_filter()
def format_datetime(value, format="%d-%m-%Y"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    date = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
    if value is None:
        return ""
    return datetime.strftime(date, format)


@app.route('/log')
@app.route('/log.html')
def log():
    return render_template('log.html')