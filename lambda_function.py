"""
BattleCON AI
POC lambda interface for Alexa Skill
"""

from board import Board
from character_utils import get_character_list
from game import Duel
from player import Player


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '0.1',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def run_game():
    session_attributes = {}
    card_title = 'Welcome'
    speech_output = Duel(
        Player('Simple Bob', True),
        Player('Kallistar', True),
        Board()
    )
    reprompt_text = None
    should_end_session = True
    return build_response(
        session_attributes,
        build_speechlet_response(
            card_title,
            speech_output,
            reprompt_text,
            should_end_session
        )
    )


def on_launch(launch_request, session):
    return run_game()


def lambda_handler(event, context):
    if event['request']['type'] == 'LaunchRequest':
        return on_launch(event['request'], event['session'])
