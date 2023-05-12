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
    def __init__(self, tournament_id=None, tournament_name=None, number_of_pools=None, number_of_boards=None, players=None):
        if tournament_id:
            self.tournament_id = tournament_id
        else:
            self.get_latest_tournament_id()

        if not None in (tournament_name, number_of_pools, number_of_boards):
            self.tournament_name = tournament_name
            self.number_of_pools = number_of_pools
            self.number_of_boards = number_of_boards
        else:
            self.get_latest_tournament_info()

        if players:
            self.players = players
        else:
            self.get_tournament_players()


    # Get tournament latest id.
    def get_latest_tournament_id(self):
        sql_ = "SELECT MAX(id) FROM tournament"
        par_ = {}
        with dartDB(settings.DB_FILE) as db:
            tournament_id = db.fetchone(sql_, par_)
        self.tournament_id = tournament_id[0]

    # Get tournament info.
    def get_latest_tournament_info(self):
        sql_ = "SELECT rowid, * from tournament WHERE id = :id"
        par_ = {"id": self.tournament_id}
        with dartDB(settings.DB_FILE) as db:
            data = db.fetchall(sql_, par_)

    # Get players participating in tournament.
    def get_tournament_players(self):
        sql_ = "SELECT * FROM TournamentPlayers WHERE tournament_id = id"
        par_ = {"id": self.tournament_id}
        with dartDB(settings.DB_FILE) as db:
            data = db.fetchall(sql_, par_)

    # Create Tournament and add to database.
    def create_tournament(self):
        date_time = datetime.datetime.now()
        sql_ = f"INSERT INTO tournament VALUES (NULL, :tournament_name, :number_of_pools, NULL, :boards, :date)"
        par_ = {"tournament_name": self.tournament_name,
                "number_of_pools": self.number_of_pools,
                "boards": self.number_of_pools,
                "date": date_time}
        
        try:
            with dartDB(settings.DB_FILE) as db:
                self.tournament_id = db.execute(sql_, par_)
            logger.info(f'Tournament created! Tournament name: {self.tournament_name}, Number of poules: {self.number_of_pools}, Datetime: {date_time}, Tournament ID: {self.tournament_id}')
        except:
            logger.error('Something went wrong with adding this tournament to the database!')

    # Add Tournament players to database.
    def add_tournament_players(self):
        for player in self.players:
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


    def create_matches(self):
        # Random list.
        all_players = players.copy()
        random.shuffle(all_players)

        # Number of players.
        number_of_players = len(self.players)
            
        # Check if number of players fit in pool.
        if number_of_players // self.number_of_pools < 2:
            raise ValueError('Not enough players!')
        elif number_of_players // self.number_of_pools > 7:
            raise ValueError("Too many players!")
        
        
        print(f'number_of_players {number_of_players}')
        print(f'number of pools: {self.number_of_pools}')
        print(number_of_players // self.number_of_pools)
        print(number_of_players % 2)

        num_pools = self.number_of_pools

        pool_sizes = [len(all_players) // num_pools] * num_pools
        remainder = len(all_players) % num_pools
        for i in range(remainder):
            pool_sizes[i] += 1
        
        pools = []
        start = 0
        for size in pool_sizes:
            pools.append(all_players[start:start+size])
            start += size

        print('hier')
   

        for pool in pools:
            print(pool)










        # Caculate max players per pool.
        num_players_per_pool = number_of_players // self.number_of_pools
        print(num_players_per_pool)

        # Create roundrobin for every pool.
        for pool in range(self.number_of_pools):
            pool_num = pool + 1

            round 







    def create_round_robin(self):
        # Number of players
        number_of_players = len(self.players)

        
        # Check if there can be played om multiple boards.        
        if number_of_players < 6 and self.number_of_boards > 1:
            raise ValueError(f"Too many boards selected for {number_of_players} players! 6 Players needed for 2 boards.")









        # # Create round-robin top side list.
        # top_players = players[:len(players)//2]

        # # Add emty spot by odd players.
        # if (number_of_players % 2) != 0:
        #     top_players.append("EMPTY")
        #     number_of_players = number_of_players + 1

        # # Create round-robin bottom side list.
        # bottom_players = players[len(players)//2:]
        # bottom_players.reverse()

        # # Create matches and save in list
        # match_number = 1
        # self.matches = []

        # for match in range(number_of_players - 1):
        #     for top_player in top_players:
        #         position = top_players.index(top_player)
        #         bottom_player = bottom_players[position]
            
        #         if top_player != "EMPTY" and bottom_player != "EMPTY":
        #             list = [top_player, bottom_player]
        #             random.shuffle(list)
        #             top_player = list[0]
        #             bottom_player = list[1]

        #             dict = {
        #                 "match": match_number,
        #                 "player1": top_player,
        #                 "player2": bottom_player
        #             }

        #             self.matches.append(dict)
        #             match_number = match_number + 1

        #     # Rotate players in round-robin.
        #     top_players.insert(1, bottom_players[0])
        #     bottom_players.append(top_players[-1])
        #     top_players.pop()
        #     bottom_players.pop(0)

        # for match in self.matches:
        #     for key, value in match.items():
        #         if key == "match":
        #             match = value
        #         if key == "player1":
        #             player1 = value
        #         if key == "player2":
        #             player2 = value

        #     sql_ = """INSERT INTO match VALUES (:date, :pool,
        #             :match, :player1, :score1, :player2, :score2, 
        #             :referee, :tournament_id, :board)"""
        #     par_ = {"date": datetime.datetime.now(),
        #             "pool": self.pool,
        #             "match": match,
        #             "player1": player1,
        #             "score1": 0,
        #             "player2": player2,
        #             "score2": 0,
        #             "referee": "",
        #             "board": 1,
        #             "tournament_id": self.tournament_id}

        #     with dartDB(settings.DB_FILE) as db:
        #         db.execute(sql_, par_)  
                
        #     self.set_boards()  
        # self.set_referee()  



players = [
    {"player_id": 1, "first_name": "Bob", "last_name": "Smith", "nickname": "Bobby"},
    {"player_id": 2, "first_name": "Isabella", "last_name": "Brown", "nickname": "Izzy"},
    {"player_id": 3, "first_name": "David", "last_name": "Anderson", "nickname": "Davey"},
    {"player_id": 4, "first_name": "Charlie", "last_name": "Davis", "nickname": "Chuck"},
    {"player_id": 5, "first_name": "Frank", "last_name": "Lee", "nickname": "Frankie"},
    {"player_id": 6, "first_name": "Grace", "last_name": "Wilson", "nickname": "Gracie"},
    {"player_id": 7, "first_name": "Henry", "last_name": "Garcia", "nickname": "Hank"},
    {"player_id": 8, "first_name": "Jack", "last_name": "Johnson", "nickname": "JJ"},
    {"player_id": 9, "first_name": "Alice", "last_name": "Martin", "nickname": "Ally"},
    {"player_id": 10, "first_name": "Emily", "last_name": "Taylor", "nickname": "Em"}
    ]

# players = [
#     {"player_id": 1, "first_name": "Bob", "last_name": "Smith", "nickname": "Bobby"},
#     {"player_id": 2, "first_name": "Isabella", "last_name": "Brown", "nickname": "Izzy"},
#     {"player_id": 3, "first_name": "David", "last_name": "Anderson", "nickname": "Davey"},
#     {"player_id": 4, "first_name": "Charlie", "last_name": "Davis", "nickname": "Chuck"},
#     {"player_id": 5, "first_name": "Frank", "last_name": "Lee", "nickname": "Frankie"},
#     {"player_id": 7, "first_name": "Henry", "last_name": "Garcia", "nickname": "Hank"},
#     {"player_id": 8, "first_name": "Jack", "last_name": "Johnson", "nickname": "JJ"},
#     {"player_id": 6, "first_name": "Grace", "last_name": "Wilson", "nickname": "Gracie"}

#     ]

tournament = Tournament(None, 'Een toernooitje', 1, 2, players)

try:
    tournament.create_tournament()
    tournament.create_matches()
    tournament.add_tournament_players()

except Exception as e:
    print('error')
    print(e)
        

'''
class Tournament:
    def __init__(self, name, num_of_pools, players):
        self.table = "tournament"

        self.name = name
        self.num_of_pools = num_of_pools    
        self.players = players  

        print(f'self.pools: {self.num_of_pools}')
        print(f'self.players: {self.players}')


    def write_players_to_db(self):
        sql_ = f"INSERT INTO tournamentplayers VALUES (tournamentID, :tournament_name, :number_of_pools, :playoffs_rounds, :boards, :date)"
        par_ = {"tournamentID": self.name,
                "firstName": self.num_of_pools,
                "lastName": self.playoffs_rounds,
                "boards": self.boards,
                "date": date_time}


    def write_to_db(self):
        date_time = datetime.datetime.now()
        sql_ = f"INSERT INTO tournament VALUES (NULL, :tournament_name, :number_of_pools, :playoffs_rounds, :boards, :date)"
        par_ = {"tournament_name": self.name,
                "number_of_pools": self.num_of_pools,
                "playoffs_rounds": self.playoffs_rounds,
                "boards": self.boards,
                "date": date_time}
        try:
            with dartDB(settings.DB_FILE) as db:
                self.tournament_id = db.execute(sql_, par_)
            logger.info(f'Tournament created! Tournament name: {self.name}, Number of poules: {self.pools}, Datetime: {date_time}, Tournament ID: {self.tournament_id}')
        except:
            logger.error('Something went wrong with creating a tournament!')






# Prompt the user to enter the number of pools
num_of_pools = int(input("Enter the number of pools: "))

players = [
    {"first_name": "Bob", "last_name": "Smith"},
    {"first_name": "Isabella", "last_name": "Brown"},
    {"first_name": "David", "last_name": "Anderson"},
    {"first_name": "Charlie", "last_name": "Davis"},
    {"first_name": "Frank", "last_name": "Lee"},
    {"first_name": "Grace", "last_name": "Wilson"},
    {"first_name": "Henry", "last_name": "Garcia"},
    {"first_name": "Jack", "last_name": "Johnson"},
    {"first_name": "Alice", "last_name": "Martin"},
    {"first_name": "Emily", "last_name": "Taylor"}  
]

# Create a Playoffs object with the gathered pool data
Tournament = Tournament(num_of_pools, players)


# Generate the playoff schedule
schedule = playoffs.create_schedule()







class Playoffs:
    def __init__(self, *pools):
        self.pools = pools
        self.num_pools = len(self.pools)
        self.players = self.flatten_pools()
        self.num_players = len(self.players)

    def flatten_pools(self):
        flattened_pools = []
        for pool in self.pools:
            flattened_pools += pool
        return flattened_pools

    def create_schedule(self):
        if self.num_players < 2:
            raise ValueError("At least 2 players are required to create a playoff schedule")

        num_rounds = self.calculate_num_rounds()
        schedule = [[] for _ in range(num_rounds)]

        print(f'self.pools: {self.pools}')

        for i, pool in enumerate(self.pools):
            for j, player in enumerate(pool):
                index = i * len(pool) + j
                schedule[0].append((player, index))


        print(f'schedule: {schedule}')

        # for r in range(1, num_rounds):
        #     round_matches = []
        #     for i in range(0, self.num_players, 2):
        #         if i + 1 < self.num_players:
        #             player1, index1 = schedule[r - 1][i]
        #             player2, index2 = schedule[r - 1][i + 1]
        #             match = (player1, player2, index1, index2)
        #             round_matches.append(match)
        #     schedule[r] = round_matches

        # return schedule

    def calculate_num_rounds(self):
        num_matches = self.num_players // 2
        num_rounds = 1
        while num_matches > 0:
            num_rounds += 1
            num_matches //= 2
        return num_rounds







# Prompt the user to enter the number of pools
num_pools = int(input("Enter the number of pools: "))

# Create an empty list to store the pool data
pools = []

# Loop through each pool and gather player data
for i in range(num_pools):
    # Prompt the user to enter the player data for this pool
    player_input = input(f"Enter the player data for pool {i+1} (first name, last name, nickname), separated by commas: ")
    # Split the input into a list of player data
    player_data = player_input.split(",")
    # Add the player data to the pools list
    pools.append(player_data)

# Print the list of pools and players
print("Pools and players:")
for i, pool in enumerate(pools):
    print(f"Pool {i+1}:")
    for player in pool:
        first_name, last_name, nickname = player.split()
        print(f" - {first_name} {last_name} ({nickname})")

pools = [['Luuk', ' Tim', ' Hanny', ' Sjaak'], ['Kobus', ' Patrick', ' Justin'], ['Mark', ' Nick', ' Lvs', ' Rick']]

# Create a Playoffs object with the gathered pool data
playoffs = Playoffs(*pools)

# Generate the playoff schedule
schedule = playoffs.create_schedule()

# Print the schedule
for r, matches in enumerate(schedule):
    print(f"Round {r+1}:")
    for match in matches:
        print(f"{match[0]} vs {match[1]}")
    print()

1

'''