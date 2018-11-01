'''
class Grandparent:
	def __init__(self, gp):
		self.gp = gp

class Parent(Grandparent):
	def __init__(self, gp, p):
		super(Parent, self).__init__(gp)
		self.p = p

class Child(Parent):
	def __init__(self, gp, p, c):
		super(Child, self).__init__(gp, p)
		self.c = c

child = Child('a', 'b', 'c')
'''
i = range(-3,4)
print(len(i))
print(type(i))