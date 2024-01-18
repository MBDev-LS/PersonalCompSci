
class Info():
	def __init__(self, text) -> None:
		self.text = text

class Thing():
	def __init__(self, info) -> None:
		self.info = info

info = Info('1')
thing = Thing(info)

print(thing.info)

del thing.info

print(thing.info)