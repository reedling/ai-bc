from card import Style, Base


class Dummy:
    def __init__(self):
        self.styles = [
            Style('Contumacious', 'gray', 0, 0, 0) for i in range(5)
        ]
        self.bases = [
            Base('Posture', 0, 0, 0) for i in range(7)
        ]


class DummyAgent:
    def get_ante(self, info):
        return None

    def init_discards(self, state):
        return

    @property
    def stunned(self):
        return False

    def get_selection(self, state):
        return Pair('fake-style', 'fake-base')

    def get_new_base(self, state):
        return 'new-fake-base'

    def get_start_of_beat(self, possible_behaviors, state):
        return
