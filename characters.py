class Character:
	def __init__(self, name, aiControlled):
		self.name = name
		self.aiControlled = aiControlled
		self.life = 20
		self.position = None

	def getAnte(self, info):
		return None

	def getStatus(self):
		return {
			'life': self.life,
			'position': self.position
		}

def getCharacterList():
	return [
		'Hikaru',
		'Khadath'
	]
