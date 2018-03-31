from card import Style, Base
from card_logic import Effects, Modifier, Trigger, Action, Conditional
from selection import Finisher
from utils import get_standard_bases


class Kallistar:
    def __init__(self):
        self.styles = [
            Style('Flare', 'yellow', 0, 3, 0, Effects([], [
                Trigger('reveal', Effects([], [], [], [
                    Conditional(
                        'Human',
                        lambda state: get_form(state),
                        Effects([
                            Modifier('lose_life', 3),
                            Modifier('priority', 3)
                        ])
                    )
                ])),
                Trigger('endOfBeat', Effects([], [], [], [
                    Conditional(
                        'Elemental',
                        lambda state: get_form(state),
                        Effects([
                            Modifier(self.change_form, 'Human')
                        ])
                    )
                ]))
            ])),
            Style('Caustic', 'green', 0, 1, -1, Effects([], [
                Trigger('onHit', Effects([], [], [], [
                    Conditional(
                        'Elemental',
                        lambda state: get_form(state),
                        Effects([
                            Modifier('stun', True, True)
                        ])
                    )
                ]))], [], [
                Conditional(
                    'Human',
                    lambda state: get_form(state),
                    Effects([
                        Modifier('soak', 2)
                    ])
                )
            ])),
            Style('Blazing', 'blue', 0, 0, 1, Effects([], [
                Trigger('afterActivating', Effects([], [], [], [
                    Conditional(
                        'Human',
                        lambda state: get_form(state),
                        Effects([], [], [
                            Action('move', [1, 2])
                        ])
                    )
                ]))], [], [
                Conditional(
                    'Elemental',
                    lambda state: get_form(state),
                    Effects([
                        Modifier('range', [0, 1])
                    ])
                )
            ])),
            Style('Volcanic', 'orange', [2, 3, 4], 0, 0, Effects([], [
                Trigger('onHit', Effects([], [], [], [
                    Conditional(
                        'Elemental',
                        lambda state: get_form(state),
                        Effects([
                            Modifier('priority', -2, True, True)
                        ])
                    )
                ])),
                Trigger('endOfBeat', Effects([], [], [], [
                    Conditional(
                        'Human',
                        lambda state: get_form(state),
                        Effects([], [], [
                            Action('teleport', 'all')
                        ])
                    )
                ]))
            ])),
            Style('Ignition', 'red', 0, 1, -1, Effects([], [
                Trigger('reveal', Effects([], [], [], [
                    Conditional(
                        'Elemental',
                        lambda state: get_form(state),
                        Effects([
                            Modifier('lose_life', 3),
                            Modifier('power', 3)
                        ])
                    )
                ])),
                Trigger('endOfBeat', Effects([], [], [], [
                    Conditional(
                        'Human',
                        lambda state: get_form(state),
                        Effects([
                            Modifier(self.change_form, 'Elemental')
                        ])
                    )
                ]))
            ]))
        ]
        self.bases = get_standard_bases()
        self.bases.extend([
            Base('Spellbolt', [2, 3, 4, 5, 6], 2, 3, Effects([], [
                Trigger('onHit', Effects([], [], [], [
                    Conditional(
                        'Human',
                        lambda state: get_form(state),
                        Effects([
                            Modifier('power', -2, True)
                        ])
                    ),
                    Conditional(
                        'Elemental',
                        lambda state: get_form(state),
                        Effects([], [], [
                            Action('pull', [1, 2])
                        ])
                    )
                ]))
            ]))
        ])
        self.finishers = [
            Finisher('Energy Beams I', [1, 3, 5], 7, 6, Effects([
                Modifier('stun_immune', True)
            ])),
            Finisher('Energy Beams II', [2, 4, 6], 7, 6, Effects([
                Modifier('stun_immune', True)
            ]))
        ]
        self.form = 'Human'

    def get_ante_effects(self):
        if self.form == 'Human':
            return Effects([
                Modifier('soak', 1)
            ])
        elif self.form == 'Elemental':
            return Effects([
                Modifier('power', 2),
                Modifier('priority', 2),
                Modifier('lose_life', 1)
            ])

    def change_form(self, new_form):
        self.form = new_form

    def get_state_details(self):
        return {
            'Form': self.form
        }


def get_form(state):
    return state.p.character.form
