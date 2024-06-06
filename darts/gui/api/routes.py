
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
from darts.roundrobin import RoundRobin
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
    tournament_matches = RoundRobin().get_tournament_matches_data(tournament_id)
    tournament_players = tournament.get_tournament_players_data(tournament_id)


    if tournament_data[0][4] == 0: # If teams are enabled
        tournament_matches_dict = []
        for value in tournament_matches:

            for team in tournament_teams:
                if value[4] == team[0]:
                    player1_id = team[4]
                if value[6] == team[0]:
                    player2_id = team[4]

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
        info = RoundRobin().update_match(tournament_id, match_id, team1_score, team2_score)

        
        teams = Tournament().get_tournament_teams_data(tournament_id)
        RoundRobin().create_tournament_standings(tournament_id, teams)

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
    tournament_id = Tournament().get_tourament_latest_id()
    players = Tournament().get_player_names(tournament_id)

    tournament_score = RoundRobin().get_tournament_standings(tournament_id)

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
    matches_played = RoundRobin().are_all_matches_played(tournament_id)
    response = make_response(jsonify(matches_played), 200)
    return response



@api.route('/api/playoffs/create', methods=['GET', 'POST'])
def create_playoffs():
    if request.method == 'POST':
        tournament_id = Tournament().get_tourament_latest_id()
        tournament_score = RoundRobin().get_tournament_standings(tournament_id)



        data = request.get_json()
        number_of_players = data["number_of_players"]
        all_players = data["all_players"]

        info = Playoffs().create_playoffs(number_of_players, all_players, tournament_score)
        return jsonify({"response": "Succes"}), 200
    return jsonify({"error": "Invalid request"}), 400





@api.route('/api/playoffs-matches/get', methods=['GET', 'POST'])
def api_get_playoffs_matches_score():
    tournament = Tournament()
    tournament_id = tournament.get_tourament_latest_id()
    tournament_data = tournament.get_tournament_data(tournament_id)
    tournament_teams = tournament.get_tournament_teams_data(tournament_id)
    tournament_players = tournament.get_tournament_players_data(tournament_id)

    playoffs_matches = Playoffs().get_matches_data(tournament_id)

    if tournament_data[0][4] == 0: # If teams are enabled
        tournament_matches_dict = []
        for match in playoffs_matches:
            team1_id = None
            team2_id = None 
            team1 = "-"
            team2 = "-"

            for team in tournament_teams:
                if match[3] == team[0]:
                    team1_id = team[4]
                if match[5] == team[0]:
                    team2_id = team[4]

            if team1_id:
                if not isinstance(team1_id, int):
                    team1_id = int(team1_id.strip('[]'))
            else:
                team1_id = None
            if team2_id:
                if not isinstance(team2_id, int):
                    team2_id = int(team2_id.strip('[]'))
            else:  
                team2_id = None

            print(team1_id, team2_id)

            for player in tournament_players:
                if team1_id == player[0]:
                    team1 = player[2] + " " + player[3]
                if team2_id == player[0]:
                    team2 = player[2] + " " + player[3]    

            print(match)

            match_dict = {
                "id": match[0],
                "tournament_id": match[1],
                "match_number": match[2],
                "team1_id": match[3],
                "team1_name": team1,
                "team1_score": match[4],
                "team2_id": match[5],
                "team2_name": team2,
                "team2_score": match[6],
                "referee_id": match[9],
                "board_id": match[10],
                "date_created": match[11],
                "date_updated": match[12]
            }


            tournament_matches_dict.append(match_dict)

    #     response = make_response(jsonify(tournament_matches_dict), 200)
    #     return response
    # else:
    #     tournament_matches_dict = []
    #     for value in playoffs_matches:

    #         for team in tournament_teams:
    #             if value[4] == team[0]:
    #                 team1_name = team[2]
    #             if value[6] == team[0]:
    #                 team2_name = team[2]

    #         match = {
    #             "match_id": value[0],
    #             "match_tournament_id": value[1],
    #             "match_poule_id": value[2],
    #             "match_number": value[3],
    #             "match_team1_id": team1_name,
    #             "match_team1_score": value[5],
    #             "match_team2_id": team2_name,
    #             "match_team2_score": value[7],
    #             "match_referee_id": value[8],
    #             "match_board_id": value[9],
    #             "match_date_created": value[10],
    #             "match_date_updated": value[11]
    #         }


    #         tournament_matches_dict.append(match)

        response = make_response(jsonify(tournament_matches_dict), 200)
        return response














@api.route('/api/playoffs-matches/update', methods=['GET', 'POST'])
def api_update_playoffs_matches():
    if request.method == 'POST':
        data = request.get_json()

        tournament_id = data["tournament_id"]
        match_id = data["match_number"]
        team1_score = data["team1_score"]
        team2_score = data["team2_score"]
        info = Playoffs().update_match(tournament_id, match_id, team1_score, team2_score)

        
        # teams = Tournament().get_tournament_teams_data(tournament_id)
        # RoundRobin().create_tournament_standings(tournament_id, teams)

        info = True
        if info == True:
            return jsonify({"response": "Succes"}), 200
        else :
            return jsonify({"response": info}), 200
        
    return jsonify({"error": "Invalid request"}), 400



















# @api.route('/api/playoffs-matches/get', methods=['GET', 'POST'])
# def api_get_playoffs_matches():


@api.route('/api/tournament/all', methods=['GET', 'POST'])
def api_tournament_all():
    tournament = Tournament()
    roundrobin = RoundRobin()
    playoffs = Playoffs()
    tournament_id = tournament.get_tourament_latest_id()
    tournament_data = tournament.get_tournament_data(tournament_id)
    tournament_teams = tournament.get_tournament_teams_data(tournament_id)
    tournament_matches = roundrobin.get_tournament_matches_data(tournament_id)
    tournament_players = tournament.get_tournament_players_data(tournament_id)
    tournament_playoffs_matches = playoffs.get_matches_data(tournament_id)


    tournament_teams_dict = []
    for value in tournament_teams:
        team = {
            "team_id": value[0],
            "team_tournament_id": value[1],
            "team_poule_id": value[2],
            "team_name": value[3],
            "team_players_id": value[4],
            "team_date_created": value[5],
            "team_date_updated": value[6]
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


    tournament_playoffs_matches_dict = []
    for value in tournament_playoffs_matches:
        match = {
            "id": value[0],
            "tournament_id": value[1],
            "match_id": value[2],
            "team1_id": value[3],
            "team1_score": value[4],
            "team2_id": value[5],
            "team2_score": value[6],
            "p1_last_match_id": value[7],
            "p2_last_match_id": value[8],
            "referee_id": value[9],
            "board_id": value[10],
            "date_created": value[11],
            "date_updated": value[12]
        }
        tournament_playoffs_matches_dict.append(match)


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
            "roundrobin_matches": tournament_matches_dict,
            "playoffs_matches": tournament_playoffs_matches_dict
        }


    response = make_response(jsonify(tournament_data_dict), 200)
    return response
            