from random import randint

from card_logic import Effects
from utils import stacks


class Pair:
    def __init__(self, style, base):
        self.style = style
        self.base = base

    @property
    def priority(self):
        return self.style.priority + self.base.priority

    @property
    def atk_range(self):
        distances = []
        for style_dist in self.style.atk_range_options:
            for base_dist in self.base.atk_range_options:
                if style_dist is None or base_dist is None:
                    return None
                distances.append(style_dist + base_dist)
        return sorted(set(distances))

    @property
    def power(self):
        if self.style.power is None or self.base.power is None:
            return 0
        else:
            return self.style.power + self.base.power

    @property
    def modifiers(self):
        mods = []
        for sm in self.style.effects.modifiers:
            mods.append(sm)
        for bm in self.base.effects.modifiers:
            mods.append(bm)
        return mods

    def get_effects(self, trigger):
        effs = []
        for st in self.style.effects.triggers:
            if st.name == trigger:
                effs.append(st.effects)
        for bt in self.base.effects.triggers:
            if bt.name == trigger:
                effs.append(bt.effects)
        return effs

    def __str__(self):
        return self.style.name + ' ' + self.base.name


class Finisher:
    def __init__(self, name, atk_range, power, priority,
                 effects=Effects()):
        self.name = name
        instance_or_none = isinstance(atk_range, list) or atk_range is None
        self.atk_range = atk_range if instance_or_none else [atk_range]
        self.power = power
        self.priority = priority
        self.effects = effects

    @property
    def modifiers(self):
        mods = []
        for m in self.effects.modifiers:
            mods.append(m)
        return mods

    def get_effects(self, trigger):
        effs = []
        for t in self.effects.triggers:
            if t.name == trigger:
                effs.append(t)
        return effs

    def __str__(self):
        return self.name
