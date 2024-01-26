
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


logger = logging.getLogger(__name__)

api = Blueprint('api', __name__)



# @api.route('/api/get/winners', methods=['GET', 'POST'])
# def api_scoreboard_winners():
#     winners = Winners().sorted()

#     response = make_response(jsonify(winners), 200)

#     # Doesnt work. Gives CORS Error.
#     response.headers.add('Access-Control-Allow-Origin','*')
#     response.headers.add('Access-Control-Allow-Methods', 'GET, POST')

#     return response
   
