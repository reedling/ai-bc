from random import choice

from card import Base
from card_logic import Action, Conditional, Effects, Modifier, Trigger


def get_standard_bases():
    return [
        Base('Dash', None, None, 9, Effects([
                Modifier('can_hit', False)
            ], [
                Trigger('afterActivating', [
                    Action('move', [1, 2, 3], [
                        Conditional(
                            lambda state: left_of_opponent(state),
                            Effects([
                                Modifier('dodge', True)
                            ])
                        )
                    ])
                ])
            ]
        )),
        Base('Grasp', 1, 2, 5, Effects([], [
                Trigger('onHit', [
                    Action('grapple', 1)
                ])
            ]
        )),
        Base('Drive', 1, 3, 4, Effects([], [
                Trigger('beforeActivating', [
                    Action('advance', [1, 2])
                ])
            ]
        )),
        Base('Strike', 1, 4, 3, Effects([
                Modifier('stun_guard', 5)
            ]
        )),
        Base('Shot', [1, 2, 3, 4], 3, 2, Effects([
                Modifier('stun_guard', 2)
            ]
        )),
        Base('Burst', [2, 3], 3, 1, Effects([], [
                Trigger('startOfBeat', [
                    Action('retreat', [1, 2])
                ])
            ]
        ))
    ]


def get_possible_behaviors(selection, trigger):
    possible = []
    effects = selection.get_effects(trigger)
    for effect in effects:
        for action in effect.actions:
            possible.append(action.behaviors)
    return possible


def choose_random_valid_behavior(possible_behaviors, state):
    chosen = []
    indices = [x for x in range(0, len(possible_behaviors))]
    for i in indices:
        opt = None
        while len(possible_behaviors[i]) > 0 and opt is None:
            opt = choice(possible_behaviors[i])
            # print(state.board)

        if opt is not None:
            chosen.append(opt)
            # update state so we can choose valid actions
    return chosen


def stacks(mod):
    return mod in [
        'soak',
        'stun_guard'
    ]


def left_of_opponent(state):
    return state.p.position < state.o.position


def get_available_indices(full_opts, discarded, played):
    rng = range(len(full_opts))
    return [x for x in rng if x not in discarded and x not in played]
