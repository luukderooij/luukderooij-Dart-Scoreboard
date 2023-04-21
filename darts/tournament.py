import logging
import datetime
import random

from darts.dartdb import dartDB
from darts.players import Players
from darts import settings

logger = logging.getLogger(__name__)

class Tournament:
    def __init__(self):
        self.table = "tournament"

    def create(self, name, players, pools=None, playoffs_rounds=None, boards=None):
        self.name = name
        self.players = players
        self.pools = pools
        self.playoffs_rounds = playoffs_rounds
        self.boards = boards

        # If None are given set default of 1.
        if self.pools == None:
            self.pools = 1
        if self.playoffs_rounds == None:
            self.playoffs_rounds = 1
        if self.boards == None:
            self.boards = 1

        number_of_players = len(self.players)

        if number_of_players > self.pools * 7:
            raise ValueError(f'Too many players ({number_of_players}) for {self.pools} poule(s)! Use max 7 players per poule.')

        # Create tournament and add too database.
        self.add_tournament_to_db()

        # Shuffle players list
        random.shuffle(self.players)

        # Divide players per pool
        players_per_pool = number_of_players // self.pools        
        player_in_tournament = []

        poule_unequal = False

        if (number_of_players % 2) != 0 and (self.pools % 2) == 0 or (number_of_players % 2) == 0 and (self.pools % 2) != 0:
            poule_unequal = True
            players_per_poule_unequal = players_per_pool + 1

        #####################################################################
        # Unequal poules and equeal Players does not work!!!!!!! 

        # Create matches for every poule
        for self.pool in range(self.pools):
            self.pool = self.pool + 1
            player_pool_list = []
            for player in self.players:
                if player not in player_in_tournament:
                    player_in_tournament.append(player)
                    player_pool_list.append(player)
                    if poule_unequal == True: 
                        if len(player_pool_list) == players_per_poule_unequal and self.pool == 1:
                            break
                        elif len(player_pool_list) == players_per_pool and self.pool != 1:
                            break
                    elif len(player_pool_list) == players_per_pool:
                        break
                        
            self.create_matches(player_pool_list)

    def add_tournament_to_db(self):
        date_time = datetime.datetime.now()
        sql_ = f"INSERT INTO tournament VALUES (NULL, :tournament_name, :number_of_pools, :playoffs_rounds, :boards, :date)"
        par_ = {"tournament_name": self.name,
                "number_of_pools": self.pools,
                "playoffs_rounds": self.playoffs_rounds,
                "boards": self.boards,
                "date": date_time}
        try:
            with dartDB(settings.DB_FILE) as db:
                self.tournament_id = db.execute(sql_, par_)
            logger.info(f'Tournament created! Tournament name: {self.name}, Number of poules: {self.pools}, Datetime: {date_time}, Tournament ID: {self.tournament_id}')
        except:
            logger.error('Something went wrong with creating a tournament!')

    def create_matches(self, players):
        # Number of players
        number_of_players = len(players)

        # Check of too many or too few players.
        if number_of_players < 2:
            raise ValueError('Not enough players!')
        elif number_of_players > 7:
            raise ValueError("Too many players!")
        
        if number_of_players < 6 and self.boards > 1:
            raise ValueError(f"Too many boards for {number_of_players} players! 6 Players needed for 2 boards.")

        # Random list
        random.shuffle(players)

        # Create round-robin top side list.
        top_players = players[:len(players)//2]

        # Add emty spot by odd players.
        if (number_of_players % 2) != 0:
            top_players.append("EMPTY")
            number_of_players = number_of_players + 1

        # Create round-robin bottom side list.
        bottom_players = players[len(players)//2:]
        bottom_players.reverse()

        # Create matches and save in list
        match_number = 1
        self.matches = []

        for match in range(number_of_players - 1):
            for top_player in top_players:
                position = top_players.index(top_player)
                bottom_player = bottom_players[position]
            
                if top_player != "EMPTY" and bottom_player != "EMPTY":
                    list = [top_player, bottom_player]
                    random.shuffle(list)
                    top_player = list[0]
                    bottom_player = list[1]

                    dict = {
                        "match": match_number,
                        "player1": top_player,
                        "player2": bottom_player
                    }

                    self.matches.append(dict)
                    match_number = match_number + 1

            # Rotate players in round-robin.
            top_players.insert(1, bottom_players[0])
            bottom_players.append(top_players[-1])
            top_players.pop()
            bottom_players.pop(0)

        for match in self.matches:
            for key, value in match.items():
                if key == "match":
                    match = value
                if key == "player1":
                    player1 = value
                if key == "player2":
                    player2 = value

            sql_ = """INSERT INTO match VALUES (:date, :pool,
                    :match, :player1, :score1, :player2, :score2, 
                    :referee, :tournament_id, :board)"""
            par_ = {"date": datetime.datetime.now(),
                    "pool": self.pool,
                    "match": match,
                    "player1": player1,
                    "score1": 0,
                    "player2": player2,
                    "score2": 0,
                    "referee": "",
                    "board": 1,
                    "tournament_id": self.tournament_id}

            with dartDB(settings.DB_FILE) as db:
                db.execute(sql_, par_)  
                
            self.set_boards()  
        self.set_referee()  

    def set_referee(self):
        with dartDB(settings.DB_FILE) as db:  
            sql_ = "SELECT * FROM tournament WHERE id = :id"
            par_ = {"id": self.tournament_id}
            tournament_data = db.fetchall(sql_, par_)

            sql_ = "SELECT * FROM match WHERE tournament_id = :id"
            par_ = {"id": self.tournament_id}
            matches_data = db.fetchall(sql_, par_)   
       
        for value in tournament_data:
            pools = value[2]
            boards = value[4]

        for pool in range(pools):
            pool = pool + 1
            referee_dict = {}
            temp_dict = {}

            # Filter pool.
            pool_data = list(filter(lambda x: x[1] == pool, matches_data))

            # Get players in pool.
            for match in pool_data:
                if match[3] not in referee_dict:
                    referee_dict[match[3]] = 0
                if match[5] not in referee_dict:
                    referee_dict[match[5]] = 0
                        
            index = 0
            last_referee = None

            # Remove playing players and select referee who did least.
            for match in pool_data:
                if len(referee_dict) == 2: 
                    referee = "Je Moeder!"
                else:
                    temp_dict.update(referee_dict)
                    temp_dict.pop(match[3])
                    temp_dict.pop(match[5])

                    # If more boards then pools players cant referee on other board when playing.
                    if boards > pools:
                        # Check if board is 1 
                        if match[9] == 1:
                            try:
                                next_match = pool_data[index + 1]
                                temp_dict.pop(next_match[3])
                                temp_dict.pop(next_match[5])
                            except:
                                pass
                        # check if board is 2 
                        if match[9] == 2:
                            try:
                                next_match = pool_data[index - 1]
                                temp_dict.pop(next_match[3])
                                temp_dict.pop(next_match[5])
                            except:
                                pass                    

                    index = index + 1

                    referee = min(temp_dict, key=temp_dict.get)
    
                    if referee == last_referee: 
                        temp_dict.pop(referee)
                        referee = min(temp_dict, key=temp_dict.get)

                    last_referee = referee
        
                    temp_dict.clear()     
                    referee_dict[referee] += 1 

                with dartDB(settings.DB_FILE) as db:
                    sql_ = """UPDATE match SET referee = :referee 
                                WHERE tournament_id = :tournament_id AND 
                                pool = :pool AND match = :match"""
                    par_ = {"tournament_id": self.tournament_id,
                            "pool": pool,
                            "match": int(match[2]),
                            "referee": referee}
                    db.execute(sql_, par_)


    # Method for settings wich board to play.
    def set_boards(self):
        with dartDB(settings.DB_FILE) as db:  
            sql_ = "SELECT * FROM tournament WHERE id = :id"
            par_ = {"id": self.tournament_id}
            tournament_data = db.fetchall(sql_, par_)

            sql_ = "SELECT * FROM match WHERE tournament_id = :id"
            par_ = {"id": self.tournament_id}
            matches_data = db.fetchall(sql_, par_)   

        for value in tournament_data:
            pools = value[2]
            boards = value[4]

        matches = len(matches_data)
        
        for match in range(matches):
            pass

        board = 1 
        # Set which match plays on which board when more boards than pools.
        if pools < boards:
            for match in range(matches):
                match = match + 1
                with dartDB(settings.DB_FILE) as db:  
                    sql_ = "update match SET board = :board WHERE match == :match"
                    par_ = {"match": match, "board": board}
                    db.execute(sql_, par_)
  
                board = board + 1
                if board > boards:
                    board = 1

        # Set which match plays on wichh board when pools en boards equal.
        if pools == boards:
            for pool in range(int(pools)):
                pool = pool + 1

                with dartDB(settings.DB_FILE) as db:  
                    sql_ = "update match SET board = :board WHERE pool == :pool"
                    par_ = {"pool": pool, "board": pool}
                    db.execute(sql_, par_)

    # Get tournament latest id.
    def get_latest_tournament_id(self):
        sql_ = "SELECT MAX(id) FROM tournament"
        par_ = {}
        with dartDB(settings.DB_FILE) as db:
            tournament_id = db.fetchone(sql_, par_)
        tournament_id = tournament_id[0]

        return tournament_id

    # Get tournament info data.
    def get_tournament_info_data(self, tournament_id):
        sql_ = "SELECT rowid, * from tournament WHERE id = :id"
        par_ = {"id": tournament_id}
        with dartDB(settings.DB_FILE) as db:
            data = db.fetchall(sql_, par_)
        return data

    # Get tournament matches data
    def get_tournament_matches_data(self, tournament_id, pool=None):
        if pool != None:
            sql_ = "SELECT * FROM match WHERE tournament_id = :id AND pool = :pool"
            par_ = {"id": tournament_id, "pool": pool}             
        else:
            sql_ = "SELECT * FROM match WHERE tournament_id = :id"
            par_ = {"id": tournament_id}
        
        with dartDB(settings.DB_FILE) as db:
            data = db.fetchall(sql_, par_)
        return data  

    # Update matches
    def update_matches(self, score1, score2, tournament_id, pool_id, match_id):
            sql_ = """UPDATE match SET score1 = :score1, score2 = :score2 
                        WHERE tournament_id = :tournament_id AND 
                        pool = :pool_id AND match = :match"""
            par_ = {"score1": score1, 
                    "score2": score2, 
                    "tournament_id": tournament_id,
                    "pool_id": pool_id,
                    "match": match_id}
            with dartDB(settings.DB_FILE) as db:
                db.execute(sql_, par_)

            self.create_standings(tournament_id)
            

    # delete tournament
    def delete_tournament(self, tournament_id):
        sql_ = "DELETE FROM tournament WHERE rowid = :id"
        par_ = {"id": tournament_id} 
        with dartDB(settings.DB_FILE) as db:
            db.execute(sql_, par_)    

    # Get players in tournament
    def get_tournament_players(self, tournament_id, pool=None):
        players = []
        if pool != None:
            sql_ = "SELECT * FROM match WHERE tournament_id = :id AND pool = :pool"
            par_ = {"id": tournament_id, "pool": pool}             
        else:
            sql_ = "SELECT * FROM match WHERE tournament_id = :id"
            par_ = {"id": tournament_id}
        with dartDB(settings.DB_FILE) as db:
            data = db.fetchall(sql_, par_)

        for match in data:
            if match[3] not in players:
                players.append(match[3])
            if match[5] not in players:
                players.append(match[5])

        return players

    def get_standings(self, ID):
        sql_ = "SELECT * FROM standings WHERE tournament_id = :id"
        par_ = {"id": ID}
        with dartDB(settings.DB_FILE) as db:
            standings = db.fetchall(sql_, par_)
        standings = sorted(standings, key=lambda standings: (standings[1], standings[2] ))

        return standings

    # Check if all tournament matches are played
    def are_all_machtes_played(self, ID):
        data = self.get_tournament_matches_data(ID)
        all_played = True
        for match in data:
            if match[4] == 0 and match[6] == 0:
                all_played = False
                break
        return all_played

    # calculate score
    def create_standings(self, tournament_id):
        tournament_data = self.get_tournament_info_data(tournament_id)
        poules = int(tournament_data[0][3])

        for poule in range(poules):
            poule = poule + 1
            matches_data = self.get_tournament_matches_data(tournament_id, poule)
            players = self.get_tournament_players(tournament_id, poule)

            standings_list = []
            all_players = []

            for player in players: 
                all_players.append(player)
    
                matches_played = 0
                matches_won = 0
                matches_lost = 0 
                legs_scored = 0 
                legs_against = 0

                for match in matches_data:
                    if player == match[3]:
                        if match[4] > 0 or match[6] > 0:
                            # Add played match to count.
                            matches_played = matches_played + 1
                            # Check if won or lost.
                            if match[4] > match[6]:
                                matches_won = matches_won + 1
                            else:
                                matches_lost = matches_lost + 1
                            # Count legs won and lost
                            legs_scored = legs_scored + match[4]
                            legs_against = legs_against + match[6]
                    if player == match[5]:
                        if match[4] > 0 or match[6] > 0:
                            # Add played match to count.
                            matches_played = matches_played + 1
                            # Check if won or lost.
                            if match[6] > match[4]:
                                matches_won = matches_won + 1
                            else:
                                matches_lost = matches_lost + 1
                            # Count legs won and lost
                            legs_scored = legs_scored + match[6]
                            legs_against = legs_against + match[4]

                legs_difference = legs_scored - legs_against

                standings_list.append(tuple((tournament_id, player, matches_played, matches_won, matches_lost, legs_scored, legs_against, legs_difference)))
            
            # Change order from first to last. 1: matches_won, 2: legs_difference, 3: legs_scored.
            standings_list = sorted(standings_list, reverse=True, key=lambda standings_list: (standings_list[3], standings_list[7], standings_list[5]))

            # This hurts my soul and looks for mutual result and gives player a position.
            number_of_players = int(len(players))

            for number in range(number_of_players):
                position = number + 1
                player = standings_list[number]
                player_name = player[1]

                for opponent in standings_list:
                    nemesis_name = opponent[1]
                    # Skip urself.
                    if player_name != nemesis_name:
                        # Checks if matches_won, legs_difference and legs_scored are equal.
                        if player[3] == opponent[3] and player[7] == opponent[7] and player[5] == opponent[5]:
                            for match in matches_data:
                                if match[3] == player_name and match[5] == nemesis_name:
                                    if match[4] > match[6] and all_players.index(player_name) > all_players.index(nemesis_name):
                                        position = position - 1
                                    if match[4] < match[6] and all_players.index(player_name) < all_players.index(nemesis_name):
                                        position = position + 1
                                if match[3] == nemesis_name and match[5] == player_name:
                                    if match[4] < match[6] and all_players.index(player_name) > all_players.index(nemesis_name):
                                        position = position - 1
                                    if match[4] > match[6] and all_players.index(player_name) < all_players.index(nemesis_name):
                                        position = position + 1

                matches_played = player[2]
                matches_won = player[3]
                matches_lost = player[4]
                legs_scored = player[5]
                legs_against = player[6]
                legs_difference = player[7]

                data = None

                sql_ = "SELECT rowid, * FROM standings WHERE tournament_id = :tournament_id AND player_name = :player_name"
                par_ = {"tournament_id": tournament_id, "player_name":player_name}

                with dartDB(settings.DB_FILE) as db:
                    data = db.fetchall(sql_, par_)

                    if not data:
                        sql_ = """INSERT INTO standings VALUES (:tournament_id, :poule, :place, :player_name, 
                                  :matches_played, :matches_won, :matches_lost, :legs_scored, :legs_against, :legs_difference)"""
                        par_ = {"tournament_id": tournament_id,
                                "poule": poule,
                                "place": position,
                                "player_name": player_name,
                                "matches_played": matches_played,
                                "matches_won": matches_won,
                                "matches_lost": matches_lost,
                                "legs_scored": legs_scored,
                                "legs_against": legs_against,
                                "legs_difference": legs_difference} 
                    else:
                        sql_ = """UPDATE standings SET place = :place, matches_played = :matches_played, matches_won = :matches_won, 
                                matches_lost = :matches_lost, legs_scored = :legs_scored, legs_against = :legs_against, legs_difference = :legs_difference
                                WHERE tournament_id = :tournament_id AND player_name = :player_name"""
                        par_ = {"tournament_id": tournament_id,
                                "place": position,
                                "player_name": player_name,
                                "matches_played": matches_played,
                                "matches_won": matches_won,
                                "matches_lost": matches_lost,
                                "legs_scored": legs_scored,
                                "legs_against": legs_against,
                                "legs_difference": legs_difference} 
                                
                    db.execute(sql_, par_)


    def api_get_tournament(self, tournament_id):

        with dartDB(settings.DB_FILE) as db:
            sql_ = "SELECT * FROM tournament WHERE id = :id"
            par_ = {"id": tournament_id}
            tournament_data = db.fetchall(sql_, par_)

            sql_ = "SELECT * FROM match WHERE tournament_id = :id"
            par_ = {"id": tournament_id}
            match_data = db.fetchall(sql_, par_)

            sql_ = "SELECT * FROM standings WHERE tournament_id = :id"
            par_ = {"id": tournament_id}
            standings_data = db.fetchall(sql_, par_)

            sql_ = "SELECT * FROM playoffs WHERE tournament_id = :id"
            par_ = {"id": tournament_id}
            playoffs_data = db.fetchall(sql_, par_)

        standings_data = sorted(standings_data, key=lambda standings_data: (standings_data[1], standings_data[2] ))

        # Check number of poules.
        for value in tournament_data:
            tournament_id = int(value[0])
            tournament_name = str(value[1])
            tournament_poules = int(value[2])
            tournament_date = value[5]

        poules = []

        for poule in range(tournament_poules):
            standings = []
            matches = []
            playoffs = []
            poule = poule + 1 

            for standing in standings_data:
                if standing[1] == poule:
                    standings_dict = {"id": standing[2],
                    "pos": standing[2],
                    "name": standing[3],
                    "matches_played": standing[4],
                    "matches_won": standing[5],
                    "matches_lost": standing[6],
                    "legs_scored": standing[7],
                    "legs_against": standing[8],
                    "legs_difference": standing[9]
                    }
                    standings.append(standings_dict)

            for match in match_data:
                if match[1] == poule:
                    match_dict = {"id": match[2],
                    "player_1": match[3],
                    "score_1": match[4],
                    "score_2": match[6],
                    "player_2": match[5],
                    "referee": match[7],
                    "board": match[9]
                    }
                    matches.append(match_dict)
        
            poules_info = {"id": poule,
            "standings": standings,
            "matches":  matches
            }
            poules.append(poules_info)

        if playoffs_data:
            playoffs_rounds = int(playoffs_data[0][1])
            id = 1
            for round in range(playoffs_rounds,-1,-1):
                matches = []
                if round == 0:
                    break
                match_id = 1
                for match in playoffs_data:
                    if match[1] == round:
                        match_dict = {
                            "id": match_id, 
                            "round": match[1],
                            "match": match[2],
                            "board": match[3],
                            "player_1": match[4],
                            "score_1": match[5],
                            "score_2": match[7],
                            "player_2": match[6],
                            "referee": match[8]
                        }
                        matches.append(match_dict)
                        match_id = match_id + 1

                if matches:        
                    playoffs_dict = {
                        "id": id,
                        "round": round,
                        "matches": matches 
                    }
                    playoffs.append(playoffs_dict)

                id = id + 1
           

        tournament_info = {"id": tournament_id,
        "name": tournament_name, 
        "date" : tournament_date,
        "poules": poules,
        "playoffs": playoffs
        }

        tournament = []
        tournament.append(tournament_info)
        tournaments = {"tournaments": tournament}
    
        return tournaments


    def api_get_matches(self, tournament_id):
        with dartDB(settings.DB_FILE) as db:
            sql_ = "SELECT * FROM match WHERE tournament_id = :id"
            par_ = {"id": tournament_id}
            match_data = db.fetchall(sql_, par_)

        matches = []

        for match in match_data:
            match_dict = {"tournament_id": tournament_id,
            "pool": match[1],
            "match_id": match[2],
            "player_1": match[3],
            "score_1": match[4],
            "score_2": match[6],
            "player_2": match[5],
            "referee": match[7],
            "board": match[9]
            }

            matches.append(match_dict)

        return matches

    def api_get_tournament_standings(self, tournament_id):
        with dartDB(settings.DB_FILE) as db:
            sql_ = "SELECT * FROM standings WHERE tournament_id = :id"
            par_ = {"id": tournament_id}
            standings_data = db.fetchall(sql_, par_)

        standings_data = sorted(standings_data, key=lambda standings_data: (standings_data[1], standings_data[2] ))

        standings = []

        for standing in standings_data:
            standings_dict = {"pool": standing[1],
            "id": standing[2],
            "pos": standing[2],
            "name": standing[3],
            "matches_played": standing[4],
            "matches_won": standing[5],
            "matches_lost": standing[6],
            "legs_scored": standing[7],
            "legs_against": standing[8],
            "legs_difference": standing[9]
            }
            standings.append(standings_dict)

        return standings