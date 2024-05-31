import logging
import datetime
import random
import pandas as pd
from time import sleep

from darts.config.dartdb import dartDB
from darts.config import settings

logger = logging.getLogger(__name__)

class Playoffs:
    def __init__(self):
        pass

    def create_playoffs(self, rounds=1):

        print(rounds)
        """
        Create a playoffs tournament
        """
        pass