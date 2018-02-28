from card import Style, Base
from utils import get_standard_bases


class SimpleBob:
    def __init__(self):
        self.styles = [
            Style('Plain', 'gray', 0, 0, 0) for i in range(5)
        ]
        self.bases = get_standard_bases()
