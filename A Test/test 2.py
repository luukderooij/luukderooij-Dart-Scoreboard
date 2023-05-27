'''
Create Tournament

Inputs
- Players (Playerid, Firstname, Lastname, Nickname  )
- number op Pools 
- number of playoff rounds
- number of boards

'''
import settings
import os
import datetime
from config import Configuration
from dartdb import dartDB
import logging
import random


settings.DATA_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"Path installation directory:: {settings.DATA_DIR}")

settings.CONFIG_FILE = os.path.join(settings.DATA_DIR, "config.ini")
print(f"Path confg.ini: {settings.CONFIG_FILE}")


Configuration(settings.CONFIG_FILE).initialize()


logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler = logging.FileHandler(settings.LOG_FILE)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.info('Logger started!')

with dartDB(settings.DB_FILE) as db:
    db.create_tables()



class Tournament:
    '''
    - get_latest_tournament_id()
    - get_tournament_info()
    - get_players()
    - create()
    - add_players()
    '''
    def __init__(self, tournament_id=None):
        if tournament_id:
            self.tournament_id = tournament_id
        else:
            self.get_latest_tournament_id()


    def get_latest_tournament_id(self):
        sql_ = "SELECT MAX(Id) FROM Tournament"
        par_ = {}
        with dartDB(settings.DB_FILE) as db:
            tournament_id = db.fetchone(sql_, par_)
        self.tournament_id = tournament_id[0]

        return self.tournament_id


    def get_tournament_info(self):
        if self.tournament_id:
            sql_ = "SELECT * from Tournament WHERE Id = :Id"
            par_ = {"Id": self.tournament_id}
            with dartDB(settings.DB_FILE) as db:
                data = db.fetchone(sql_, par_)
        
        self.tournament_name = data[1]
        self.number_of_pools = data[2]
        self.teams = data[3]
        self.playoffs_rounds = data[4]
        self.number_of_boards = data[5]
        self.winner = data[6]
        self.created_date = data[7]
        
        return data


    def get_players(self):
        if self.tournament_id:
            sql_ = "SELECT * FROM TournamentPlayers WHERE TournamentId = :id"
            par_ = {"id": self.tournament_id}
            with dartDB(settings.DB_FILE) as db:
                data = db.fetchall(sql_, par_)

        else:  
            logger.warning('No tournament id available')
            return

        self.players = data.copy()
        return data


    def create(self, tournament_name, number_of_pools, teams, boards):
        date_time = datetime.datetime.now()
        sql_ = f"INSERT INTO tournament VALUES (NULL, :Name, :Pools, :Teams, :PlayoffsRounds, :Boards, NULL, :CreatedDate)"
        par_ = {"Name": tournament_name,
                "Pools": number_of_pools,
                "Teams": int(teams),
                "PlayoffsRounds": 2,
                "Boards": boards,
                "CreatedDate": date_time}
        
        try:
            with dartDB(settings.DB_FILE) as db:
                self.tournament_id = db.execute(sql_, par_)
            logger.info(f'Tournament created! Tournament name: {tournament_name}, Number of poules: {number_of_pools}, Datetime: {date_time}, Tournament ID: {self.tournament_id}')
        except:
            logger.error('Something went wrong with adding this tournament to the database!')
            raise
        
        self.tournament_info = self.get_tournament_info()
        return self.tournament_info


    def add_players(self, players):
        for player in players:
            firstname = player['first_name']
            lastname = player['last_name']
            nickname = player['nickname']

            sql_ = f"INSERT INTO TournamentPlayers VALUES (NULL, :tournament_id, :player_id, :firstname, :lastname, :nickname)"
            par_ = {"tournament_id": self.tournament_id,
                    "player_id": player['player_id'],
                    "firstname": firstname,
                    "lastname": lastname,       
                    "nickname": nickname}               
    
            try:
                with dartDB(settings.DB_FILE) as db:
                    db.execute(sql_, par_)
                logger.info(f'For tournament {self.tournament_id} added player: {firstname} {nickname} {lastname}.')
            except:
                logger.error('Something went wrong with adding player to the database!')

        self.get_players()





class RoundRobin():
    def __init__(self, tournament_id):
        self.tournament_id = tournament_id


    def create_matches(self, players, tournament_info):
        self.number_of_pools = tournament_info[2]
        self.number_of_boards = tournament_info[5]
        
        # Get player id
        participants = []
        for player in players:
            participants.append(player[0])
        
        # Random list.
        random.shuffle(participants)

        # Number of players.
        number_of_players = len(participants)

        # Check if number of players fit in pool.
        if number_of_players // self.number_of_pools < 2:
            raise ValueError('Not enough players!')
        elif number_of_players // self.number_of_pools > 7:
            raise ValueError("Too many players!")

        # Divide players over the pools.
        pool_sizes = [len(participants) // self.number_of_pools] * self.number_of_pools
        remainder = len(participants) % self.number_of_pools
        for i in range(remainder):
            pool_sizes[i] += 1
        pools = []
        start = 0
        for size in pool_sizes:
            pools.append(participants[start:start+size])
            start += size    
        pool_number = 1
 
        self.matches = []
        # Create mathes for every pool.
        for pool_players in pools:
            self.create_round_robin(pool_players, pool_number)
            pool_number += 1


        for match in self.matches:
            sql_ = f"INSERT INTO RoundRobinMatches VALUES (Null, :TournamentID, :Pool, :Match, :Player1, :Score1, :Player2, :Score2, :Referee, :Board, :CreatedDate, :ModifiedDate)"
            par_ = {"TournamentID": self.tournament_id,
                    "Pool": match['pool'],
                    "Match": match['match'],
                    "Player1": match['player1'],
                    "Score1": 0,
                    "Player2": match['player2'],
                    "Score2": 0,
                    "Referee": None,
                    "Board": None,
                    "CreatedDate": datetime.datetime.now(),
                    "ModifiedDate": None}
            print(match)
            try:
                with dartDB(settings.DB_FILE) as db:
                    db.execute(sql_, par_)
            except:
                logger.error('Something went wrong with adding Matches to the database!')
                raise

    def create_round_robin(self, pool_players, pool_number):
        # Number of players
        number_of_players = len(pool_players)

        # Check if there can be played om multiple boards.        
        if number_of_players < 6 and self.number_of_boards > 1:
            raise ValueError(f"Too many boards selected for {number_of_players} players! 6 Players needed for 2 boards.")

        # Create round-robin top side list.
        top_players = pool_players[:len(pool_players)//2]

        # Create round-robin bottom side list.
        bottom_players = pool_players[len(pool_players)//2:]
        bottom_players.reverse()

        # Fill empty spot 
        if len(top_players) < len(bottom_players):
            top_players.append(0)
        elif len(top_players) > len(bottom_players):
            bottom_players.append(0)

        # Calculate number of matches there need to be played.
        number_of_rounds = (len(top_players) + len(bottom_players)) - 1
        match_number = 1

        for match in range(number_of_rounds):
            for top_player in top_players:
                bottom_player = bottom_players[top_players.index(top_player)]

                if top_player != 0 and bottom_player != 0:    

                    # Random the first and second player!
                    list = [top_player, bottom_player]
                    random.shuffle(list)
                    top_player = list[0]
                    bottom_player = list[1]

                    dict = {
                        "pool": pool_number,
                        "match": match_number,
                        "player1": top_player,
                        "player2": bottom_player}

                    match_number += 1
                    self.matches.append(dict)

            # Rotate players in round-robin.
            top_players.insert(1, bottom_players[0])
            bottom_players.append(top_players[-1])
            top_players.pop()
            bottom_players.pop(0)

                
        










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







players = [    
    {"player_id": 1, "first_name": "Mia", "last_name": "Garcia", "nickname": "MGar"}, 
    {"player_id": 2, "first_name": "Benjamin", "last_name": "Jones", "nickname": "BJon"},
    {"player_id": 3, "first_name": "Evelyn", "last_name": "Moore", "nickname": "EMoo"},    
    {"player_id": 4, "first_name": "James", "last_name": "Rodriguez", "nickname": "JRod"},    
    {"player_id": 5, "first_name": "Isabella", "last_name": "Scott", "nickname": "ISco"},    
    {"player_id": 6, "first_name": "Grace", "last_name": "Anderson", "nickname": "GAnd"},    
    {"player_id": 7, "first_name": "Sophia", "last_name": "White", "nickname": "SWhi"},    
    {"player_id": 8, "first_name": "Oliver", "last_name": "Wilson", "nickname": "OWil"},    
    {"player_id": 9, "first_name": "Alice", "last_name": "Lopez", "nickname": "ALop"},    
    {"player_id": 10, "first_name": "David", "last_name": "Taylor", "nickname": "DTay"},    
    {"player_id": 11, "first_name": "Frank", "last_name": "Davis", "nickname": "FDav"},    
    {"player_id": 12, "first_name": "Charlie", "last_name": "Miller", "nickname": "CMil"},    
    {"player_id": 13, "first_name": "Ava", "last_name": "Johnson", "nickname": "AJoh"},    
    {"player_id": 14, "first_name": "William", "last_name": "Hernandez", "nickname": "WHer"},    
    {"player_id": 15, "first_name": "Jack", "last_name": "Martin", "nickname": "JMar"},    
    {"player_id": 16, "first_name": "Emily", "last_name": "Smith", "nickname": "ESmi"},    
    {"player_id": 17, "first_name": "Noah", "last_name": "Jackson", "nickname": "NJac"},    
    {"player_id": 18, "first_name": "Bob", "last_name": "Lee", "nickname": "BLee"},    
    {"player_id": 19, "first_name": "Henry", "last_name": "Gonzalez", "nickname": "HGon"},    
    {"player_id": 20, "first_name": "Emma", "last_name": "Brown", "nickname": "EBro"}
]


number_of_players = 7
number_of_pools = 2
number_of_boards = 1
teams = False
tournament_name = 'Een Toernooitje'


new_players = players[:number_of_players]

#tournament = Tournament()
tournament = Tournament()

try:
    tournament_info = tournament.create(tournament_name, number_of_pools, teams, number_of_boards)
    tournament.add_players(new_players)
    
    # tournament.create_matches()
    print(tournament.get_tournament_info())

    tournament_id = tournament_info[0]


    participants = tournament.get_players()
  

    roundrobin = RoundRobin(tournament_id)

    roundrobin.create_matches(participants, tournament_info)

    print(participants)







except Exception as e:
    print('error')
    print(e)
        

