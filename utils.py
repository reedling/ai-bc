from card import Base

def getStandardBases():
	return [
		Base('Dash', None, None, 9, {
			'canHit': False,
			'afterActivating': {
				'move': [1, 2, 3],
				'onPass': {
					'canBeHit': False
				}
			}
		}),
		Base('Grasp', 1, 2, 5, {
			'onHit': {
				'grapple': 1
			}
		}),
		Base('Drive', 1, 3, 4, {
			'beforeActivating': {
				'advance': [1, 2]
			}
		}),
		Base('Strike', 1, 4, 3, {
			'stunGuard': 5
		}),
		Base('Shot', [1, 2, 3, 4], 3, 2, {
			'stunGuard': 2
		}),
		Base('Burst', [2, 3], 3, 1, {
			'startOfBeat': {
				'retreat': [1, 2]
			}
		})
	]

def getAvailableIndices(fullOptions, discarded, played):
	return [x for x in range(len(fullOptions)) if x not in discarded and x not in played]