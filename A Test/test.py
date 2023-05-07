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


settings.DATA_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"Path installation directory:: {settings.DATA_DIR}")

settings.CONFIG_FILE = os.path.join(settings.DATA_DIR, "config.ini")
print(f"Path confg.ini: {settings.CONFIG_FILE}")


Configuration(settings.CONFIG_FILE).initialize()


with dartDB(settings.DB_FILE) as db:
    db.create_tables()







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