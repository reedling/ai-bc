from cardLogic import Effects

class Style:
	def __init__(self, name, color, attkRange, power, priority, effects = Effects()):
		self.name = name
		self.color = color
		self.attkRange = attkRange
		self.power = power
		self.priority = priority
		self.effects = effects

class Base:
	def __init__(self, name, attkRange, power, priority, effects = Effects()):
		self.name = name
		self.attkRange = attkRange
		self.power = power
		self.priority = priority
		self.effects = effects
