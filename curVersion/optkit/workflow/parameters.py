'''
Define class Parameters, the parameter part of a project.
'''
from . import Node
from ..parameter import Variable, Response

class Parameters(Node):
	def __init__(self, 
				 variables=[], 
				 responses=[]):
		'''
		Initiate class Parameters.

		Attributes
		----------
		child : None
			the parameters is a leaf node on the workflow tree
		changedFlag : bool
			whether the parameters has been changed
		variables : list of Variable
			the list of variables of the project
		responses : list of Response
			the list of responses of the project
		'''
		super(Parameters, self).__init__(None, True)
		self.variables = variables
		self.responses = responses
		self.validator()

	def __str__(self):
		str_self = 'variables:' + '\n'
		for var in self.variables:
			str_self += var.__str__() + '\n'
		str_self += 'responses:' + '\n'
		for resp in self.responses:
			str_self += resp.__str__() + '\n'
		return str_self

	def validator(self):
		'''
		Check the validity of variables and responses

		Raises
		------
		TypeError
			When variables contains element not of type Variable.
			When responses contains element not of type Response.
		'''
		for k in self.variables:
			if not isinstance(k, Variable):
				raise TypeError(k, "is not of type Variable.")
		for k in self.responses:
			if not isinstance(k, Response):
				raise TypeError(k, "is not of type Response.")

	def add_var(self, var):
		'''
		Add variable to variables.

		Parameters
		----------
		var : Variable
			the variable about to add into variables

		Raises
		------
		TypeError
			When var is not of type Variable.
		ValueError
			When var's name is already used.
		'''
		try:
			if not isinstance(var, Variable):
				raise TypeError("Input parameter must be of type Variable.")
			for cur_var in self.variables:
				if var.name == cur_var.name:
					raise ValueError("Name already exists.")
		except Exception as e:
			raise e
		else:
			self.variables.append(var)
			super(Parameters, self).change_flag()

	def del_var(self, var):
		'''
		Delete variable from variables.

		Parameters
		----------
		var : Variable
			the variable to be deleted

		Raises
		------
		ValueError
			When var is not in variables.
		'''
		try:
			if not var in self.variables:
				raise ValueError("Variable not found.")
			else:
				self.variables.remove(var)
		except Exception as e:
			raise e
		else:
			print('deleted ', var)
			super(Parameters, self).change_flag()

	def edit_var(self, var, **kwargs):
		'''
		Edit attributes of variable.

		Parameters
		----------
		var : Variable
			the variable to be edited
		**kwargs 
			the attributes to be edited

		Raises
		------
		ValueError
			When var is not in variables.
		Other exceptions
			Check Variable.edit()
		'''
		try:
			if not var in self.variables:
				raise ValueError("Variable not found.")
			else:
				if 'name' in kwargs:
					for v in self.variables:
						if v.name == kwargs['name']:
							raise ValueError("Name already exists.")
					for r in self.responses:
						if r.name == kwargs['name']:
							raise ValueError("Name already exists.")
				self.variables[self.variables.index(var)].edit(**kwargs)
		except Exception as e:
			raise e
		else:
			super(Parameters, self).change_flag()

	def add_resp(self, resp):
		'''
		Add response to responses.

		Parameters
		----------
		resp : Response
			the response to be added into responses

		Raises
		------
		TypeError
			When resp is not of type Response.
		ValueError
			When resp's name is already used.
		'''
		try:
			if not isinstance(resp, Response):
				raise TypeError("Input parameter must be of type Response.")
			for cur_resp in self.responses:
				if resp.name == cur_resp.name:
					raise ValueError("Name already exists.")
		except Exception as e:
			raise e
		else:
			self.responses.append(resp)
			super(Parameters, self).change_flag()

	def del_resp(self, resp):
		'''
		Delete response from responses.

		Parameters
		----------
		resp : Response
			the response to be deleted

		Raises
		------
		ValueError
			When resp is not in responses.
		'''
		try:
			if not resp in self.responses:
				raise ValueError("Response not found.")
			else:
				self.responses.remove(resp)
		except Exception as e:
			raise e
		else:
			print('deleted ', resp)
			super(Parameters, self).change_flag()

	def edit_resp(self, resp, **kwargs):
		'''
		Edit attributes of response.

		Parameters
		----------
		resp : Response
			the response to be edited
		**kwargs 
			the attributes to be edited

		Raises
		------
		ValueError
			When resp is not in responses.
		Other exceptions
			Check Response.edit()
		'''
		try:
			if not resp in self.responses:
				raise ValueError("Response not found.")
			else:
				if 'name' in kwargs:
					for r in self.responses:
						if r.name == kwargs['name']:
							raise ValueError("Name already exists.")
					for v in self.variables:
						if v.name == kwargs['name']:
							raise ValueError("Name already exists.")
				self.responses[self.responses.index(resp)].edit(**kwargs)
		except Exception as e:
			raise e
		else:
			super(Parameters, self).change_flag()