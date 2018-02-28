class Effects:
    def __init__(self, modifiers=[], triggers=[]):
        self.modifiers = modifiers
        self.triggers = triggers


class Modifier:
    def __init__(self, type, val):
        self.type = type
        self.val = val


class Trigger:
    def __init__(self, name, actions=[]):
        self.name = name
        self.actions = actions


class Action:
    def __init__(self, type, opts, conditionals=[]):
        self.type = type
        self.opts = opts
        self.conditionals = conditionals

    @property
    def behaviors(self):
        behaviors = []
        if isinstance(self.opts, list):
            for opt in self.opts:
                behaviors.append(Behavior(self.type, opt))
        else:
            behaviors.append(Behavior(self.type, self.opts))
        return behaviors


class Behavior:
    def __init__(self, type, val):
        self.type = type
        self.val = val

    def __str__(self):
        return self.type.capitalize() + ' ' + str(self.val)


class Conditional:
    def __init__(self, test_fn, if_result=None, else_result=None):
        # Call test_fn before and after -- checking equality of results
        self.test_fn = test_fn
        self.if_result = if_result
        self.else_result = else_result
