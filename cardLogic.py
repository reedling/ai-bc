class Effects:
	def __init__(self, modifiers = [], triggers = []):
		self.modifiers = modifiers
		self.triggers = triggers

class Modifier:
	def __init__(self, type, val):
		self.type = type
		self.val = val

class Trigger:
	def __init__(self, name, actions = []):
		self.name = name
		self.actions = actions

class Action:
	def __init__(self, type, val, conditionals = []):
		self.type = type
		self.val = val
		self.conditionals = conditionals

class Conditional:
	def __init__(self, beforeFn, afterFn, ifResult = None, elseResult = None):
		self.beforeFn = beforeFn
		self.afterFn = afterFn
		self.ifResult = ifResult
		self.elseResult = elseResult