'''
Complete execute()

Define class Module.
'''
from . import Node, Variable, Response
from ..utils.portals import portals

class Module(Node):
	def __init__(self,
				 name,
				 portal='General',
				 inlist=[],
				 outlist=[],
				 description=''):
		'''
		Initiate class Module.

		Attributes
		----------
		child : None
			module is the leaf node of the workflow tree
		changedFlag : bool
			whether the module has been changed
		name : str
			the name of the module
		portal : str
			the software portal the module uses
		inlist : list
			the input list of the module
		outlist : list
			the output list of the module
		description : str
			the description of the module
		'''
		super(Module, self).__init__(None, True)
		self.name = str(name)
		self.portal = portal
		self.inlist = inlist
		self.outlist = outlist
		self.description = str(description)
		self.validator()

	def __str__(self):
		str_inlist = '['
		for i in range(len(self.inlist)-1):
			str_inlist += self.inlist[i].name + ','
		str_inlist += self.inlist[-1].name + ']'
		str_outlist = '['
		for i in range(len(self.outlist)-1):
			str_outlist += self.outlist[i].name + ','
		str_outlist += self.outlist[-1].name + ']'
		return (self.name + '\t' + 
				self.portal + '\t' +
				str_inlist + '\t' +
				str_outlist + '\t' +
				self.description)

	def validator(self):
		try:
			for i in self.inlist:
				if not (isinstance(i, Variable) or isinstance(i, Response)):
					raise TypeError("The input of the module must be of type Variable or Response.")
			for i in self.outlist:
				if not isinstance(i, Response):
					raise TypeError("The output of the module must be of type Response.")
			self.validator_portal()
		except Exception as e:
			raise e

	def validator_portal(self):
		'''
		Check whether the portal is in the list.
		'''
		try:
			if not self.portal in portals:
				raise ValueError("Parameter portal is not found in the portal list.")
		except Exception as e:
			raise e

	def edit(self, **kwargs):
		'''
		Support edition of parameter name, portal and description.
		'''
		try:
			if 'name' in kwargs:
				self.name = kwargs['name']
			if 'portal' in kwargs:
				self.portal = kwargs['portal']
				self.validator_portal()
			if 'description' in kwargs:
				self.description = kwargs['description']
		except Exception as e:
			raise e
		else:
			super(Module, self).change_flag()

	def add_inlist(self, obj):
		'''
		Support add object to inlist.
		'''
		try:
			if not (isinstance(obj, Variable) or isinstance(obj, Response)):
				raise TypeError("Parameter obj must be of type Variable or Response.")
		except Exception as e:
			raise e
		else:
			self.inlist.append(obj)
			super(Module, self).change_flag()

	def del_inlist(self, obj):
		'''
		Support delete object from inlist.
		'''
		try:
			if not obj in self.inlist:
				raise ValueError("obj is not in inlist.")
			else:
				self.inlist.remove(obj)
		except Exception as e:
			raise e
		else:
			super(Module, self).change_flag()

	def add_outlist(self, obj):
		'''
		Support add object to outlist.
		'''
		try:
			if not isinstance(obj, Response):
				raise TypeError("Parameter obj must be of type Response.")
		except Exception as e:
			raise e
		else:
			self.outlist.append(obj)
			super(Module, self).change_flag()

	def del_outlist(self, obj):
		'''
		Support delete object from outlist.
		'''
		try:
			if not obj in self.outlist:
				raise ValueError("obj is not in outlist.")
			else:
				self.outlist.remove(obj)
		except Exception as e:
			raise e
		else:
			super(Module, self).change_flag()

	def execute(self):
		'''
		Send inlist's data to portal software.
		Drive software do calculations.
		Get data to outlist.
		'''
		pass