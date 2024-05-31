import logging
import datetime
import random
import pandas as pd
from time import sleep

from darts.config.dartdb import dartDB
from darts.config import settings

from darts.playoffstemplate import playoffs_template

logger = logging.getLogger(__name__)

class Playoffs:
    def __init__(self):
        pass

    def create_playoffs(self, number_of_players, all_players, tournament_score):
        try:
            number_of_players = int(number_of_players)
        except ValueError:
            number_of_players = False
            
        if all_players:
            number_of_players = len(tournament_score)

        if number_of_players:
            if int(number_of_players) < 2:
                number_of_players = 2
            if int(number_of_players) > len(tournament_score):
                number_of_players = len(tournament_score)
        else:  
            number_of_players = 2

        df = pd.DataFrame(tournament_score, columns=['id', 'tournamentId', 'pouleId', 'place', 'teamId', 'matchesPlayed', 'matchesWon', 'matchesLost', 'legsScored', 'legsAgainst', 'legsDifference', 'dateCreated', 'dateUpdated'])
        df = df.sort_values(by=['pouleId', 'place'])
        df = df.iloc[:, :-8]

        number_of_poules = df['pouleId'].nunique()
        # template = playoffs_template()


        print(df)

        place_to_teamid = dict(zip(df['place'], df['teamId']))


        if number_of_poules == 1:
            template = playoffs_template(number_of_players, number_of_poules)

            for round in template['rounds']:
                for match in round['matches']:

                    if match['player1']:
                        match['player1'] = place_to_teamid[match['player1']]
                    if match['player2']:
                        match['player2'] = place_to_teamid[match['player2']]


            for round in template['rounds']:
                for match in round['matches']:
                    print(f"Player 1: {match['player1']} - Player 2: {match['player2']}")   


        if number_of_poules == 2:
            template = playoffs_template(number_of_players, number_of_poules)
            for round in template['rounds']:
                for match in round['matches']:

                    if match['player1']:
                        p1_place = match['player1']
                        p1_poule = match['p1_poule_id']
                        match['player1'] = df[(df['place'] == p1_place) & (df['pouleId'] == p1_poule)]['teamId'].values[0]
                    else:
                        match['player1'] = 0
                    if match['player2']:
                        p2_place = match['player2']
                        p2_poule = match['p2_poule_id']
                        match['player2'] = df[(df['place'] == p2_place) & (df['pouleId'] == p2_poule)]['teamId'].values[0]
                    else:
                        match['player2'] = 0


        for round in template['rounds']:
            for match in round['matches']:


                print(match['player1'])



        with dartDB(settings.DB_FILE) as db:
            sql_ = "SELECT rowid, * FROM tournament_playoffs_matches WHERE tournament_id = :tournament_id"
            par_ = {"tournament_id": df['tournamentId'].values[0]}
            data = db.fetchall(sql_, par_)

        if not data: 
            for round in template['rounds']:
                for match in round['matches']:


                    print(match['player1'])


                    date_created = datetime.datetime.now()
                    date_updated = datetime.datetime.now()
                    sql_ = """INSERT INTO tournament_playoffs_matches VALUES (NULL, :tournament_id, :match_id, :team1_id, :team1_score, :team2_id, :team2_score, :p1_last_match_id, :p2_last_match_id, :referee, :board, :date_created, :date_updated)"""
                    par_ = {"tournament_id": int(df['tournamentId'].values[0]),
                            "match_id": int(match["match_id"]),
                            "team1_id": int(match["player1"]),
                            "team1_score": 0,
                            "team2_id": int(match["player2"]),
                            "team2_score": 0,
                            "p1_last_match_id": match["p1_last_match_id"],
                            "p2_last_match_id": match["p2_last_match_id"],
                            "referee": "",
                            "board": 0,
                            "date_created": date_created,
                            "date_updated": date_updated}
                    with dartDB(settings.DB_FILE) as db:
                        db.execute(sql_, par_)







    def get_tournament_matches_data(self, tournament_id):
            # Get matches data from a tournament.
            sql_ = "SELECT * FROM tournament_playoffs_matches WHERE tournament_id = :tournament_id"
            par_ = {"tournament_id": tournament_id}
            with dartDB(settings.DB_FILE) as db:
                data = db.fetchall(sql_, par_)
            return data






'''
With the use of the df where the position and poule of the teams are i would like to create a playoff. we can use the template from the playoffs_template.py file. use number_of_players to determine the amount of players in the playoff.
if there are more players than the number_of_players we can use the first x players in the playoff. it needs always to be equal between the poules if there is more than 1 poule.
   
    
111111111111

Use the data from data.tx
Help me with wrinting python code that will do the following:

With the use of the df where the position and poule of the teams are. Create a playoff tournament with the use of the template. 

- Make it possible to use the template if there are more than 8 players. something like reusing the same template.
- if there is 1 poule you can use the template without changes.
- if there is more than 1 poule players always need to play against someone from another poule. player poule 1 against player poule 2 etc.
- Use no more than the amount of players given in number_of_players. If there are more players than the number_of_players we can use the first x players in the playoff equal betwween poules.
         
          
11111111111111111       

 fill in the team id from the df where for example 'player1': 1 is player position 1 from the df            
             
              
 '''