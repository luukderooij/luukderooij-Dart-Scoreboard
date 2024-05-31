
import logging
import datetime
import random
import pandas as pd
from time import sleep

from darts.config.dartdb import dartDB
from darts.config import settings

logger = logging.getLogger(__name__)

class RoundRobin:
    def __init__(self):
        pass

           
    def create_matches(self, tournament_id, poule, teams):
        team_ids = [team[0] for team in teams]

        # Number of teams
        number_of_teams = len(teams)


        # Create round-robin top side list.
        top_teams = team_ids[:len(team_ids)//2]

        # Add emty spot by odd players.
        if (number_of_teams % 2) != 0:
            top_teams.append("EMPTY")
            number_of_teams = number_of_teams + 1

        # Create round-robin bottom side list.
        bottom_teams = team_ids[len(team_ids)//2:]
        bottom_teams.reverse()

        # Create matches and save in list
        match_number = 1
        matches = []

        for _ in range(number_of_teams - 1):
            for top_team in top_teams:
                postion = top_teams.index(top_team)
                bottom_team = bottom_teams[postion]

                if top_team != "EMPTY" and bottom_team != "EMPTY":
                    matches.append({"match": match_number, "team1": top_team, "team2": bottom_team})
                    match_number = match_number + 1

            # Rotate teams in round-robin
            top_teams.insert(1, bottom_teams[0])
            bottom_teams.append(top_teams[-1])
            top_teams.pop()
            bottom_teams.pop(0)

        for match in matches:
            for key, value in match.items():
                if key == "match":
                    match = value
                if key == "team1":
                    team1 = value
                if key == "team2":
                    team2 = value


            date_created = datetime.datetime.now()
            date_updated = datetime.datetime.now()

            sql_ = """INSERT INTO tournament_round_robin_matches VALUES (NULL, :tournament_id, :poule,
                    :match, :team1, :score1, :team2, :score2, 
                    :referee, :board, :date_created, :date_updated)"""
            par_ = {"tournament_id": tournament_id,
                    "poule": poule,
                    "match": match,
                    "team1": team1,
                    "score1": 0,
                    "team2": team2,
                    "score2": 0,
                    "referee": "",
                    "board": 1,
                    "date_created": date_created,
                    "date_updated": date_updated}


            with dartDB(settings.DB_FILE) as db:
                db.execute(sql_, par_)  

 






        # matches = self.get_tournament_matches_data(tournament_id)
        # match_ids = []
        # # print(matches)
        # for match in matches:
        #     match_id = match[0]
        #     match_ids.append(match_id)

        #     # score1 = random.randint(1, 2)
        #     # score2 = random.randint(0, 2)
        #     # while score1 == score2:
        #     #     score2 = random.randint(0, 2)

        #     # score1 = 1
        #     # score2 = 2
        #     # self.update_match(tournament_id, match_id, score1, score2)
        # a = 0
        # for id in match_ids:
        #     a = a + 1
        #     if a == 1:
        #         self.update_match(tournament_id, id, 1, 2)
        #     elif a == 2:
        #         self.update_match(tournament_id, id, 1, 2)
        #     elif a == 3:
        #         self.update_match(tournament_id, id, 1, 2)
        #     elif a == 4:
        #         self.update_match(tournament_id, id, 1, 2)
        #     elif a == 5:
        #         self.update_match(tournament_id, id, 1, 2)
        #     elif a == 6:
        #         self.update_match(tournament_id, id, 1, 2)
        #     elif a == 7:
        #         self.update_match(tournament_id, id, 1, 2)
        #     elif a == 8:
        #         self.update_match(tournament_id, id, 1, 2)  
        #     elif a == 9:
        #         self.update_match(tournament_id, id, 1, 2)
        #     elif a == 10:
        #         self.update_match(tournament_id, id, 1, 2)
        #     elif a == 11:
        #         self.update_match(tournament_id, id, 1, 2)
        #     elif a == 12:
        #         self.update_match(tournament_id, id, 1, 2)
        #     elif a == 13:
        #         self.update_match(tournament_id, id, 1, 2)
        #     elif a == 14:
        #         self.update_match(tournament_id, id, 1, 2)
        #     elif a == 15:
        #         self.update_match(tournament_id, id, 1, 2)

            






















    def create_tournament_standings(self, tournament_id, teams):
        matches = self.get_tournament_matches_data(tournament_id)

        print(matches)

        df = pd.DataFrame(matches, columns=["id", "tournament_id", "poule", "match", "team1", "score1", "team2", "score2", "referee", "board", "date_created", "date_updated"])
        df.drop(["referee", "board", "date_created", "date_updated"], axis=1, inplace=True)
  
        team_standings = pd.DataFrame(columns=["Team ID", "Poule", "Matches Played", "Matches Won", "Matches Lost", "Points Scored", "Points Against", "Points Difference"])

        print(df)
        print(teams)
        
        for team in teams:
            team_id = team[0]
            print(team)
            poule = df.loc[(df["team1"] == team_id) | (df["team2"] == team_id), "poule"].values[0]

            matches_played = df[(df["team1"] == team_id) | (df["team2"] == team_id)].shape[0]

            matches_won = df[((df["team1"] == team_id) & (df["score1"] > df["score2"])) | ((df["team2"] == team_id) & (df["score2"] > df["score1"]))].shape[0]
            matches_lost = df[((df["team1"] == team_id) & (df["score1"] < df["score2"])) | ((df["team2"] == team_id) & (df["score2"] < df["score1"]))].shape[0]
            
            points_scored = df[(df["team1"] == team_id)]["score1"].sum() + df[(df["team2"] == team_id)]["score2"].sum()
            points_against = df[(df["team1"] == team_id)]["score2"].sum() + df[(df["team2"] == team_id)]["score1"].sum()
            points_difference = points_scored - points_against
            
            team_standings = pd.concat([team_standings, pd.DataFrame({"Team ID": [team_id], "Poule": [poule], "Matches Played": [matches_played], "Matches Won": [matches_won], 
                                                                      "Matches Lost": [matches_lost], "Points Scored": [points_scored], 
                                                                      "Points Against": [points_against], "Points Difference": [points_difference]})], 
                                       ignore_index=True)


            team_standings = team_standings.sort_values(by=["Poule", "Matches Won", "Points Difference", "Points Scored"], ascending=[True, False, False, False])

        team_standings.insert(0, "Place", team_standings.groupby("Poule").cumcount() + 1)

        # Check for mutal resluts in standings. and sort the standings accordingly.
        for poule in team_standings['Poule'].unique():
            poule_data = team_standings[team_standings['Poule'] == poule]
            all_duplicate_teams = poule_data[poule_data.duplicated(subset=['Matches Won', 'Points Difference', 'Points Scored'], keep=False)]

            if not all_duplicate_teams.empty:
                for _, group in all_duplicate_teams.groupby(['Matches Won', 'Points Difference', 'Points Scored']):
                    team_ids = group['Team ID'].tolist()
                    points = []
                    for team_id in team_ids:
                        opponent_team_ids = [team for team in team_ids if team != team_id]
                        points.append(0)

                        for opponent_team_id in opponent_team_ids:                            
                            team1_wins = df[(df["team1"] == team_id) & (df["team2"] == opponent_team_id) & (df["score1"] > df["score2"])]
                            team2_wins = df[(df["team1"] == opponent_team_id) & (df["team2"] == team_id) & (df["score1"] < df["score2"])]

                            if not team1_wins.empty or not team2_wins.empty:
                                points[-1] += 1
                                logger.info(f'team_id: {team_id} won from opponent_team_id: {opponent_team_id}')
     
                            team_points_dict = dict(zip(team_ids, points))

                            # Sort team_points_dict by points in descending order
                            sorted_teams = sorted(team_points_dict.items(), key=lambda x: x[1], reverse=True)

                            # Get the team IDs sorted by points
                            sorted_team_ids = [team[0] for team in sorted_teams]
                   
                        # Reorder the DataFrame based on sorted_team_ids
                        team_standings_sorted = team_standings.set_index('Team ID').reindex(sorted_team_ids).reset_index()

                        # Combine the sorted teams with the remaining teams in the original order
                        remaining_teams = team_standings[~team_standings['Team ID'].isin(sorted_team_ids)]
                        team_standings = pd.concat([team_standings_sorted, remaining_teams]).reset_index(drop=True)
        print(team_standings)

        with dartDB(settings.DB_FILE) as db:
            sql_ = "SELECT rowid, * FROM tournament_standings WHERE tournament_id = :tournament_id"
            par_ = {"tournament_id": tournament_id}
            data = db.fetchall(sql_, par_)

        if not data: 
            for index, row in team_standings.iterrows():
                date_created = datetime.datetime.now()
                date_updated = datetime.datetime.now()
                sql_ = """INSERT INTO tournament_standings VALUES (NULL, :tournament_id, :poule, :place, :team_id, :matches_played, :matches_won, :matches_lost, :legs_scored, :legs_against, :legs_difference, :date_created, :date_updated)"""
                par_ = {"tournament_id": tournament_id,
                        "poule": row["Poule"],
                        "place": row["Place"],
                        "team_id": row["Team ID"],
                        "matches_played": row["Matches Played"],
                        "matches_won": row["Matches Won"],
                        "matches_lost": row["Matches Lost"],
                        "legs_scored": row["Points Scored"],
                        "legs_against": row["Points Against"],
                        "legs_difference": row["Points Difference"],
                        "date_created": date_created,
                        "date_updated": date_updated}
                with dartDB(settings.DB_FILE) as db:
                    db.execute(sql_, par_)

        else:
            for index, row in team_standings.iterrows():
                date_updated = datetime.datetime.now()
                sql_ = """UPDATE tournament_standings SET place = :place, matches_played = :matches_played, matches_won = :matches_won, matches_lost = :matches_lost, legs_scored = :legs_scored, legs_against = :legs_against, legs_difference = :legs_difference, date_updated = :date_updated WHERE tournament_id = :tournament_id AND team_id = :team_id"""
                par_ = {"place": row["Place"],
                        "matches_played": row["Matches Played"],
                        "matches_won": row["Matches Won"],
                        "matches_lost": row["Matches Lost"],
                        "legs_scored": row["Points Scored"],
                        "legs_against": row["Points Against"],
                        "legs_difference": row["Points Difference"],
                        "date_updated": date_updated,
                        "tournament_id": tournament_id,
                        "team_id": row["Team ID"]}
                with dartDB(settings.DB_FILE) as db:
                    db.execute(sql_, par_)




    def get_tournament_standings(self, tournament_id):
        with dartDB(settings.DB_FILE) as db:
            sql_ = "SELECT * FROM tournament_standings WHERE tournament_id = :tournament_id"
            par_ = {"tournament_id": tournament_id}
            data = db.fetchall(sql_, par_)
        return data
    



    def get_tournament_matches_data(self, tournament_id):
            # Get matches data from a tournament.
            sql_ = "SELECT * FROM tournament_round_robin_matches WHERE tournament_id = :tournament_id"
            par_ = {"tournament_id": tournament_id}
            with dartDB(settings.DB_FILE) as db:
                data = db.fetchall(sql_, par_)
            return data

    def are_all_matches_played(self, tournament_id):
            # Check if all matches are played.
            sql_ = "SELECT * FROM tournament_round_robin_matches WHERE tournament_id = :tournament_id AND team1_score = 0 AND team2_score = 0"
            par_ = {"tournament_id": tournament_id}
            with dartDB(settings.DB_FILE) as db:
                data = db.fetchall(sql_, par_)
            if data:
                logger.info('Not all matches are played!')
                return False
            else:
                return True
            
   
    def update_match(self, tournament_id, match_id, score1, score2):
        sql_ = "UPDATE tournament_round_robin_matches SET team1_score = :score1, team2_score = :score2 WHERE tournament_id = :tournament_id AND id = :match_id"
        par_ = {"score1": score1, "score2": score2, "tournament_id": tournament_id, "match_id": match_id}
        with dartDB(settings.DB_FILE) as db:
            data = db.execute(sql_, par_)


        return data