from random import randint

class Pair:
    def __init__(self, style, base):
        self.style = style
        self.base = base

    @property
    def priority(self):
        return self.style.priority + self.base.priority

    def getEffectsForTrigger(self, trigger):
        triggerEffects = []
        for st in self.style.effects.triggers:
            if st.name == trigger:
                triggerEffects.append(st)
        for bt in self.base.effects.triggers:
            if bt.name == trigger:
                triggerEffects.append(bt)
        return triggerEffects

    def __str__(self):
        return self.style.name + ' ' + self.base.name