import logging
import datetime

from darts.dartdb import dartDB
from darts.players import Players
from darts import settings


logger = logging.getLogger(__name__)


class Finishes:
    def __init__(self):
        self.table = "finishes"

    def add(self, player_id, score, combi):
        # Checks if Player id exist in database.
        if Players().check_id(player_id) == None:
            logger.info(f"Player ID {player_id} does not exist! Cannot add a finish too the database.")
        else:
            sql_ = f"INSERT INTO {self.table} VALUES (NULL, :player_id, :score, :combi, :date)"
            par_ = {"player_id": player_id,
                    "score": score,
                    "combi": combi, 
                    "date": datetime.datetime.now()}
            with dartDB(settings.DB_FILE) as db:
                db.execute(sql_, par_) 

    def fetchall(self):
        sql_ = f"SELECT * FROM {self.table}"
        par_ = {}  
        with dartDB(settings.DB_FILE) as db:
            data = db.fetchall(sql_, par_)
       
        finishes = []
        players = Players().fetchall()

        for finish in data:
            for player in players:
                if player["id"] == finish[1]:
                    player_id = player["id"]
                    firstname = player["firstname"]
                    lastname = player["lastname"]
                    nickname = player["nickname"]
                    arcadename = player["arcadename"]

            dictionary = {"player_id": int(player_id),
                         "firstname": firstname,
                         "lastname": lastname,
                         "nickname": nickname,
                         "arcadename": arcadename,
                         "score": int(finish[2]),
                         "combi": str(finish[3]),
                         "date": str(finish[4])}
            finishes.append(dictionary)
        return finishes

    def remove(self, id):
        sql_ = f"DELETE FROM {self.table} WHERE id = :id"
        par_ = {"id": id}
        with dartDB(settings.DB_FILE) as db:           
            db.execute(sql_, par_)      

    def sorted(self):
        finishes = self.fetchall()
        finishes.sort(reverse=True, key=lambda x:int(x["score"]))

        # Give dict an id. 
        new_finishes = []
        id_count = 1
        for finish in finishes:
            dictionary = {"id": id_count}
            dictionary.update(finish)
            new_finishes.append(dictionary)
            id_count = id_count + 1

        return new_finishes