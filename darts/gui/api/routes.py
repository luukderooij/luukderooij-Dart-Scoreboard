
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
from darts.toneighty import TonEighty
from darts.winners import Winners
from darts.finishes import Finishes
from darts import settings
from darts.players import Players
from darts.toneighty import TonEighty
from darts.winners import Winners
from darts.finishes import Finishes
from darts.tournament import Tournament
from darts.playoffs import Playoffs

logger = logging.getLogger(__name__)

api = Blueprint('api', __name__)


class RegistrationForm(FlaskForm):
    id = StringField('id')
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired(), Length(min=2, max=20)])
    arcadename = StringField('Arcadename', validators=[Optional(), Length(min=3, max=3)])
    email = StringField('Email', validators=[Optional(), Email()])
    submit = SubmitField('Sign Up')

@api.route('/api/get/winners', methods=['GET', 'POST'])
def api_scoreboard_winners():
    winners = Winners().sorted()

    response = make_response(jsonify(winners), 200)

    # Doesnt work. Gives CORS Error.
    response.headers.add('Access-Control-Allow-Origin','*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')

    return response
   

@api.route('/api/get/onehunderdandeighty', methods=['GET', 'POST'])
def api_scoreboard_onehunderdandeighty():
    onehunderdandeighty = TonEighty().sorted()

    response = make_response(jsonify(onehunderdandeighty), 200)

    # Doesnt work. Gives CORS Error.
    response.headers.add('Access-Control-Allow-Origin','*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')

    return response


@api.route('/api/get/finishes', methods=['GET', 'POST'])
def api_scoreboard_finishes():
    finishes = Finishes().sorted()

    response = make_response(jsonify(finishes), 200)

    # Doesnt work. Gives CORS Error.
    response.headers.add('Access-Control-Allow-Origin','*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')

    return response

    
@api.route('/api/get/players', methods=['GET', 'POST'])
def api_get_players():
    players = Players().fetchall()

    response = make_response(jsonify(players), 200)

    return response


@api.route('/api/add/player', methods=['GET', 'POST'])   
def api_add_player():    
    form = RegistrationForm()

    if form.validate_on_submit():
        Players().add(form.firstname.data,
                    form.lastname.data,
                    form.nickname.data,
                    form.arcadename.data,
                    form.email.data)
    return redirect('/players')


@api.route('/api/update/player', methods=['GET', 'POST'])   
def api_update_player():    
    form = RegistrationForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            
            id = form.id.data
            firstname = form.firstname.data
            lastname = form.lastname.data
            nickname = form.nickname.data
            arcadename = form.arcadename.data
            email = form.email.data
      
            Players().update(id, firstname, lastname, nickname, arcadename, email)

    return redirect('/players')


@api.route('/api/remove/player', methods=['GET', 'POST'])   
def api_remove_player():    
    jsonData = request.get_json()

    playerid = int(jsonData['playerid'])
    Players().remove(playerid)

    response = make_response(jsonify('ok'), 200)

    return response


@api.route('/api/add/180', methods=['GET', 'POST'])   
def api_add_180():    
    jsonData = request.get_json()
    playerid = int(jsonData['id'])
    TonEighty().add(playerid)   

    response = make_response(jsonify('ok'), 200)

    return response


@api.route('/api/get/trowed180', methods=['GET', 'POST'])   
def api_get_trowed180():    
    toneightys=TonEighty().fetchall()

    response = make_response(jsonify(toneightys), 200)

    return response


@api.route('/api/remove/180', methods=['GET', 'POST'])   
def api_remove_180():    
    jsonData = request.get_json()
    id = int(jsonData['id'])

    TonEighty().remove(id)

    response = make_response(jsonify('ok'), 200)

    return response


@api.route('/api/add/winner', methods=['GET', 'POST'])   
def api_add_winner():    
    jsonData = request.get_json()
    playerid = int(jsonData['id'])
    print(playerid)
    Winners().add(playerid)   

    response = make_response(jsonify('ok'), 200)

    return response


@api.route('/api/get/wins', methods=['GET', 'POST'])   
def api_get_winners():    
    winners = Winners().fetchall()
    print(winners)
    print('hier')
    response = make_response(jsonify(winners), 200)

    return response


@api.route('/api/remove/winner', methods=['GET', 'POST'])   
def api_remove_winners():    
    jsonData = request.get_json()
    id = int(jsonData['id'])
    print(id)
    Winners().remove(id)

    response = make_response(jsonify('ok'), 200)

    return response


@api.route('/api/get/finishes', methods=['GET', 'POST'])   
def api_get_finishes():    
    finishes = Finishes().fetchall()

    response = make_response(jsonify(finishes), 200)

    return response

@api.route('/api/add/finish', methods=['GET', 'POST'])   
def api_add_finish():    
    jsonData = request.get_json()
    playerid = int(jsonData['playerID'])
    trowed = int(jsonData['trowed'])
    combination = str(jsonData['combination'])

    Finishes().add(playerid, trowed, combination)    

    response = make_response(jsonify('ok'), 200)


    return response

@api.route('/api/remove/finish', methods=['GET', 'POST'])   
def api_remove_finish():    
    jsonData = request.get_json()
    id = int(jsonData['id'])

    Finishes().remove(id)

    response = make_response(jsonify('ok'), 200)

    return response


@api.route('/api/add/tournament', methods=['GET', 'POST'])   
def api_add_tournament():    

    jsonData = request.get_json()

    print(jsonData)

    tournament_name = str(jsonData['tournament_name'])
    number_dartboards = int(jsonData['number_dartboards'])
    number_pools = int(jsonData['number_pools'])
    selected_players = jsonData['players']

    selected_players_list = []

    for players in selected_players:
        #player = players['firstname'] + ' "' + players['nickname'] + '" ' + players['lastname'] 
        player = players['nickname']
        selected_players_list.append(player)

    try:
        Tournament().create(tournament_name, selected_players_list, number_pools, None, number_dartboards)
    except ValueError as e:
        response = make_response(jsonify(message=str(e)), 400)
        return response
      
    response = make_response(jsonify('ok'), 200)
    return response




@api.route('/api/get/matches/', methods=['GET','POST'])
def getmatches():
    if request.method == 'POST':
        pass
    tid = request.args.get('tournamentid')
    pid = request.args.get('pouleid')

    if tid == None:
        tid = Tournament().get_latest_tournament_id()

    matches=Tournament().api_get_matches(tid)

    res = make_response(jsonify(matches), 200)
    res.headers.add('Access-Control-Allow-Origin','*')
    return res


@api.route('/api/get/tournament/standings/', methods=['GET','POST'])
def gettournamentstandings():
    if request.method == 'POST':
        pass
    tid = request.args.get('tournamentid')
    pid = request.args.get('pouleid')

    if tid == None:
        tid = Tournament().get_latest_tournament_id()

    matches=Tournament().api_get_tournament_standings(tid)

    res = make_response(jsonify(matches), 200)
    res.headers.add('Access-Control-Allow-Origin','*')
    return res


@api.route('/api/update/tournament', methods=['GET','POST'])
def updatetournament():
    if request.method == 'POST':
        data = request.json

        tournament_id = data['tournament_id']
        pool = data['pool']
        match_id = data['match_id']
        score_1 = data['score_1']
        score_2 = data['score_2']
        
        Tournament().update_matches(score_1, score_2, tournament_id, pool, match_id)

    result = 'abcd'
    return result

@api.route('/api/create/playoffs', methods=['GET','POST'])
def createplayoffs():
    if request.method == 'POST':
        data = request.json
        
        TOURNAMENT_ID = Tournament().get_latest_tournament_id()

        if not Tournament().are_all_machtes_played(TOURNAMENT_ID):
            res = make_response(jsonify({"status": False, "message": "Not all matches are played"}),200)
            print('not all played')
        elif Playoffs().bracket_data(TOURNAMENT_ID):
            res = make_response(jsonify({"status": False, "message": "Playoffs already created!"}),200)
            print('Playoffs already created')
        else:
            rounds = data['rounds']
            if isinstance(rounds, int):
                Playoffs().create(TOURNAMENT_ID, rounds)
            else:
                Playoffs().create(TOURNAMENT_ID)

            res = make_response(jsonify({"status": True, "message": "no message!!!!"}),200)

    return res



@api.route('/api/update/playoffs', methods=['GET','POST'])
def updateplayoffs():
    if request.method == 'POST':
        data = request.json

        tournament_id = data['tournament_id']
        round = data['round']
        match = data['match_id']
        score_1 = data['score_1']
        score_2 = data['score_2']
        
        Playoffs().update_bracket(tournament_id, round, match, score_1, score_2)
 
    result = 'abcd'
    return result


@api.route('/api/get/playoffs/matches/', methods=['GET','POST'])
def getplayoffsmatches():
    if request.method == 'POST':
        pass
    tid = request.args.get('tournamentid')
    pid = request.args.get('pouleid')

    if tid == None:
        tid = Tournament().get_latest_tournament_id()

    matches=Playoffs().api_get_matches(tid)

    res = make_response(jsonify(matches), 200)
    res.headers.add('Access-Control-Allow-Origin','*')
    return res

@api.route('/api/create/playoffs/match', methods=['GET','POST'])
def createplayoffsmatch():
    if request.method == 'POST':
        data = request.json
        if data['status'] == 'ok':
            Playoffs().next_bracket(Tournament().get_latest_tournament_id())

            

    res = make_response(jsonify({"status": True, "message": "no message!!!!"}),200)

    return res


@api.route('/api/remove/playoffs/match', methods=['GET','POST'])
def removeplayoffsmatch():
    if request.method == 'POST':
        data = request.json


        Playoffs().remove_bracket(data['tournament_id'], data['round'], data['match_id'])


    res = make_response(jsonify({"status": True, "message": "no message!!!!"}),200)

    return res


@api.route('/api/get/playoffs/winner', methods=['GET','POST'])
def checkforwinner():
    if request.method == 'POST':
        data = request.json

        winner = Playoffs().winner_bracket(Tournament().get_latest_tournament_id())

        if winner == None:
            print('None')
            # response = make_response(jsonify({"winner": "None"}), 400)
            response = make_response(jsonify({"status": "false", "winner": "None"}),200)
        else:
            print(winner)
            # response = make_response(jsonify({"winner": winner}),200)
            response = make_response(jsonify({"status": "true", "winner": winner}),200)

    return response


@api.route('/api/upload/image/')
def uploadimage():
    tournament_id = str(Tournament().get_latest_tournament_id())
    path = os.path.join(os.getcwd(), "uploads")

    print(f"Path = {path}")
    print(f"Path = {settings.DATA_DIR}")
    #j

    files = []
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and tournament_id in i:
            files.append(i)


    if files: 
        return send_from_directory(path, files[0], as_attachment=False)
    else:
        abort(404)


@api.route('/api/upload/file', methods=['POST'])
def uploadfile():
    if request.method == 'POST':
        tournament_id = str(Tournament().get_latest_tournament_id())
        file = request.files['file']
        print(file)
        print(os.getcwd())
        filename = secure_filename(file.filename)
        print(filename)
        filename_old, file_extension = os.path.splitext(filename)
        filename = os.path.join(tournament_id + file_extension)
        print(filename)

        folder = 'uploads'
        if not os.path.exists(os.path.join(settings.DATA_DIR, folder)):
            logger.info(f'Creating folder uploads!')
            os.makedirs(os.path.join(settings.DATA_DIR, folder))

        print(f"Path = {settings.DATA_DIR}")

        #file.save(os.path.join(".\\uploads\\", filename))
        print(os.path.join(os.getcwd(), "uploads", filename))
        file.save(os.path.join(os.getcwd(), "uploads", filename))
   
    response = make_response('Response')
    return response





@api.route('/api/get_player', methods=['POST'])
def get_player():

    req = request.get_json()

    print(req)

    playerid = int(req['playerid'])
    session['id'] = playerid 

    player = Players().fetchone(playerid)

    res = make_response(player, 200)

    return res





@api.route('/api/menu', methods=['POST'])
def menu():
    if request.method == 'POST':

        jsonData = request.get_json()

        if 'button' in jsonData:
            button = jsonData['button']

            if button == 'shutdown':
                try:
                    print("voer shutdown os command uit")
                    os.system("sudo shutdown -h now")
                except:
                    print("os command SHUTDOWN niet gelukt")


            elif button == 'reboot':
                try:
                    print("voer reboot os command uit")
                    os.system("sudo reboot")
                except:
                    print("os command SHUTDOWN niet gelukt")


            elif button == 'marks_tournament':
                try:
                    logger.info('Marks tournament openen!')
    
                    os.environ['DISPLAY'] = ':0'
                    os.system("sudo -u pi chromium-browser -kiosk --app http:localhost:8080")
                except:
                    print("os command niet gelukt")


            elif button == 'tournament':
                try:
                    logger.info('tournament openen!')

                    os.environ['DISPLAY'] = ':0'
                    print(os.environ.get('DISPLAY'))
                    
                    subprocess.call(['xset', '-dpms'])
                    subprocess.call(['xset', 's', 'off'])
                    subprocess.call(['xset', 's', 'noblank'])
                    
                    subprocess.Popen(['chromium-browser', '--kiosk', 'http://localhost/tv/tournament'])
                except:
                    print("os command niet gelukt")


            elif button == 'scoreboard':
                try:
                    logger.info('scoreboard openen!')

                    os.environ['DISPLAY'] = ':0'
                    print(os.environ.get('DISPLAY'))
                    
                    subprocess.call(['xset', '-dpms'])
                    subprocess.call(['xset', 's', 'off'])
                    subprocess.call(['xset', 's', 'noblank'])
                    
                    subprocess.Popen(['chromium-browser', '--kiosk', 'http:localhost/tv/scoreboard'])
                except:
                    print("os command niet gelukt")


    response = make_response(jsonify({"status": "true"}),200)
    return response

@api.route('/api/log', methods=['GET','POST'])
def log():

    if request.method == 'POST':

        jsonData = request.get_json()
        print(jsonData)

    with open(settings.LOG_FILE) as log:
        logs = log.read().splitlines()
    #limit loglines
    logs = logs[-100:]
    
    logs.reverse()
    response = make_response(jsonify({"log": logs}),200)
    return response

#####################################################################################
# -----  api Marks tv site -----
#####################################################################################



@api.route('/api/get/tournament/', methods=['GET','POST'])
def gettournament():
    if request.method == 'POST':
        pass
    tid = request.args.get('tournamentid')
    pid = request.args.get('pouleid')

    if tid == None:
        tid = Tournament().get_latest_tournament_id()

    matches=Tournament().api_get_tournament(tid)

    res = make_response(jsonify(matches), 200)
    res.headers.add('Access-Control-Allow-Origin','*')
    return res





