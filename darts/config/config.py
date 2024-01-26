import os
import configparser

from darts.config import settings


class Configuration:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def check_section(self, section):
        if not section in self.config:
            self.config.add_section(section)

    def check_key_str(self, section, key, default_value):
        try:
            return self.config.get(section, key)
        except:
            self.config.set(section, key, default_value)
            return default_value

    def check_key_int(self, section, key, default_value):
        try:
            return self.config.getint(section, key)
        except:
            self.config.set(section, key, str(default_value))
            return default_value

    def check_key_bool(self, section, key, default_value):
        try:
            return self.config.getboolean(section, key)
        except:
            self.config.set(section, key, str(default_value))
            return default_value   
        
    def initialize(self):
        sections = {
            'General',
            'Database',
            'Logger'
        }

        for section in sections:
            self.check_section(section)

        settings.WEB_HOST = self.check_key_str('General', 'web_host', '0.0.0.0')
        settings.WEB_PORT = self.check_key_int('General', 'web_port', 80)
        settings.DEVELOPMENT = self.check_key_bool('General', 'development', False)

        settings.LOG_FILE = self.check_key_str('Logger', 'log_file', os.path.join(settings.DATA_DIR, "darts.log"))
        settings.DB_FILE = self.check_key_str('Database', 'db_file',  os.path.join(settings.DATA_DIR, "darts.db"))

        with open(self.config_file, 'w') as file:
            self.config.write(file)


 