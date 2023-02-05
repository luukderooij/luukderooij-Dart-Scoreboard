import logging
import datetime

from darts.dartdb import dartDB
from darts.players import Players
from darts import settings

logger = logging.getLogger(__name__)

class TonEighty:
    def __init__(self):
        self.table = "onehundredandeighty"

    # Add a 180 to database.
    def add(self, player_id):
        # Checks if Player id exist in database.
        if Players().check_id(player_id) == None:
            logger.info(f"Player ID {player_id} does not exist! Cannot add a onehundredandeighty too the database.")
        else:
            sql_ = f"INSERT INTO {self.table} VALUES (NULL, :player_id, :date)"
            par_ = {"player_id": player_id, "date": datetime.datetime.now()}
            with dartDB(settings.DB_FILE) as db:
                db.execute(sql_, par_)        

    # Get al thrown 180s from database.
    def fetchall(self):
        sql_ = f"SELECT * FROM {self.table}"
        par_ = {}  
        with dartDB(settings.DB_FILE) as db:
            data = db.fetchall(sql_, par_)
       
        toneightys = []
        players = Players().fetchall()

        for toneighty in data:
            for player in players:
                if player["id"] == toneighty[1]:
                    player_id = player["id"]
                    firstname = player["firstname"]
                    lastname = player["lastname"]
                    nickname = player["nickname"]
                    arcadename = player["arcadename"]

            dictionary = {"id": int(toneighty[0]),
                         "player_id": int(player_id),
                         "firstname": firstname,
                         "lastname": lastname,
                         "nickname": nickname,
                         "arcadename": arcadename,
                         "date": str(toneighty[2])}
            toneightys.append(dictionary)
        return toneightys

    # Remove a 180 from database.
    def remove(self, id):
        sql_ = f"DELETE FROM {self.table} WHERE id = :id"
        par_ = {"id": id}
        with dartDB(settings.DB_FILE) as db:           
            db.execute(sql_, par_)      

    # Make dictonary list in order for most trown 180s
    def sorted(self):
        players = Players().fetchall()
        toneightys = self.fetchall()
        scored_180 = []
       
        for player in players:
            toneighty_per_player = [item for item in toneightys if item["player_id"] == player["id"]]
            if toneighty_per_player:
                date_list = []
                for toneighty in toneighty_per_player:
                    date_list.append(toneighty["date"])
                
                dictionary = {"firstname": player["firstname"],
                            "lastname": player["lastname"],
                            "nickname": player["nickname"],
                            "arcadename": player["arcadename"],
                            "score": len(toneighty_per_player),
                            "last_date": max(date_list)}

                scored_180.append(dictionary)

        scored_180.sort(reverse=True, key=lambda x:int(x["score"]))

        # Give dict a id.
        new_scored_180 = []
        id_count = 1 

        for old_dict in scored_180:
            dictionary = {"id": id_count}
            dictionary.update(old_dict)
            new_scored_180.append(dictionary)
            id_count = id_count + 1

        return new_scored_180