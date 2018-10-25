import os
'''
class Parent:
	def __init__(self, name):
		self.name = name
		#self.talk()

	def __str__(self):
		return self.name
	def talk(self):
		print("i'm ",self.name)

class Child(Parent):
	def __init__(self, name, age):
		super(Child, self).__init__(name)
		self.age = age
		#self.talk()

	def __str__(self):
		return (self.name + '\n' +str(self.age))

	def talk(self):
		print("i'm ",self.name," age ",self.age)

my = Child('lzy', 22)
print(my)
string = my.__str__()
print(string)
'''
name = 'lzy'
age = '22'
edu = 'bachelor'
description = ''
string = name + '\t' + age + '\t' + edu + '\t' + description + '\n'
path = 'E:\\Code\\Marvel_tech_proj\\curVersion\\test\\data.txt'
f = open(path, 'w')
f.write(string)
f.close()
f = open(path, 'r')
info = f.readline().rstrip('\n')
print(info)
print(info.split('\t'))
print(info.split('\t')[1])
f.close()
