
import os
from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
app.config['JSON_SORT_KEYS'] = False


