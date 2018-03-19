class Effects:
    def __init__(self, modifiers=[], triggers=[], actions=[], conditionals=[]):
        self.modifiers = modifiers
        self.triggers = triggers
        self.actions = actions
        self.conditionals = conditionals


class Modifier:
    def __init__(self, mtype, val, opponent=False):
        self.mtype = mtype
        self.val = val
        self.opponent = opponent


class Trigger:
    def __init__(self, name, effects=Effects()):
        self.name = name
        self.effects = effects


class Action:
    def __init__(self, atype, opts, conditionals=[]):
        self.atype = atype
        self.opts = opts
        self.conditionals = conditionals

    def get_behaviors(self, atype, magnitude):
        if atype == 'grapple':
            return [
                Behavior('push', magnitude, self.conditionals),
                Behavior('pull', magnitude, self.conditionals),
            ]
        elif atype == 'move':
            return [
                Behavior('advance', magnitude, self.conditionals),
                Behavior('retreat', magnitude, self.conditionals)
            ]
        else:
            return [Behavior(atype, magnitude, self.conditionals)]

    @property
    def behaviors(self):
        behaviors = []
        if isinstance(self.opts, list):
            for opt in self.opts:
                behaviors.extend(self.get_behaviors(self.atype, opt))
        else:
            behaviors.extend(self.get_behaviors(self.atype, self.opts))
        return behaviors


class Behavior:
    def __init__(self, btype, val, conditionals):
        self.btype = btype
        self.val = val
        self.conditionals = conditionals

    def __str__(self):
        return self.btype.capitalize() + ' ' + str(self.val)

    def is_move(self):
        return self.btype in [
            'advance',
            'retreat',
            'push',
            'pull'
        ]


class Conditional:
    def __init__(self, expected, fn, if_result=None, else_result=None,
                 type='equals'):
        self.expected = expected
        self.fn = fn
        self.if_result = if_result
        self.else_result = else_result
        self.type = type
