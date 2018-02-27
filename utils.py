from card import Base

def getStandardBases():
	return [
		Base('Dash', None, None, 9, {
			'modifiers': [
				{
					'type': 'canHit',
					'val': False
				}
			],
			'triggers': [
				{
					'name': 'afterActivating',
					'actions': [
						{
							'type': 'move',
							'val': [1, 2, 3],
							'conditionals': [
								{
									'beforeFn': lambda state: state.me.position < state.opponent.position,
									'afterFn': lambda state, compare: (state.me.position < state.opponent.position) != compare,
									'if': {
										'modifiers': [
											{
												'type': 'dodge',
												'val': True
											}
										],
									}
								}
							]
						}
					]
				}
			]
		}),
		Base('Grasp', 1, 2, 5, {
			'triggers': [
				{
					'name': 'onHit',
					'actions': [
						{
							'type': 'grapple',
							'val': 1
						}
					]
				}
			]
		}),
		Base('Drive', 1, 3, 4, {
			'triggers': [
				{
					'name': 'beforeActivating',
					'actions': [
						{
							'type': 'advance',
							'val': [1, 2]
						}
					]
				}
			]
		}),
		Base('Strike', 1, 4, 3, {
			'modifiers': [
				{
					'type': 'stunGuard',
					'val': 5
				}
			]
		}),
		Base('Shot', [1, 2, 3, 4], 3, 2, {
			'modifiers': [
				{
					'type': 'stunGuard',
					'val': 2
				}
			]
		}),
		Base('Burst', [2, 3], 3, 1, {
			'triggers': [
				{
					'name': 'startOfBeat',
					'actions': [
						{
							'type': 'retreat',
							'val': [1, 2]
						}
					]
				}
			]
		})
	]

def getAvailableIndices(fullOptions, discarded, played):
	return [x for x in range(len(fullOptions)) if x not in discarded and x not in played]
