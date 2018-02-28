from card_logic import Effects


class Style:
    def __init__(self, name, color, attk_range, power, priority,
                 effects=Effects()):
        self.name = name
        self.color = color
        self.attk_range = attk_range
        self.power = power
        self.priority = priority
        self.effects = effects


class Base:
    def __init__(self, name, attk_range, power, priority,
                 effects=Effects()):
        self.name = name
        self.attk_range = attk_range
        self.power = power
        self.priority = priority
        self.effects = effects
