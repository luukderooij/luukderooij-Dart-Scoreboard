
import logging

from flask import Blueprint, session, render_template

from darts.tournament import Tournament
from darts.toneighty import TonEighty
from darts.winners import Winners
from darts.finishes import Finishes
from darts.playoffs import Playoffs

logger = logging.getLogger(__name__)

tv = Blueprint('tv', __name__, template_folder='templates', static_folder='static', static_url_path='/static')


@tv.route('/tv/tournament')
@tv.route('/tv/tournament.html')
def tournamenttv():
    SCORE = {}

    TOURNAMENT_ID = Tournament().get_latest_tournament_id()

    try:
        if 'tournament_id' in session: 
            TOURNAMENT_ID = session['tournament_id']
    except:
        logger.info("Getting latest Tournamant ID")
        TOURNAMENT_ID = Tournament().get_latest_tournament_id()
        logger.info(f"Latest Tournament ID: {TOURNAMENT_ID}")


    TOURNAMENT_INFO = Tournament().get_tournament_info_data(TOURNAMENT_ID)
    TOURNAMENT = Tournament().get_tournament_matches_data(TOURNAMENT_ID)
        
    # Create tournament standings
    try:
        Tournament().create_standings(TOURNAMENT_ID)
    except:
        logger.info("Something went wrong in create_standings")
    # Get latest tournament standings
    try:
        TOURNAMENT_STANDINGS = Tournament().get_standings(TOURNAMENT_ID)
    except:
        logger.info("Something went wrong in get_standings")
    # get bracket data from db
    try:
        BRACKET_DATA = Playoffs().bracket_data(TOURNAMENT_ID)
    except:
        logger.info("Something went wrong in bracket_data.")
    # Get winner from bracket data
    try:
        bracket_winner = Playoffs().winner_bracket(TOURNAMENT_ID)
    except:
        bracket_winner = None
        logger.info("Something went wrong in winner_bracket.")  
    return render_template('/tournament.html', matches=TOURNAMENT, 
                                                  info=TOURNAMENT_INFO, 
                                                  score=SCORE, 
                                                  scoreboard=TOURNAMENT_STANDINGS, 
                                                  bracketdata=BRACKET_DATA, 
                                                  bracket_winner = bracket_winner)

@tv.route('/tv/scoreboard')
@tv.route('/tv/scoreboard.html')
def scoreboard():
    return render_template('/scoreboard.html',
                            winners=Winners().sorted(),
                            toneightys=TonEighty().sorted(),
                            finishes=Finishes().sorted())


