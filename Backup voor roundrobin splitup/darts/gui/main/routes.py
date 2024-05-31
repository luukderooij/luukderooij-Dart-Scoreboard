
import logging

from flask import Blueprint, render_template, render_template

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional


from darts.players import Players

logger = logging.getLogger(__name__)

main = Blueprint('main', __name__,  template_folder='templates', static_folder='static', static_url_path='/main/static')


class RegistrationForm(FlaskForm):
    id = StringField('id')
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired(), Length(min=2, max=20)])
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


@main.route('/create', methods=['GET', 'POST'])
def create_tournament():
    return render_template('create.html',
                            players=Players().fetchall())


@main.route('/tournament', methods=['GET', 'POST'])
def tournament():
    return render_template('tournament.html',
                            players=Players().fetchall())


@main.route('/playoffs-settings', methods=['GET', 'POST'])
def playoffs_settings():
    return render_template('playoffs-settings.html')