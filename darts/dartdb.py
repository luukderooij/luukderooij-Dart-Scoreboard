import os
import sqlite3
import logging
import datetime

from sqlite3 import Error
from datetime import date


logger = logging.getLogger(__name__)
today = date.today()

class dartDB:
    def __init__(self, db_file=None):
        self.conn = None
        self.cursor = None

        if db_file:
            self.open(db_file)


    def open(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
            self.cursor.execute("""PRAGMA foreign_keys = ON""")

        except sqlite3.Error as e:
            logger.info("Error connecting to database!")
            logger.error(e)


    def close(self):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()


    def __enter__(self):
        return self


    def __exit__(self,exc_type,exc_value,traceback):
        self.close()


    def create_tables(self):
        queries = [
            "CREATE TABLE IF NOT EXISTS db (id INTEGER PRIMARY KEY AUTOINCREMENT, version TEXT NOT NULL)",
            "CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT NOT NULL, lastname TEXT NOT NULL, nickname TEXT NOT NULL, arcadename TEXT, name email, date_joined DATE NOT NULL)",
            "CREATE TABLE IF NOT EXISTS onehundredandeighty (id INTEGER PRIMARY KEY AUTOINCREMENT, player_id INTEGER, date DATE NOT NULL, FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE)",
            "CREATE TABLE IF NOT EXISTS winner (id INTEGER PRIMARY KEY AUTOINCREMENT, player_id INTEGER, date DATE NOT NULL, FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE)",
            "CREATE TABLE IF NOT EXISTS finishes (id INTEGER PRIMARY KEY AUTOINCREMENT, player_id INTEGER, score TEXT NOT NULL, combi TEXT NOT NULL, date TEXT NOT NULL,  FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE)",
            "CREATE TABLE IF NOT EXISTS tournament (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, pools INTEGER, playoffs_rounds INTEGER, boards INTEGER, date TEXT NOT NULL)",
            "CREATE TABLE IF NOT EXISTS match (date TEXT NOT NULL, pool INTEGER, match TEXT NOT NULL, player1 TEXT NOT NULL, score1 INTEGER, player2 TEXT NOT NULL, score2 INTEGER, referee TEXT NOT NULL, tournament_id INTEGER, board INTEGER, FOREIGN KEY(tournament_id) REFERENCES tournament(id) ON DELETE CASCADE)",
            "CREATE TABLE IF NOT EXISTS standings (tournament_id INTEGER, poule INTEGER, place INTEGER, player_name TEXT NOT NULL, matches_played INTEGER, matches_won INTEGER, matches_lost INTEGER, legs_scored INTEGER, legs_against INTEGER, legs_difference INTEGER, FOREIGN KEY(tournament_id) REFERENCES tournament(id) ON DELETE CASCADE)",
            "CREATE TABLE IF NOT EXISTS bracketmatches (tournament_id INTEGER, round INTEGER, match INTEGER, board INTEGER, player1 TEXT NOT NULL, score1 INTEGER, player2 TEXT NOT NULL, score2 INTEGER, referee TEXT NOT NULL, date TEXT NOT NULL, FOREIGN KEY(tournament_id) REFERENCES tournament(id) ON DELETE CASCADE)",
            "CREATE TABLE IF NOT EXISTS playoffs (tournament_id INTEGER, round INTEGER, match INTEGER, board INTEGER, player_1 TEXT NOT NULL, score_1 INTEGER, player_2 TEXT NOT NULL, score_2 INTEGER, referee TEXT NOT NULL, date TEXT NOT NULL, FOREIGN KEY(tournament_id) REFERENCES tournament(id) ON DELETE CASCADE)"
        ]

        for querie in queries:
            try:
                self.cursor.execute(querie)
            except Error as e:
                logger.error(e)

########################################################################################
# Algemeen
    def fetchall(self, sql_, par_=None):    
        try:
            self.cursor.execute(sql_, par_)
            data = self.cursor.fetchall()
            return data
        except Error as e:
            logger.error('Something went wrong with "def fetchall"')
            logger.error(f"SQL Command: {sql_}")
            logger.error(f"SQL Parameters: {par_}")
            logger.error(e)

    def fetchone(self, sql_, par_):    
        try:
            self.cursor.execute(sql_, par_)
            data = self.cursor.fetchone()
            return data
        except Error as e:
            logger.error('Something went wrong with "def fetchone"')
            logger.error(f"SQL Command: {sql_}")
            logger.error(f"SQL Parameters: {par_}")
            logger.error(e)

    def execute(self, sql_, par_):
        try:
            self.cursor.execute(sql_, par_)
            data = self.cursor.lastrowid
            return data
        except Error as e:
            logger.error('Something went wrong with "def execute"')
            logger.error(f"SQL Command: {sql_}")
            logger.error(f"SQL Parameters: {par_}")
            logger.error(e)
        
        

#update shizzle may work or not:)
################################################################################################
################################################################################################

    def drop(self):
            table = ""
            self.cursor.execute(f"DROP TABLE {table}")


    def db_version(self):
        data = None
        try:
            self.cursor.execute("SELECT * FROM db ORDER BY id DESC LIMIT 1")
            data = self.cursor.fetchone()
        except Error as e:
            pass 
        return data
    
    def update_db(self):
        data = self.db_version()
        if data == None:
            try:
                sql_ = "INSERT INTO db VALUES (Null, :version)"
                par_ = {"version": "0.1"}
                self.cursor.execute(sql_, par_)
            except Error as e:
                logger.error(e)

        data = self.db_version()

        if data[1] == "0.1":
            columns = [i[1] for i in self.cursor.execute('PRAGMA table_info(players)')]
            if "firstname" not in columns:
                try:
                    self.cursor.execute("""PRAGMA foreign_keys=OFF""") 
                    self.cursor.execute("""CREATE TABLE IF NOT EXISTS players_new (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        firstname TEXT NOT NULL,
                                        lastname TEXT,
                                        nickname TEXT,
                                        arcadename TEXT,
                                        email TEXT,
                                        date_joined DATE NOT NULL
                                        )""")
                    self.cursor.execute("INSERT INTO players_new(id, firstname, date_joined) SELECT id, name, date_joined FROM players")
                    self.cursor.execute("DROP TABLE players")
                    self.cursor.execute("ALTER TABLE players_new RENAME to players")

                    self.conn.commit()




                    sql_ = "INSERT INTO db VALUES (Null, :version)"
                    par_ = {"version": "0.2"}
                    self.cursor.execute(sql_, par_)
                    data = self.db_version()
                except Error as e:
                    logger.error("something went wrong with updating database too version 0.2")
                    logger.error(e)


        if data[1] == "0.2":
            columns = [i[1] for i in self.cursor.execute('PRAGMA table_info(tournament)')]
            if "playoffs_rounds" not in columns:
                try:
                    self.cursor.execute("""PRAGMA foreign_keys=OFF""") 
                    self.cursor.execute("""CREATE TABLE IF NOT EXISTS tournament_new
                                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                         name TEXT NOT NULL, 
                                         pools INTEGER,
                                         playoffs_rounds INTEGER, 
                                         boards INTEGER, 
                                         date TEXT NOT NULL)""")
                
                    self.cursor.execute("INSERT INTO tournament_new(id, name, pools, date) SELECT id, name, pools, date FROM tournament")
                    self.cursor.execute("DROP TABLE tournament")
                    self.cursor.execute("ALTER TABLE tournament_new RENAME to tournament")

                    self.conn.commit()

                    sql_ = "INSERT INTO db VALUES (Null, :version)"
                    par_ = {"version": "0.3"}
                    self.cursor.execute(sql_, par_)
                    data = self.db_version()
                except Error as e:
                    logger.error("something went wrong with updating database too version 0.2")
                    logger.error(e)
            else:
                    sql_ = "INSERT INTO db VALUES (Null, :version)"
                    par_ = {"version": "0.3"}
                    self.cursor.execute(sql_, par_)
                    data = self.db_version()




        return data[1]




