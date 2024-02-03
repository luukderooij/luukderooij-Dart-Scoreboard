
import os
from datetime import datetime
from flask import Flask


from darts.gui.main.routes import main
from darts.gui.api.routes import api
from darts.gui.tv.routes import tv

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
app.config['JSON_SORT_KEYS'] = False

app.register_blueprint(main)
app.register_blueprint(api)
app.register_blueprint(tv)

@app.template_filter()
def format_datetime(value, format="%d-%m-%Y"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    date = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
    if value is None:
        return ""
    return datetime.strftime(date, format)