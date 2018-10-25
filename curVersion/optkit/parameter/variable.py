'''
Define parent class Variable and subclass Continuous, Discrete and Constant.
'''
class Variable:
	def __init__(self, name, description=''):
		'''
		Initiate parent class Variable.

		Attributes
		----------
		name : str
			The name of the variable.
		description : str
			The description of the variable.
		'''
		self.name = str(name)
		self.description = str(description)

	def edit(self, **kwargs):
		'''
		Allow edition of name and description.
		'''
		try:
			if 'name' in kwargs:
				self.name = str(kwargs['name'])
			if 'description' in kwargs:
				self.description = str(kwargs['description'])
		except Exception as e:
			raise e


class Continuous(Variable):
	
	def __init__(self, name, var_range, baseline, resolution, description=''):
		'''
		Initiate subclass Continuous.
		
		Attributes
		----------
		name : str
			The name of the variable.
		var_range : tuple of float
			The range of the variable, where var_range[0] is the minimum and var_range[1] is the maximum.
		baseline : float
			Base design value for the variable.
		resolution : int
			Resolution of the continuous variable.
		description : str
			The description of the variable.
		'''
		super(Continuous, self).__init__(name, description)
		self.var_range = var_range
		self.baseline = baseline
		self.resolution = resolution
		self.validator()

	def __str__(self):
		str_range = '(' + str(self.var_range[0]) + ',' + str(self.var_range[1]) + ')'
		return (self.name + '\t' + 
			    'Continuous' + '\t' + 
			    str_range + '\t' + 
			    str(self.baseline) + '\t' + 
			    str(self.resolution) + '\t' + 
			    str(self.description))

	def validator(self):
		self.validator_range()
		self.validator_baseline()
		self.validator_resolution()
		
	def validator_range(self):
		'''
		Check the validity of var_range.

		Raises
		------
		TypeError
			When var_range is not of type tuple.
			When var_range's element is not of type float or int.
		IndexError
			When var_range is not of size 2.
		ValueError
			When var_range[0] is not smaller than var_range[1].
		'''
		if not isinstance(self.var_range, tuple):
			raise TypeError("Continuous variable's range must be a tuple.")
		if not len(self.var_range) == 2:
			raise IndexError("Continuous variable's range must be of size 2.")
		if not (isinstance(self.var_range[0], (float, int)) and isinstance(self.var_range[1], (float, int))):
			raise TypeError("Continuous variable's range must be a tuple of float or int.")
		if not self.var_range[0] < self.var_range[1]:
			raise ValueError("Value of var_range[0] must be smaller than var_range[1].")
	
	def validator_baseline(self):
		'''
		Check the validity of baseline.

		Raises
		------
		TypeError
			When baseline is not of type float or int.
		IndexError
			When baseline is out of range.
		'''
		if not isinstance(self.baseline, (float, int)):
			raise TypeError("Parameter baseline must be a float or int.")
		if not (self.baseline >= self.var_range[0] and self.baseline <= self.var_range[1]):
			raise IndexError("Baseline is out of range.")

	def validator_resolution(self):
		'''
		Check the validity of resolution.

		Raises
		------
		TypeError
			When resolution is not of type int.
		'''
		if not isinstance(self.resolution, int):
			raise TypeError("Resolution must be int.")

	def edit(self, **kwargs):
		try:
			super(Continuous, self).edit(**kwargs)
			if 'var_range' in kwargs:
				self.var_range = kwargs['var_range']
				self.validator_range()
				self.validator_baseline()
			if 'resolution' in kwargs:
				self.resolution = kwargs['resolution']
				self.validator_resolution()
			if 'baseline' in kwargs:
				self.validator_baseline()
		except Exception as e:
			raise e


class Discrete(Variable):
	def __init__(self, name, var_range, baseline, description=''):
		'''
		Initiate subclass Discrete.

		Attributes
		----------
		name : str
			The name of the variable.
		var_range : list of float
			The value set of the variable.
		baseline : float
			Base design value for the variable.
		description : str
			The description of the variable.
		'''
		super(Discrete, self).__init__(name, description)
		self.var_range = var_range
		self.baseline = baseline
		self.validator()

	def __str__(self):
		str_range = '['
		for i in range(len(self.var_range)-1):
			str_range += str(self.var_range[i]) + ','
		str_range += str(self. var_range[-1]) + ']'
		return (self.name + '\t' + 
			    'Discrete' + '\t' + 
			    str_range + '\t' +
			    str(self.baseline) + '\t' + 
			    str(self.description))

	def validator(self):
		self.validator_range()
		self.validator_baseline()

	def validator_range(self):
		'''
		Check the validity of var_range.

		Raises
		------
		TypeError
			When var_range is not of type list.
			When var_range's element is not of type float or int.
		IndexError
			When var_range's size is not greater than 1.
		'''
		if not isinstance(self.var_range, list):
			raise TypeError("Discrete variable's range must be a list.")
		if not len(self.var_range) > 1:
			raise IndexError("Discrete variable's range's size must be larger than 1.")
		for k in self.var_range:
			if not isinstance(k, (float,int)):
				raise TypeError("Discrete variable's range must be a list of float or int.")
	
	def validator_baseline(self):
		'''
		Check the validity of baseline.

		Raises
		------
		TypeError
			When baseline is not of type float or int.
		IndexError
			When baselien is not in range.
		'''
		if not isinstance(self.baseline, (float, int)):
			raise TypeError("Parameter baseline must be a float or int.")
		if not self.baseline in self.var_range:
			raise IndexError("Baseline is out of range.")

	def edit(self, **kwargs):
		try:
			super(Discrete, self).edit(**kwargs)
			if 'var_range' in kwargs:
				self.var_range = kwargs['var_range']
				self.validator_range()
				self.validator_baseline()
			if 'baseline' in kwargs:
				self.baseline = kwargs['baseline']
				self.validator_baseline()
		except Exception as e:
			raise e

	
class Constant(Variable):
	def __init__(self, name, baseline, description=''):
		'''
		Initiate subclass Constant.

		Attributes
		----------
		name : str
			The name of the variable.
		baseline : float
			Base design value for the variable.
		description : str
			The description of the variable.
		'''
		super(Constant, self).__init__(name, description)
		self.baseline = baseline
		self.validator()

	def __str__(self):
		return (self.name + '\t' + 
			    'Constant' + '\t' + 
			    str(self.baseline) + '\t' + 
			    str(self.description))

	def validator(self):
		self.validator_baseline()

	def validator_baseline(self):
		'''
		Check the validity of baseline.

		Raises
		------
		TypeError
			When baseline is not of type float or int.
		'''
		if not isinstance(self.baseline, (float, int)):
			raise TypeError("Parameter baseline must be float or int.")

	def edit(self, **kwargs):
		try:
			super(Constant, self).edit(**kwargs)
			if 'baseline' in kwargs:
				self.baseline = kwargs['baseline']
				self.validator_baseline()
		except Exception as e:
			raise e
