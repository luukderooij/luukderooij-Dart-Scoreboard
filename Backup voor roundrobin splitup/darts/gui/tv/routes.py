
import logging

from flask import Blueprint, session, render_template



logger = logging.getLogger(__name__)

tv = Blueprint('tv', __name__, template_folder='tv-templates', static_folder='static', static_url_path='/tv/static')



@tv.route('/tv/test')
def test():
     return render_template('/test.html')