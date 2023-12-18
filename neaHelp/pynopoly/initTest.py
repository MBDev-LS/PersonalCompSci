
class Parent():
	def __init__(self, parentAttr) -> None:
		self.parentAttr = parentAttr
	
	def _testFunc(self):
		print('Func')


class Child(Parent):
	def __init__(self, parentAttr) -> None:
		super().__init__(parentAttr)

	def getParentAttr(self):
		self.__testFunc()
		return self.parentAttr
	
	


child = Child(1)

print(child.getParentAttr())