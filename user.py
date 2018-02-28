class UserAgent:
    def getAnte(self, info):
        return None

    def setInitialDiscards(self, state):
        return

    def isStunned(self):
        return False

    def getSelection(self, state):
        return Pair('fake-style', 'fake-base')

    def getNewBase(self, state):
        return 'new-fake-base'

    def getStartOfBeatBehavior(self, possibleBehaviors, state):
        return