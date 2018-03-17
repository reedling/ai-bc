from collections import deque

from card import Style, Base


class Discards:
    def __init__(self, length):
        self.q = deque([[] for x in range(length)], length)

    def discard_inner(self, to_discard):
        if isinstance(to_discard, list):
            self.q[-1].extend(to_discard)
        else:
            self.q[-1].append(to_discard)

    def discard_outer(self, to_discard):
        if isinstance(to_discard, list):
            self.q[0].extend(to_discard)
        else:
            self.q[0].append(to_discard)

    def cycle_out(self):
        to_recover = self.q.popleft()
        self.q.append([])
        return to_recover

    @property
    def styles(self):
        found = []
        for pile in self.q:
            for item in pile:
                if isinstance(item, Style):
                    found.append(item)
        return found

    @property
    def bases(self):
        found = []
        for pile in self.q:
            for item in pile:
                if isinstance(item, Base):
                    found.append(item)
        return found

    @property
    def inner(self):
        discarded = {
            'styles': [],
            'bases': []
        }
        for item in self.q[-1]:
            if isinstance(item, Style):
                discarded['styles'].append(item)
            elif isinstance(item, Base):
                discarded['bases'].append(item)
        return discarded

    @property
    def outer(self):
        discarded = {
            'styles': [],
            'bases': []
        }
        for item in self.q[0]:
            if isinstance(item, Style):
                discarded['styles'].append(item)
            elif isinstance(item, Base):
                discarded['bases'].append(item)
        return discarded
