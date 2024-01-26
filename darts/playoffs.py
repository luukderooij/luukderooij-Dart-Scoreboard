import logging
import datetime

import pandas as pd

from darts.config.dartdb import dartDB
from darts.tournament import Tournament
from darts.config import settings

logger = logging.getLogger(__name__)

class Playoffs:
    def __init__(self) -> None:
        self.table = "playoffs"


    def bracket_data(self, tournament_id):
        with dartDB(settings.DB_FILE) as db:
            sql_ = "SELECT * FROM playoffs WHERE tournament_id = :id"
            par_ = {"id": tournament_id}         
            data = db.fetchall(sql_, par_)   
        return data

    def create(self, tournament_id, rounds=None, players=None):
        if self.bracket_data(tournament_id):
            logger.info("Playoffs already exists!")   
            return

        if not rounds:
            rounds = 2

        if not players:
            standing_data = Tournament().get_standings(tournament_id)
 
        data = Tournament().get_tournament_info_data(tournament_id)
        poules = int((data[0][3]))
            
        number_of_players = 2 ** rounds
        number_of_matches = int(number_of_players / 2)
        players_per_poule = int(number_of_players / poules)

        df_standings = pd.DataFrame(standing_data, columns =['tournament_id',
                                                             'poule_id',
                                                             'position',
                                                             'player_name', 
                                                             'matches_played',
                                                             'matches_won',
                                                             'matches_lost',
                                                             'legs_scored',
                                                             'legs_against',
                                                             'legs_difference'])

        df_standings = df_standings[df_standings.position <= players_per_poule]

        count = 1 
        poule = 1

        for match in range(number_of_matches):
            match = match + 1

            if count > poules:
                poule = 1
                count = 1 

            if poules > 1:
                if count != poule:
                    break

                if df_standings.empty:
                    break

                try:
                    df_tmp1 = df_standings[df_standings['poule_id'] == count]
                    index = df_tmp1['position'].idxmin()
                    player1 = df_standings["player_name"][index]
                except:
                    pass
                
                poule_player_2 = count + 1
                if poule_player_2 > poules:
                    poule_player_2 = 1
    
                try:
                    df_tmp2 = df_standings[df_standings['poule_id'] == poule_player_2]
                    index = df_tmp2['position'].idxmax()
                    player2 = df_standings["player_name"][index]
                except:
                    pass

                df_standings = df_standings[df_standings['player_name'].str.contains(player1) == False]
                df_standings = df_standings[df_standings['player_name'].str.contains(player2) == False]

            else:
                # Get lowest position in dataframe
                index = df_standings['position'].idxmin()
                player1 = df_standings["player_name"][index]

                index = df_standings['position'].idxmax()
                player2 = df_standings["player_name"][index]               

                # Remove players from dataframe
                df_standings = df_standings[df_standings['player_name'].str.contains(player1) == False]
                df_standings = df_standings[df_standings['player_name'].str.contains(player2) == False]

            sql_ = """INSERT INTO playoffs VALUES (:tournament_id, :round,
                    :match, :board, :player_1, :score_1, :player_2, :score_2,
                    :referee, :date)"""
            par_ = {"tournament_id": tournament_id,
                    "round": rounds,            
                    "match": match,
                    "board": 1,
                    "player_1": player1,
                    "score_1": 0,
                    "player_2": player2,
                    "score_2": 0,
                    "referee": "",
                    "date": datetime.datetime.now()}

            with dartDB(settings.DB_FILE) as db:
                db.execute(sql_, par_)      

            poule = poule + 1
            count = count + 1

    # Update bracket
    def update_bracket(self, tournament_id, round, match, score1, score2):
        with dartDB(settings.DB_FILE) as db:
            sql_ = """UPDATE playoffs SET score_1 = :score_1, score_2 = :score_2 
                WHERE tournament_id = :tournament_id AND 
                round = :round AND match = :match"""
            par_ = {"tournament_id": tournament_id,
                    "round": round,
                    "match": match,
                    "score_1": score1, 
                    "score_2": score2}
            db.execute(sql_, par_) 

    # remove bracket
    def remove_bracket(self, tournament_id, round, match):
        with dartDB(settings.DB_FILE) as db:
            sql_ = "DELETE FROM playoffs WHERE tournament_id = :tournament_id AND round = :round AND match = :match"
            par_ = {"tournament_id": tournament_id, "round": round, "match": match}
            db.execute(sql_, par_) 





    # Create next bracket
    def next_bracket(self, tournament_id):
        winners = []    

        with dartDB(settings.DB_FILE) as db:
            sql_ = "SELECT * FROM playoffs WHERE tournament_id = :tournament_id"
            par_ = {"tournament_id": tournament_id}
            data = db.fetchall(sql_, par_)   

        if not data:
            logger.info("No bracket data found for next_bracket")
            return

        df_bracket = pd.DataFrame(data, columns =['tournament_id', 
                                                'round', 
                                                'match', 
                                                'board', 
                                                'player1', 
                                                'score1', 
                                                'player2', 
                                                'score2', 
                                                'referee', 
                                                'date'])
        

        print(df_bracket)

        round = int(df_bracket['round'].min()) - 1

        print(df_bracket['round'].min())



        if round == 0:
            logger.info("All brackets are played!")
            return

        for index, row in df_bracket.iterrows():
            if row['score1'] != None and row['score2'] != None:
                if row['score1'] > row['score2']:
                    winners.append(row['player1'])
                else:
                    winners.append(row['player2'])
            else:
                logger.info("Not all matches are played.")
                return

        matches = int(len(winners) / 2) 
        board = 1 

        for match in range(matches):
            match = match + 1
            player_1 = winners[0]
            player_2 = winners[1]
            del winners[0:1]            

            with dartDB(settings.DB_FILE) as db:
                sql_ = """INSERT INTO playoffs VALUES (:tournament_id, :round,
                    :match, :board, :player_1, :score_1, :player_2, :score_2,
                    :referee, :date)"""
                par_ = {"tournament_id": tournament_id,
                    "round": round,          
                    "match": match,
                    "board": board,
                    "player_1": player_1,
                    "score_1": 0,
                    "player_2": player_2,
                    "score_2": 0,
                    "referee": "",
                    "date": datetime.datetime.now()}
                db.execute(sql_, par_)      



    # check bracket winner
    def winner_bracket(self, tournament_id):

        with dartDB(settings.DB_FILE) as db:
            sql_ = "SELECT * FROM playoffs WHERE tournament_id = :tournament_id"
            par_ = {"tournament_id": tournament_id}
            data = db.fetchall(sql_, par_) 

        winner = None
        df_bracket = pd.DataFrame(data, columns =['tournament_id', 
                                                'round', 
                                                'match', 
                                                'board', 
                                                'player_1', 
                                                'score_1', 
                                                'player_2', 
                                                'score_2', 
                                                'referee', 
                                                'date'])

        for index, row in df_bracket.iterrows():
            if row['round'] == 1:
                score1 = df_bracket.at[index, 'score_1']
                score2 = df_bracket.at[index, 'score_2']
       
                if score1 != 0 or score2 != 0:
                    if row['score_1'] > row['score_2']:
                        winner = row['player_1']
                    else:
                        winner = row['player_2']
        return winner





    def api_get_playoffs(self, tournament_id):

        with dartDB(settings.DB_FILE) as db:
            sql_ = "SELECT * FROM tournament WHERE id = :id"
            par_ = {"id": tournament_id}
            tournament_data = db.fetchall(sql_, par_)

            sql_ = "SELECT * FROM playoffs WHERE tournament_id = :id"
            par_ = {"id": tournament_id}
            playoff_data = db.fetchall(sql_, par_)




        # Check number of poules.
        for value in tournament_data:
            tournament_id = int(value[0])
            tournament_name = str(value[1])
            tournament_date = value[5]

        print(playoff_data)

        playoffs = []

        for match in playoff_data:
            playoff_dict = {
                "round": match[1],
                "match": match[2],
                "board": match[3],
                "player1": match[4],
                "score1": match[5],
                "player2": match[6],
                "score2": match[7],
                "referee": match[8]}
            playoffs.append(playoff_dict)

        print(playoffs)



        tournament_info = {"id": tournament_id,
        "name": tournament_name, 
        "date" : tournament_date,
        "playoffs": playoffs
        }

        tournament = []
        tournament.append(tournament_info)
        tournaments = {"tournaments": tournament}
    
        return tournaments


    def api_get_matches(self, tournament_id):
        with dartDB(settings.DB_FILE) as db:
            sql_ = "SELECT * FROM playoffs WHERE tournament_id = :id"
            par_ = {"id": tournament_id}
            match_data = db.fetchall(sql_, par_)

        matches = []

        for match in match_data:
            match_dict = {"tournament_id": tournament_id,
            "round": match[1],
            "match_id": match[2],
            "player_1": match[4],
            "score_1": match[5],
            "score_2": match[7],
            "player_2": match[6],
            "referee": match[8],
            "board": match[3]
            }

            matches.append(match_dict)

        return matches