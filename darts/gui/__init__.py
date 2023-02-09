
import os
from flask import Flask


from darts.gui.main.routes import main
from darts.gui.api.routes import api

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
app.config['JSON_SORT_KEYS'] = False

app.register_blueprint(main)
app.register_blueprint(api)