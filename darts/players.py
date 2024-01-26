import logging
import datetime

from darts.config.dartdb import dartDB
from darts.config import settings

logger = logging.getLogger(__name__)

class Players:
    def __init__(self):
        self.table = "players"

    def fetchall(self):
        sql_ = f"SELECT * FROM {self.table}"
        par_ = {}    
        with dartDB(settings.DB_FILE) as db:
            data = db.fetchall(sql_, par_)

        if data:
            players = []
            for player in data:
                dictionary = {"id": int(player[0]),
                            "firstname": str(player[1]),
                            "lastname": str(player[2]),
                            "nickname": str(player[3]),
                            "arcadename": str(player[4]),
                            "email": str(player[5]),
                            "date_joined": str(player[6])}
                players.append(dictionary)

            return players
        else:
            logger.error(f"No players found in database!")
            return None

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
                        "arcadename": str(data[4]),
                        "email": str(data[5]),
                        "date_joined": str(data[6])}

            return player
        else:
            logger.error(f"No player with id: {id} found in database!")
            return None

    def add(self, firstname, lastname, nickname, arcadename, email):
        sql_ = f"""INSERT INTO {self.table} VALUES (NULL, :firstname, 
                  :lastname, :nickname, :arcadename, :email, :date_joined)"""
        par_ = {"firstname": firstname,
                "lastname": lastname,
                "nickname": nickname,
                "arcadename": arcadename,
                "email": email,
                "date_joined": datetime.datetime.now()}
        with dartDB(settings.DB_FILE) as db:
            db.execute(sql_, par_)

    def update(self, id, firstname, lastname, nickname, arcadename, email):
        sql_ = f"""UPDATE {self.table} SET firstname = :firstname, 
            lastname = :lastname, nickname = :nickname, 
            arcadename = :arcadename, email = :email 
            WHERE id = :id"""
        par_ = {"id": id,
            "firstname": firstname,
            "lastname": lastname,
            "nickname": nickname,
            "arcadename": arcadename,
            "email": email}
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

    def names(self):
        names = []
        players = self.fetchall()
        for player in players:
            firstname = player["firstname"]
            lastname = player["lastname"]
            name = f"{firstname} {lastname}"
            names.append(name)
        return names

    def nickname(self):
        nicknames = []
        players = self.fetchall()
        for player in players:
            nickname = player["nickname"]
            nicknames.append(nickname)
        return nicknames