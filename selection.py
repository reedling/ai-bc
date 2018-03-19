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
            return None
        else:
            return self.style.power + self.base.power

    @property
    def modifiers(self):
        mods = {}
        for sm in self.style.effects.modifiers:
            if stacks(sm.mtype) and sm.mtype in mods:
                mods[sm.mtype] += sm.val
            else:
                mods[sm.mtype] = sm.val
        for bm in self.base.effects.modifiers:
            if stacks(bm.mtype) and bm.mtype in mods:
                mods[bm.mtype] += bm.val
            else:
                mods[bm.mtype] = bm.val
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
        self.atk_range = atk_range
        self.power = power
        self.priority = priority
        self.effects = effects

    @property
    def atk_range_options(self):
        if not isinstance(self.atk_range, list):
            return [self.atk_range]
        else:
            return self.atk_range

    @property
    def modifiers(self):
        mods = {}
        for m in self.effects.modifiers:
            if stacks(m.mtype) and m.mtype in mods:
                mods[m.mtype] += m.val
            else:
                mods[m.mtype] = m.val
        return mods

    def get_effects(self, trigger):
        effs = []
        for t in self.effects.triggers:
            if t.name == trigger:
                effs.append(t)
        return effs

    def __str__(self):
        return self.name
