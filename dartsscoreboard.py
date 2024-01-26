import os
import logging

from waitress import serve

from darts.config import settings
from darts.config.config import Configuration
from darts.config.dartdb import dartDB

from darts.gui import app


__version__ = "1.0.3"
__date__ = "2023-05-06"


class Darts:
    def __init__(self):
        pass

    def start(self):
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

        if settings.DEVELOPMENT:
            app.run(debug=True, host=settings.WEB_HOST, port=settings.WEB_PORT)
        else:
            serve(app, host=settings.WEB_HOST, port=settings.WEB_PORT)


def main():
    Darts().start()


if __name__ == "__main__":
    main()
