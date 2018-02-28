from card import Base
from cardLogic import Action, Conditional, Effects, Modifier, Trigger


def getStandardBases():
    return [
        Base('Dash', None, None, 9, Effects([
                Modifier('canHit', False)
            ], [
                Trigger('afterActivating', [
                    Action('move', [1, 2, 3], [
                        Conditional(
                            lambda state: state.me.position < state.opponent.position,
                            lambda state, compare: (state.me.position < state.opponent.position) != compare,
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
                Modifier('stunGuard', 5)
            ]
        )),
        Base('Shot', [1, 2, 3, 4], 3, 2, Effects([
                Modifier('stunGuard', 2)
            ]
        )),
        Base('Burst', [2, 3], 3, 1, Effects([], [
                Trigger('startOfBeat', [
                    Action('retreat', [1, 2])
                ])
            ]
        ))
    ]


def getAvailableIndices(fullOptions, discarded, played):
    return [x for x in range(len(fullOptions)) if x not in discarded and x not in played]
