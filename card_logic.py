

# An Effects object contains the modifiers, triggers, actions, and conditionals
# associated with a selection, event, or condition.
class Effects:
    def __init__(self, modifiers=[], triggers=[], actions=[], conditionals=[]):
        self.modifiers = modifiers
        self.triggers = triggers
        self.actions = actions
        self.conditionals = conditionals


# A standard Modifier applies to a player for only the current turn.
# The options opponent, onset, and duration my change this.
# Modifiers may be something like stun-guard or life loss.
class Modifier:
    def __init__(self, mtype, val, opponent=False, onset=0, duration=1):
        self.mtype = mtype
        self.val = val
        self.opponent = opponent
        self.onset = onset
        self.duration = duration

    def __str__(self):
        if self.onset == 0:
            props = (self.mtype, self.val, self.duration)
            return '{} ({}) - ACTIVE - Duration {}'.format(*props)
        else:
            props = (self.mtype, self.val, self.onset, self.duration)
            return '{} ({}) - Onset in {} - Duration {}'.format(*props)


# A Trigger will make its effects available for handling at a specific
#  point in the beat.  For example, a Trigger with the name 'endOfBeat'
#  will have its effects handled during the End of Beat phase.
class Trigger:
    def __init__(self, name, effects=Effects()):
        self.name = name
        self.effects = effects


# Actions are high-level descriptors that capture possible behavior.
# In general, there are several available behaviors available per action.
# Depending on the state, some of the behaviors may not be executable.
class Action:
    def __init__(self, atype, opts=[], conditionals=[]):
        self.atype = atype
        self.opts = opts
        self.conditionals = conditionals
        if atype == 'teleport' and opts == 'all':
            self.needs_state_for_behaviors = True
        else:
            self.needs_state_for_behaviors = False

    def behaviors_for_state(self, state):
        behaviors = []
        if self.atype == 'teleport' and self.opts == 'all':
            for pos in range(state.board.length):
                behaviors.append(Behavior('teleport', pos, self.conditionals))
        else:
            behaviors = self.behaviors
        return behaviors

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


# A Behavior is a specific, concrete notion of how an action may/will
#  be executed.  For example, the behavior 'retreat 2' may be derived
#  from an action of type 'move' with options [1, 2].
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


# A Conditional provides a way of applying different effects circumstantially.
# For instance, Kallistar's cards all have very different effects based on her
#  current form.  See kallistar.py for some examples.
class Conditional:
    def __init__(self, expected, fn, if_result=None, else_result=None,
                 type='equals'):
        self.expected = expected
        self.fn = fn
        self.if_result = if_result
        self.else_result = else_result
        self.type = type
