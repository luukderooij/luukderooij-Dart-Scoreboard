
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
@main.route('/index')
def index():
    return render_template('index.html')


@main.route('/players', methods=['GET', 'POST'])
def players():
    form = RegistrationForm()
    return render_template('players.html',
                            players=Players().fetchall(),
                            form = form)


@main.route('/180', methods=['GET', 'POST'])
def onehunderdandeighty():
    return render_template('180.html')


@main.route('/winner', methods=['GET', 'POST'])
def winner():
    return render_template('winner.html')


@main.route('/finishes', methods=['GET', 'POST'])
def finishes():
    return render_template('finishes.html')


@main.route('/create-tournament')
def createtournament():
    return render_template('create-tournament.html')


@main.route('/tournament')
def tournament():
    return render_template('tournament.html')


@main.route('/playoffs')
def playoffs():
    return render_template('playoffs.html')


@main.route('/winners')
def winners():
    return render_template('winners.html')


@main.route('/rules')
def rules():
    return render_template('rules.html')    


@main.route('/tv/scoreboard')
def scoreboard():
    return render_template('/tv/scoreboard.html',
                            winners=Winners().sorted(),
                            toneightys=TonEighty().sorted(),
                            finishes=Finishes().sorted())


@main.template_filter()
def format_datetime(value, format="%d-%m-%Y"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    date = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
    if value is None:
        return ""
    return datetime.strftime(date, format)


@main.route('/log')
def log():
    return render_template('log.html')