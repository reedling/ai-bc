class UserAgent:
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
