from kallistar import Kallistar
from simple import SimpleBob


def get_character_list():
    return [
        'Kallistar',
        'Simple Bob'
    ]


def character_by_name(name):
    chars = {
        'Kallistar': Kallistar(),
        'Simple Bob': SimpleBob()
    }

    if name in chars:
        return chars[name]
    else:
        return None
