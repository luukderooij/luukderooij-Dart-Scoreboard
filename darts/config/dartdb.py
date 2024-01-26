import sqlite3
import logging

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

########################################################################################
# Database create tables
########################################################################################

    def create_tables(self):
        statements = [
            "CREATE TABLE IF NOT EXISTS db (id INTEGER PRIMARY KEY AUTOINCREMENT, version TEXT NOT NULL)",
            "CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT NOT NULL, lastname TEXT NOT NULL, nickname TEXT NOT NULL, arcadename TEXT, date_joined DATE NOT NULL)",
        ]

        for statement in statements:
            try:
                self.cursor.execute(statement)
            except Error as e:
                logger.error(e)

########################################################################################
# Database actions
########################################################################################

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
        
        
