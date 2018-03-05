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
    def __init__(self):
        self.blank = True
