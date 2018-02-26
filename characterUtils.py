from simpleCharacter import SimpleBob

def getCharacterList():
	return [
		'Hikaru',
		'Khadath',
		'Simple Bob'
	]

def getCharacterByName(name):
	chars = {
		'Simple Bob': SimpleBob()
	}

	if name in chars:
		return chars[name]
	else:
		return None