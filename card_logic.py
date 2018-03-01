class Effects:
    def __init__(self, modifiers=[], triggers=[]):
        self.modifiers = modifiers
        self.triggers = triggers


class Modifier:
    def __init__(self, mtype, val):
        self.mtype = mtype
        self.val = val


class Trigger:
    def __init__(self, name, actions=[]):
        self.name = name
        self.actions = actions


class Action:
    def __init__(self, atype, opts, conditionals=[]):
        self.atype = atype
        self.opts = opts
        self.conditionals = conditionals

    @staticmethod
    def get_behaviors(atype, magnitude):
        if atype == 'grapple':
            return [
                Behavior('push', magnitude),
                Behavior('pull', magnitude),
            ]
        elif atype == 'move':
            return [
                Behavior('advance', magnitude),
                Behavior('retreat', magnitude)
            ]
        else:
            return [Behavior(atype, magnitude)]

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
    def __init__(self, btype, val):
        self.btype = btype
        self.val = val

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
    def __init__(self, test_fn, if_result=None, else_result=None):
        # Call test_fn before and after -- checking equality of results
        self.test_fn = test_fn
        self.if_result = if_result
        self.else_result = else_result
