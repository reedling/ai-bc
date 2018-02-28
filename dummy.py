from card import Style, Base

class Dummy:
    def __init__(self):
        self.styles = [Style('Contumacious', 'gray', 0, 0, 0) for i in range(5)]
        self.bases = [Base('Posture', 0, 0, 0) for i in range(7)]

class DummyAgent:
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
