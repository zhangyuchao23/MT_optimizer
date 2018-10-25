'''
Define parent class Response and subclass Objective, Constraint and Monitored.
'''
class Response:
	def __init__(self, name, description=''):
		'''
		Initiate parent class Response.

		Attributes
		----------
		name : str
			the name of the response
		description : str
			the description of the response
		'''
		self.name = str(name)
		self.description = str(description)
	
	def edit(self, **kwargs):
		try:
			if 'name' in kwargs:
				self.name = str(kwargs['name'])
			if 'description' in kwargs:
				self.description = str(kwargs['description'])
		except Exception as e:
			raise e


class Objective(Response):
	def __init__(self, name, option=0, weight=1.0, description=''):
		'''
		Initiate the subclass Objective

		Attributes
		----------
		name : str
			the name of the response
		option : int
			0 for minimize
			1 for maximize
		weight : float 
			weight of the objective
		description : str
			the description of the response
		'''
		super(Objective, self).__init__(name, description)
		self.option = option
		self.weight = weight
		self.validator()

	def __str__(self):
		if self.option == 0:
			str_option = 'min'
		else:
			str_option = 'max'
		return (self.name + '\t' + 
			    'Objective' + '\t' + 
			    str_option + '\t' +
			    str(self.weight) + '\t' + 
			    str(self.description))

	def validator(self):
		self.validator_option()
		self.validator_weight()

	def validator_option(self):
		'''
		Check the validity of option.

		Raises
		------
		ValueError
			When the option is not 0 or 1.
		'''
		if not (self.option == 0 or self.option == 1):
			raise ValueError("Parameter option must be 0 or 1.")

	def validator_weight(self):
		'''
		Check the validity of weight.

		Raises
		------
		TypeError
			When the weight is not of type float or int.
		'''
		if not isinstance(self.weight, (float, int)):
			raise TypeError("Parameter weight must be float or int.")
		if not self.weight > 0:
			raise ValueError("Parameter weight must be greater than 0.")

	def edit(self, **kwargs):
		super(Objective, self).edit(**kwargs)
		if 'option' in kwargs:
			self.option = kwargs['option']
			self.validator_option()
		if 'weight' in kwargs:
			self.weight = kwargs['weight']
			self.validator_weight()


class Constraint(Response):
	def __init__(self, name, resp_min, resp_max, description=''):
		'''
		Initiate the subclass Constraint

		Attributes
		----------
		name : str
			the name of the response
		resp_min : float
			the min of the response
		resp_max : float
			the max of the response
		description : str
			the description of the response
		'''
		super(Constraint, self).__init__(name, description)
		self.resp_min = resp_min
		self.resp_max = resp_max
		self.validator()

	def __str__(self):
		return (self.name + '\t' + 
			    'Constraint' + '\t' + 
			    str(self.resp_min) + '\t' +
			    str(self.resp_max) + '\t' + 
			    str(self.description))

	def validator(self):
		self.validator_min()
		self.validator_max()

	def validator_min(self):
		'''
		Check the validity of resp_min.

		Raises
		------
		TypeError
			When resp_min is not of type float or int.
		IndexError
			When resp_min is not smaller than resp_max.
		'''
		if not isinstance(self.resp_min, (float, int)):
			raise TypeError("Parameter resp_min must be float or int.")
		if not self.resp_min <= self.resp_max:
			raise IndexError("Parameter resp_min must be smaller than resp_max.")

	def validator_max(self):
		'''
		Check the validity of resp_max.

		Raises
		------
		TypeError
			When resp_max is not of type float or int.
		IndexError
			When resp_max is not greater than resp_min.
		'''
		if not isinstance(self.resp_max, (float, int)):
			raise TypeError("Parameter resp_max must be float or int.")
		if not self.resp_max >= self.resp_min:
			raise IndexError("Parameter resp_max must be greater than resp_min.")

	def edit(self, **kwargs):
		super(Constraint, self).edit(**kwargs)
		try:
			if 'resp_min' in kwargs and 'resp_max' in kwargs:
				self.resp_min = kwargs['resp_min']
				self.resp_max = kwargs['resp_max']
				self.validator_min()
				self.validator_max()
			elif 'resp_min' in kwargs:
				self.resp_min = kwargs['resp_min']
				self.validator_min()
			elif 'resp_max' in kwargs:
				self.resp_max = kwargs['resp_max']
				self.validator_max()
		except Exception as e:
			raise e


class Monitored(Response):
	def __init__(self, name, description=''):
		super(Monitored, self).__init__(name, description)

	def __str__(self):
		return (self.name + '\t' + 
			    'Monitored' + '\t' + 
			    str(self.description))

	def edit(self, **kwargs):
		super(Monitored, self).edit(**kwargs)