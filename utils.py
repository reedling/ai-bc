from random import choice, shuffle

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
                            'changes',
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


def get_possible(selection, trigger, get_behaviors=False):
    possible = []
    effects = selection.get_effects(trigger)
    for effect in effects:
        for action in effect.actions:
            if get_behaviors:
                possible.append(action.behaviors)
            else:
                possible.append(action)
    return possible


def choose_random_valid_behavior(actions, state):
    action = choice(actions)
    possible_behaviors = state.get_permitted_behaviors(action)
    return action, choice(possible_behaviors)


def stacks(mod):
    return mod in [
        'power',
        'priority',
        'soak',
        'stun_guard'
    ]


def left_of_opponent(state):
    return state.p.position < state.o.position


def get_played_cards(p):
    played = {
        'styles': [s.name for s in p.played_styles],
        'bases': [b.name for b in p.played_bases]
    }
    return played


def player_state_string_cli(desc, p):
    played = get_played_cards(p)
    acc = []
    acc.append('({}) -- {}'.format(desc, p.name))
    acc.append('  Life: {}'.format(p.life))

    if p.selection is not None:
        acc.append('  Selection: {}'.format(str(p.selection)))

    if len(played['styles']) + len(played['bases']) > 0:
        acc.append('  Played:')
        if len(played['styles']) > 0:
            acc.append('    Styles: {}'.format(' '.join(played['styles'])))
        if len(played['bases']) > 0:
            acc.append('    Bases:  {}'.format(' '.join(played['bases'])))

    acc.append('  Outer Discard:')
    if len(p.discards.outer['styles']) > 0:
        acc.append('    Styles: {}'.format(' '.join(
            [outs.name for outs in p.discards.outer['styles']]
        )))
    if len(p.discards.outer['bases']) > 0:
        acc.append('    Bases:  {}'.format(' '.join(
            [outb.name for outb in p.discards.outer['bases']]
        )))
    acc.append('  Inner Discard:')
    if len(p.discards.inner['styles']) > 0:
        acc.append('    Styles: {}'.format(' '.join(
            [ins.name for ins in p.discards.inner['styles']]
        )))
    if len(p.discards.inner['bases']) > 0:
        acc.append('    Bases:  {}'.format(' '.join(
            [inb.name for inb in p.discards.inner['bases']]
        )))

    if p.finisher is not None:
        acc.append('  Finisher: {}'.format(p.finisher.name))
    else:
        acc.append('  (Finisher unavailable)')

    acc.append('')
    return '\n'.join(acc)


def state_string_cli(state):
    acc = []
    acc.append('Beat {}'.format(state.beat))
    acc.append(player_state_string_cli('Enemy', state.o))
    acc.append(str(state.board))
    acc.append('')
    acc.append(player_state_string_cli('You', state.p))
    acc.append('')
    return '\n'.join(acc)
