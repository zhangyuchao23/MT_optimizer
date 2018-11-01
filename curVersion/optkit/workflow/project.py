'''
Run(), check_validity() check the validity of whole proj before run.

Define class Project, the highest hierarchy of the workflow.
'''
import os
from queue import Queue
from . import Node, Variable, Response, Module, Process

class Project(Node):
	def __init__(self, 
				 name='untitled',
				 variables=[],
				 responses=[],
				 processes=[],
				 directory=''):
		'''
		Initiate class Project.

		Attributes
		----------
		child : variables & responses & processes
			the child should be procs and params
		changedFlag : bool
			whether the project has been changed
		name : str
			the name of the project
		variables : list of Variable
			the variables of the project
		responses : list of Response
			the responses of the project
		processes : list of Process
			the processes of the project
		directory : str
			the work directory of the project (eg: X:\\...\\{name})
		'''
		super(Project, self).__init__([*variables, *responses, *processes], True)
		self.name = str(name)
		self.variables = variables
		self.responses = responses
		self.processes = processes
		self.directory = directory
		self.validator()

	def __str__(self):
		str_self = self.name + '\t' + self.directory + '\n'
		str_vars = 'variables:\n'
		for var in self.variables:
			str_vars += var.__str__() + '\n'
		str_resps = 'responses:\n'
		for resp in self.responses:
			str_resps += resp.__str__() + '\n'
		str_procs = 'processes:\n'
		for proc in self.processes:
			str_procs += proc.__str__() 
		return (str_self + str_vars + str_resps + str_procs)

	def validator(self):
		'''
		Check the validity of project.

		Raises
		------
		TypeError
			When processes has element not of type Process.
			When param is not of type Parameters.
		'''
		try:
			for var in self.variables:
				if not isinstance(var, Variable):
					raise TypeError(var, "is not of type Variable.")
			for resp in self.responses:
				if not isinstance(resp, Response):
					raise TypeError(resp, "is not of type Response.")
			for proc in self.processes:
				if not isinstance(proc, Process):
					raise TypeError(proc, "is not of type Process.")
		except Exception as e:
			raise e
	
	def whether_changed(self):
		'''
		Check whether the project has been changed.
		Use BFS to search the tree.

		Return
		------
		changed : bool
		'''
		q = Queue()
		q.put(self)
		changed = False
		while not q.empty():
			node = q.get()
			if node.changedFlag == True:
				changed = True
				break
			else:
				if not node.child == None:
					for i in node.child:
						q.put(i)
		return changed

	def flags2False(self):
		'''
		Turn the changedFlag of all nodes on the workflow tree to False.
		Use BFS to search the tree.
		'''
		q = Queue()
		q.put(self)
		while not q.empty():
			node = q.get()
			node.changedFlag = False
			if not node.child == None:
				for i in node.child:
					q.put(i)

	def add_var(self, var):
		'''
		Add one or more variables to variables.

		Parameters
		----------
		var : Variable or list of Variables
			the variable about to add into variables

		Raises
		------
		TypeError
			When var is not of type Variable.
		ValueError
			When var's name is already used.
		'''
		try:
			if isinstance(var, Variable):
				for cur_var in self.variables:
					if var.name == cur_var.name:
						raise ValueError("Name already exists.")
				self.variables.append(var)
			elif isinstance(var, list):
				for v in var:
					if not isinstance(v, Variable):
						raise TypeError(v, "is not of type Variable.")
					for cur_var in self.variables:
						if var.name == cur_var.name:
							raise ValueError("Name already exists.")
					self.variables.append(var)
			else:
				raise TypeError(var, "must be of type Variable or list of Variable.")
		except Exception as e:
			raise e
		else:
			self.changedFlag = True

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
			self.changedFlag = True

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
			self.changedFlag = True

	def add_resp(self, resp):
		'''
		Add one or more responses to responses.

		Parameters
		----------
		resp : Response or list of Response
			the response to be added into responses

		Raises
		------
		TypeError
			When resp is not of type Response.
		ValueError
			When resp's name is already used.
		'''
		try:
			if isinstance(resp, Response):
				for cur_resp in self.responses:
					if resp.name == cur_resp.name:
						raise ValueError("Name already exists.")
				self.responses.append(resp)
			elif isinstance(resp, list):
				for r in resp:
					if not isinstance(r, Response):
						raise TypeError(r, "is not of type Response.")
					for cur_resp in self.responses:
						if r.name == cur_resp.name:
							raise ValueError("Name already exists.")
					self.responses.append(resp)
			else:
				raise TypeError(resp, "must be of type Response or list of Response.")
		except Exception as e:
			raise e
		else:
			self.changedFlag = True

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
			self.changedFlag = True

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
			self.changedFlag = True

	def add_proc(self, proc):
		'''
		Add one or more proc to self.processes.

		Parameters
		----------
		proc : Process or list of Process
			the process to be added to the processes

		Raises
		------
		TypeError
			When proc is not of type Process.
		ValueError
			When proc's name already exists in processes.
		'''
		try:
			if isinstance(proc, Process):
				for p in self.processes:
					if p.name == proc.name:
						raise ValueError("Process's name must be unique.")
				self.processes.append(proc)
			elif isinstance(proc, list):
				for p in proc:
					if not isinstance(p, Process):
						raise TypeError(p, "is not of type Process.")
					for cur_proc in self.processes:
						if p.name == cur_proc.name:
							raise ValueError("Name already exists.")
					self.processes.append(p)
			else:
				raise TypeError(proc, "must be of type Process or list of Process.")
		except Exception as e:
			raise e
		else:
			self.changedFlag = True

	def del_proc(self, proc):
		'''
		Delete the proc from processes.

		Parameters
		----------
		proc : Process
			the process to be deleted

		Raises
		------
		ValueError
			When proc is not in processes.
		'''
		try:
			if not proc in self.processes:
				raise ValueError("Parameter proc not in processes.")
			else:
				self.processes.remove(proc)
		except Exception as e:
			raise e
		else:
			print("deleted ", proc)
			self.changedFlag = True

	def edit_proc(self, proc, **kwargs):
		'''
		Edit the attributes of proc

		Parameters
		----------
		proc : Process
			proc to be edited
		**kwargs
			parameters to be edited

		Raises
		------
		ValueError
			When proc is not in processes.
		'''
		try:
			if not proc in self.processes:
				raise ValueError("Process not found.")
			else:
				if 'name' in kwargs:
					for p in self.processes:
						if p.name == kwargs['name']:
							raise ValueError("Process's name must be unique.")
				self.processes[self.processes.index(proc)].edit(**kwargs)
		except Exception as e:
			raise e
		else:
			self.changedFlag = True
	
	def run_opt(self, proc, method, **kwargs):
		'''
		Run every module in the process.

		Parameters
		----------
		proc : Process
			the process to run
		method : str
			the algorithm to do the optimization
		**kwargs
			the algorithm parameters
		'''
		# check process's validity and organize the process
		if not proc in self.processes:
			raise ValueError("Process not found.")
		for mod in proc.modules:
			for in_obj in mod.inlist:
				if not (in_obj in self.variables or in_obj in self.responses):
					raise ValueError("Module {}'s inlist contains invalid object.".format(mod.name))
			for out_obj in mod.outlist:
				if not out_obj in self.responses:
					raise ValueError("Module {}'s outlist contains invalid object.".format(mod.name))
		proc.organize()
		# create an instance of the optimizer
		if method == 'PSO':
			optimizer = PSO_Optimizer(variables=, **kwargs)
			optimizer.optimize(proc.run_proc, **kwargs)