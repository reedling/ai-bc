from random import randint

class Pair:
	def __init__(self, style, base):
		self.style = style
		self.base = base

	@property
	def priority(self):
		return self.style.priority + self.base.priority

	def getEffectsForTrigger(self, trigger):
		triggerEffects = []
		if trigger in self.style.effects:
			triggerEffects.append(self.base.effects[trigger])
		if trigger in self.base.effects:
			triggerEffects.append(self.base.effects[trigger])
		return triggerEffects

	def __str__(self):
		return self.style.name + ' ' + self.base.name