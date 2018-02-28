from simple import SimpleBob


def get_character_list():
    return [
        'Hikaru',
        'Khadath',
        'Simple Bob'
    ]


def character_by_name(name):
    chars = {
        'Simple Bob': SimpleBob()
    }

    if name in chars:
        return chars[name]
    else:
        return None
