##### TODO #####
# - Cleanup after deleting tournament


import logging
import datetime
import random
import pandas as pd
from time import sleep

from darts.config.dartdb import dartDB
from darts.roundrobin import RoundRobin
from darts.config import settings

logger = logging.getLogger(__name__)

class Tournament:    
    def __init__(self):
        self.table = "tournament"

    def create(self, data):
        tournament_name = data["tournament_name"]
        if not tournament_name:
            tournament_name = "Dubbel 1"

        number_of_poules = int(data["number_of_poules"]) if data["number_of_poules"] and data["number_of_poules"].isdigit() else 1

        number_of_boards = data["number_of_boards"]     
        if not number_of_boards:
            number_of_boards = 1

        teams = bool(data["teams"])
        if not teams:
            teams = False  

        players = data["selectedPlayers"]
        if not players:
            logger.error(f"No players are selected!")
            return "No players are selected!"

        date_created = datetime.datetime.now()
        date_updated = datetime.datetime.now()

        sql_ = f"""INSERT INTO {self.table} VALUES (NULL, :tournament_name, 
                  :number_of_poules, :number_of_boards, :teams, :date_created, :date_updated)"""
        par_ = {"tournament_name": tournament_name,        
                "number_of_poules": number_of_poules,
                "number_of_boards": number_of_boards,
                "teams": teams,
                "date_created": date_created,
                "date_updated": date_updated}
        with dartDB(settings.DB_FILE) as db:    
            tournament_id = db.execute(sql_, par_)

        self.add_players(tournament_id, players)
        self.create_teams(tournament_id)

        for poule in range(number_of_poules):
            poule = poule + 1
            teams = self.get_tournament_teams_data(tournament_id, poule)
            RoundRobin().create_matches(tournament_id, poule, teams)

        return True
    

    def add_players(self, tournament_id, players):    
        player_ids = []  
        for player in players:
            date_created = datetime.datetime.now()
            date_updated = datetime.datetime.now()
            sql_ = f"""INSERT INTO tournament_players VALUES (NULL, :tournament_id, :firstname, :lastname, :nickname, :date_joined, :date_updated)"""
            par_ = {"tournament_id": tournament_id, "firstname": player["firstname"], "lastname": player["lastname"], "nickname": player["nickname"], "date_joined": date_created, "date_updated": date_updated}
            with dartDB(settings.DB_FILE) as db:
                data = db.execute(sql_, par_)
                player_ids.append(data)

        if len(player_ids) == len(players): # Check if all players are added
            return True
        else:  
            return False


    def create_teams(self, tournament_id):
        tournament_info = self.get_tournament_data(tournament_id)
        if not tournament_info:
            return None
        
        players = self.get_tournament_players_data(tournament_id)
        if not players:
            return None

        # Get number of players.
        number_of_players = len(players)
        logger.info(f'Number of players: {number_of_players}')

        # Check if teams are enabled.
        if tournament_info[0][4]:
            if number_of_players % 2 != 0:
                number_of_teams = number_of_players // 2 + 1
                logger.info(f'Number of players ({number_of_players}) is not even! Teams can only be created with an even number of players. someone needs to play alone!')
            else:
                number_of_teams = number_of_players // 2
        else:
            number_of_teams = number_of_players

        logger.info(f'Number of teams: {number_of_teams}')

        teams = []
        for team in range(number_of_teams):
            team = team + 1
            teams.append(team)

        random.shuffle(teams)

        # Divide teams into poules
        poules = [[] for _ in range(tournament_info[0][2])]
        for team in teams:
            min_poule = min(poules, key=len) # Find the poule with the least amount of teams
            min_poule.append(team) # Add team to the poule with the least amount of teams

        # Create teams and save in database
        date_created = datetime.datetime.now()
        date_updated = datetime.datetime.now()

        sql_ = f"""INSERT INTO tournament_teams VALUES (NULL, :tournament_id, :poule_id, :team_name, :team_players_id, 
                :date_created, :date_updated)"""
        
        for team in range(number_of_teams):
            team = team + 1

            for i, poule in enumerate(poules):
                if team in poule:
                    poule_id = i + 1
                    break

            if tournament_info[0][4]:
                par_ = {"tournament_id": tournament_id,
                        "poule_id": poule_id,
                        "team_id": team,
                        "team_name": f"Team {team}",
                        "team_players_id": "",
                        "date_created": date_created,
                        "date_updated": date_updated}
            else:
                par_ = {"tournament_id": tournament_id,
                        "poule_id": poule_id,
                        "team_id": team,
                        "team_name": f"Team {team}",
                        "team_players_id": f"[{players[team-1][0]}]",
                        "date_created": date_created,
                        "date_updated": date_updated}
            
            with dartDB(settings.DB_FILE) as db:    
                db.execute(sql_, par_)

        return poules


    def get_tourament_latest_id(self):
        # Get the latest tournament id.
        sql_ = "SELECT * FROM tournament ORDER BY id DESC LIMIT 1"
        par_ = {}
        with dartDB(settings.DB_FILE) as db:
            data = db.fetchall(sql_, par_)
        return data[0][0]


    def get_tournament_data(self, tournament_id = None):
        # Get tournament data.
        if tournament_id:
            sql_ = "SELECT * FROM tournament WHERE id = :id"
            par_ = {"id": tournament_id}
        else:
            sql_ = "SELECT * FROM tournament"
            par_ = {}    
        with dartDB(settings.DB_FILE) as db:
            data = db.fetchall(sql_, par_)
        return data
    

    def get_tournament_players_data(self, tournament_id: int):
        # Get players data from a tournament.
        sql_ = "SELECT * FROM tournament_players WHERE tournament_id = :tournament_id"
        par_ = {"tournament_id": tournament_id}
        with dartDB(settings.DB_FILE) as db:
            data = db.fetchall(sql_, par_)
        return data

    
    def get_tournament_teams_data(self, tournament_id, poule_id=None):
        # Get teams data from a tournament.
        if poule_id:
            sql_ = "SELECT * FROM tournament_teams WHERE tournament_id = :tournament_id AND poule_id = :poule_id"
            par_ = {"tournament_id": tournament_id, "poule_id": poule_id}
        else:
            sql_ = "SELECT * FROM tournament_teams WHERE tournament_id = :tournament_id"
            par_ = {"tournament_id": tournament_id}
        with dartDB(settings.DB_FILE) as db:
            data = db.fetchall(sql_, par_)
        return data
    
  
    def delete_tournament(self, tournament_id):
        sql_ = "DELETE FROM tournament WHERE rowid = :id"
        par_ = {"id": tournament_id} 
        with dartDB(settings.DB_FILE) as db:
            data = db.execute(sql_, par_)   
        return data


    def get_player_names(self, tournament_id=None, teams_enables=None):
        if not tournament_id:
            tournament_id = self.get_tourament_latest_id()
        players = self.get_tournament_players_data(tournament_id)
        teams = self.get_tournament_teams_data(tournament_id)

        updated_players = []
        if not teams_enables:
            for team in teams:
                team_id = team[0]
                team_name = team[3]
                player_id = team[4]
                player_id =  int(player_id.strip('[]'))

                for player in players:
                    if player_id == player[0]:
                        firstname = player[2]
                        lastname = player[3]
                        nickname = player[4]

                data = {
                    "team_id": team_id,
                    "team_name": team_name,
                    "firstname": firstname,
                    "lastname": lastname,
                    "nickname": nickname
                }
                updated_players.append(data)

        return updated_players
        








        # teams = self.get_tournament_teams_data(tournament_id)
        # for i, poule_list in enumerate(poules, start=1):
        #     self.create_matches(tournament_id, i, poule_list, teams)
        # self.create_tournament_standings(tournament_id)



