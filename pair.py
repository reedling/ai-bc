from random import randint

class Pair:
	def __init__(self, style, base):
		self.style = style
		self.base = base

	@property
	def priority(self):
		return randint(0, 9)
