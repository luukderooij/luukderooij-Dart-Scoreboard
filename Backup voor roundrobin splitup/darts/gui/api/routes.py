
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
from darts.tournament import Tournament
from darts.playoffs import Playoffs
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



@api.route('/api/tournament/create', methods=['GET', 'POST'])
def api_create_tournament():
    if request.method == 'POST':
        data = request.get_json()
        info = Tournament().create(data)

        if info == True:
            return jsonify({"response": "Succes"}), 200
        else :
            return jsonify({"response": info}), 200
        
    return jsonify({"error": "Invalid request"}), 400


@api.route('/api/tournament/get', methods=['GET', 'POST'])
def api_get_tournament():
    tournament = Tournament()
    tournament_id = tournament.get_tourament_latest_id()
    tournament_data = tournament.get_tournament_data(tournament_id)
    tournament_teams = tournament.get_tournament_teams_data(tournament_id)
    tournament_matches = tournament.get_tournament_matches_data(tournament_id)
    tournament_players = tournament.get_tournament_players_data(tournament_id)

    tournament_teams_dict = []
    for value in tournament_teams:
        team = {
            "team_id": value[0],
            "team_tournament_id": value[1],
            "team_name": value[2],
            "team_players_id": value[3],
            "team_date_created": value[4],
            "team_date_updated": value[5]
        } 
        tournament_teams_dict.append(team)

    tournament_matches_dict = []
    for value in tournament_matches:
        match = {
            "match_id": value[0],
            "match_tournament_id": value[1],
            "match_poule_id": value[2],
            "match_number": value[3],
            "match_team1_id": value[4],
            "match_team1_score": value[5],
            "match_team2_id": value[6],
            "match_team2_score": value[7],
            "match_referee_id": value[8],
            "match_board_id": value[9],
            "match_date_created": value[10],
            "match_date_updated": value[11]
        }
        tournament_matches_dict.append(match)

    tournament_players_dict = []
    for value in tournament_players:
        player = {
            "player_id": value[0],
            "player_tournament_id": value[1],
            "player_firstname": value[2],
            "player_lastname": value[3],
            "player_nickname": value[4],
            "player_date_created": value[5],
            "player_date_updated": value[6]
        }
        tournament_players_dict.append(player)  
    
    for value in tournament_data:
        tournament_data_dict = {
            "tournament_id": value[0],
            "tournament_name": value[1],
            "tournament_number_of_poules": value[2],
            "tournament_number_of_boards": value[3],
            "tournament_teams_enabled": value[4],
            "tournament_date_created": value[5],
            "tournament_date_updated": value[6],
            "tournament_players": tournament_players_dict,
            "tournament_teams": tournament_teams_dict,
            "tournament_matches": tournament_matches_dict
        }


    response = make_response(jsonify(tournament_data_dict), 200)
    return response
            

@api.route('/api/round-robin-matches/get', methods=['GET', 'POST'])
def api_get_round_robin_matches():
    tournament = Tournament()
    tournament_id = tournament.get_tourament_latest_id()
    tournament_data = tournament.get_tournament_data(tournament_id)
    tournament_teams = tournament.get_tournament_teams_data(tournament_id)
    tournament_matches = tournament.get_tournament_matches_data(tournament_id)
    tournament_players = tournament.get_tournament_players_data(tournament_id)


    if tournament_data[0][4] == 0: # If teams are enabled
        tournament_matches_dict = []
        for value in tournament_matches:

            for team in tournament_teams:
                if value[4] == team[0]:
                    player1_id = team[3]
                if value[6] == team[0]:
                    player2_id = team[3]

            player1_id = int(player1_id.strip('[]'))
            player2_id = int(player2_id.strip('[]'))

            for player in tournament_players:
                if player1_id == player[0]:
                    team1 = player[2] + " " + player[3]
                if player2_id == player[0]:
                    team2 = player[2] + " " + player[3]    

            match = {
                "match_id": value[0],
                "match_tournament_id": value[1],
                "match_poule_id": value[2],
                "match_number": value[3],
                "match_team1_id": team1,
                "match_team1_score": value[5],
                "match_team2_id": team2,
                "match_team2_score": value[7],
                "match_referee_id": value[8],
                "match_board_id": value[9],
                "match_date_created": value[10],
                "match_date_updated": value[11]
            }


            tournament_matches_dict.append(match)

        response = make_response(jsonify(tournament_matches_dict), 200)
        return response
    else:
        tournament_matches_dict = []
        for value in tournament_matches:

            for team in tournament_teams:
                if value[4] == team[0]:
                    team1_name = team[2]
                if value[6] == team[0]:
                    team2_name = team[2]

            match = {
                "match_id": value[0],
                "match_tournament_id": value[1],
                "match_poule_id": value[2],
                "match_number": value[3],
                "match_team1_id": team1_name,
                "match_team1_score": value[5],
                "match_team2_id": team2_name,
                "match_team2_score": value[7],
                "match_referee_id": value[8],
                "match_board_id": value[9],
                "match_date_created": value[10],
                "match_date_updated": value[11]
            }


            tournament_matches_dict.append(match)

        response = make_response(jsonify(tournament_matches_dict), 200)
        return response
    

@api.route('/api/round-robin-matches/update', methods=['GET', 'POST'])
def api_update_round_robin_matches():
    if request.method == 'POST':
        data = request.get_json()

        tournament_id = data["match_tournament_id"]
        match_id = data["match_id"]
        team1_score = data["match_team1_score"]
        team2_score = data["match_team2_score"]
        info = Tournament().update_match(tournament_id, match_id, team1_score, team2_score)

        info = True
        if info == True:
            return jsonify({"response": "Succes"}), 200
        else :
            return jsonify({"response": info}), 200
        
    return jsonify({"error": "Invalid request"}), 400

@api.route('/api/round-robin-matches-score/get', methods=['GET', 'POST'])
def api_get_round_robin_matches_score():
    if request.method == 'POST':
        pass
    # data = request.get_json()
    tournament = Tournament()
    tournament_id = tournament.get_tourament_latest_id()
    tournament_score = tournament.get_tournament_standings(tournament_id)
    players = tournament.get_player_names(tournament_id)

    score = []
    for poistion in tournament_score:
        for player in players:
          if poistion[4] == player['team_id']:
              team_name = player['team_name']
              firstname = player['firstname']
              lastname = player['lastname']
              nickname = player['nickname']          
          
        data = {
            "id": poistion[0],
            "tournament_id": poistion[1],
            "poule": poistion[2],
            "place": poistion[3],
            "name": f'{firstname} {nickname} {lastname}',
            "matches_played": poistion[5],
            "matches_won": poistion[6],
            "matches_lost": poistion[7],
            "legs_scored": poistion[8],
            "legs_against": poistion[9],
            "legs_difference": poistion[10],
        }
        score.append(data)


    sorted_score = sorted(score, key=lambda x: x['place'])
    response = make_response(jsonify(sorted_score), 200)
    return response

@api.route('/api/round-robin-matches-played/get', methods=['GET', 'POST'])
def are_matches_played():
    tournament = Tournament()
    tournament_id = tournament.get_tourament_latest_id()
    matches_played = tournament.are_all_matches_played(tournament_id)
    response = make_response(jsonify(matches_played), 200)
    return response



@api.route('/api/playoffs/create', methods=['GET', 'POST'])
def create_playoffs():
    if request.method == 'POST':
        data = request.get_json()
        number_of_rounds = data["number_of_rounds"]
        info = Playoffs().create_playoffs(number_of_rounds)
        return jsonify({"response": "Succes"}), 200
    return jsonify({"error": "Invalid request"}), 400