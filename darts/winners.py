import logging
import datetime

from darts.config.dartdb import dartDB
from darts.players import Players
from darts.config import settings

logger = logging.getLogger(__name__)

class Winners:
    def __init__(self):
        self.table = "winner"
    
    def add(self, player_id):
        # Checks if Player id exist in database.
        if Players().check_id(player_id) == None:
            logger.info(f"Player ID {player_id} does not exist! Cannot add a win too the database.")
        else:
            sql_ = f"INSERT INTO {self.table} VALUES (NULL, :player_id, :date)"
            par_ = {"player_id": player_id, "date": datetime.datetime.now()}
            with dartDB(settings.DB_FILE) as db:
                db.execute(sql_, par_)

    def fetchall(self):
        sql_ = f"SELECT * FROM {self.table}"
        par_ = {}  
        with dartDB(settings.DB_FILE) as db:
            data = db.fetchall(sql_, par_)
       
        winners = []
        players = Players().fetchall()

        for win in data:
            for player in players:
                if player["id"] == win[1]:
                    player_id = player["id"]
                    firstname = player["firstname"]
                    lastname = player["lastname"]
                    nickname = player["nickname"]
                    arcadename = player["arcadename"]

            dictionary = {"id": int(win[0]),
                         "player_id": int(player_id),
                         "firstname": firstname,
                         "lastname": lastname,
                         "nickname": nickname,
                         "arcadename": arcadename,
                         "date": str(win[2])}
            winners.append(dictionary)
        return winners                

    def remove(self, id):
        print('hier remove winners')
        sql_ = f"DELETE FROM {self.table} WHERE id = :id"
        par_ = {"id": id}
        with dartDB(settings.DB_FILE) as db:           
            db.execute(sql_, par_)        

    def sorted(self):
        players = Players().fetchall()
        wins = self.fetchall()
        winners = []

        for player in players:
            wins_per_player = [item for item in wins if item["player_id"] == player["id"]]
            if wins_per_player:
                date_list = []
                for win in wins_per_player:
                    date_list.append(win["date"])
            
                dictionary = {"firstname": player["firstname"],
                            "lastname": player["lastname"],
                            "nickname": player["nickname"],
                            "arcadename": player["arcadename"],
                            "score": len(wins_per_player),
                            "last_date": max(date_list)}

                winners.append(dictionary)

        winners.sort(reverse=True, key=lambda x:int(x["score"]))

        # Give dict a id.
        new_winners = []
        id_count = 1 

        for old_dict in winners:
            dictionary = {"id": id_count}
            dictionary.update(old_dict)
            new_winners.append(dictionary)
            id_count = id_count + 1

        return new_winners