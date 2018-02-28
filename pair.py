from random import randint


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

    def get_effects(self, trigger):
        effs = []
        for st in self.style.effects.triggers:
            if st.name == trigger:
                effs.append(st)
        for bt in self.base.effects.triggers:
            if bt.name == trigger:
                effs.append(bt)
        return effs

    def __str__(self):
        return self.style.name + ' ' + self.base.name
