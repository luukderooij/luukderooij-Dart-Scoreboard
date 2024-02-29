import logging
import datetime

from darts.config.dartdb import dartDB
from darts.config import settings

logger = logging.getLogger(__name__)

class Players:
    # Class to handle players in the database
    # The class will handle the following:
    # 1. Fetching all players
    # 2. Fetching a single player by id
    # 3. Adding a new player
    # 4. Updating a player
    # 5. Removing a player
    # 6. Checking if a player exists by id
    def __init__(self):
        self.table = "players"

    def fetchone(self, id):
        sql_ = f"SELECT * FROM {self.table} WHERE id = :id"
        par_ = {"id": id}        
        with dartDB(settings.DB_FILE) as db:           
            data = db.fetchone(sql_, par_)
        if data:
            player = {"id": int(data[0]),
                        "firstname": str(data[1]),
                        "lastname": str(data[2]),
                        "nickname": str(data[3]),
                        "date_joined": str(data[4]),
                        "date_updated": str(data[5])}
            return player
        else:
            logger.error(f"No player with id: {id} found in database!")
            return None

    def fetchall(self):
        sql_ = f"SELECT * FROM {self.table}"
        par_ = {}    
        with dartDB(settings.DB_FILE) as db:
            data = db.fetchall(sql_, par_)
        if data:
            players = []
            for player_data in data:
                player = {"id": int(player_data[0]),
                        "firstname": str(player_data[1]),
                        "lastname": str(player_data[2]),
                        "nickname": str(player_data[3]),
                        "date_joined": str(player_data[4]),
                        "date_updated": str(player_data[5])}
                players.append(player)
            return players
        else:
            logger.error(f"No players found in database!")
            return None

    def add(self, firstname, lastname, nickname):
        sql_ = f"""INSERT INTO {self.table} VALUES (NULL, :firstname, 
                  :lastname, :nickname, :date_joined, :date_updated)"""
        par_ = {"firstname": firstname,
                "lastname": lastname,
                "nickname": nickname,
                "date_joined": datetime.datetime.now(),
                "date_updated": datetime.datetime.now()}
        with dartDB(settings.DB_FILE) as db:
            db.execute(sql_, par_)

    def update(self, id, firstname, lastname, nickname):
        sql_ = f"""UPDATE {self.table} SET firstname = :firstname, 
            lastname = :lastname, nickname = :nickname, 
            date_updated = :date_updated 
            WHERE id = :id"""
        par_ = {"id": id,
            "firstname": firstname,
            "lastname": lastname,
            "nickname": nickname,
            "date_updated": datetime.datetime.now()}
        with dartDB(settings.DB_FILE) as db:
            print(db.execute(sql_, par_))
        
    def remove(self, id):
        sql_ = f"DELETE FROM {self.table} WHERE id = :id"
        par_ = {"id": id}
        with dartDB(settings.DB_FILE) as db:           
            db.execute(sql_, par_)

    def check_id(self, id):
        sql_ = f"SELECT * FROM {self.table} WHERE id = :id"
        par_ = {"id": id}
        with dartDB(settings.DB_FILE) as db:           
            id = db.fetchone(sql_, par_)
        return id

