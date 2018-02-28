from card_logic import Effects


class Style:
    def __init__(self, name, color, atk_range, power, priority,
                 effects=Effects()):
        self.name = name
        self.color = color
        self.atk_range = atk_range
        self.power = power
        self.priority = priority
        self.effects = effects


class Base:
    def __init__(self, name, atk_range, power, priority,
                 effects=Effects()):
        self.name = name
        self.atk_range = atk_range
        self.power = power
        self.priority = priority
        self.effects = effects
