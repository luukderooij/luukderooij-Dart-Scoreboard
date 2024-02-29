
import os
import logging
import datetime
import subprocess

from flask import Blueprint, render_template, Flask, redirect, request, render_template, send_file, session, jsonify, abort, make_response, flash, send_from_directory, send_file
from flask_wtf import FlaskForm

from werkzeug.utils import secure_filename

from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Optional

from darts.players import Players
from darts.config import settings

from darts.gui.main.routes import RegistrationForm


logger = logging.getLogger(__name__)

api = Blueprint('api', __name__)



@api.route('/api/get/players', methods=['GET', 'POST'])
def api_get_players():
    players = Players().fetchall()
    response = make_response(jsonify(players), 200)

    return response


@api.route('/api/player/add', methods=['GET', 'POST'])
def add_player():
    form = RegistrationForm()

    if form.validate_on_submit():  
        Players().add(form.firstname.data,
                    form.lastname.data,
                    form.nickname.data)
        
    return redirect('/players')


@api.route('/api/player/update', methods=['GET', 'POST'])   
def api_update_player():    
    form = RegistrationForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            
            id = form.id.data
            firstname = form.firstname.data
            lastname = form.lastname.data
            nickname = form.nickname.data
      
            Players().update(id, firstname, lastname, nickname)

    return redirect('/players')