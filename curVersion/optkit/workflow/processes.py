'''
Suppose there is no data transform among processes.

Define class Processes, the process part of the project.
'''
from . import Node, Process

class Processes(Node):
	def __init__(self, processes=[]):
		'''
		Initiate the Processes class.

		Attributes
		----------
		child : processes
			the list of processes is the child
		changedFlag : bool
			whether the processes has been changed
		processes : Process
			the list of processes
		'''
		super(Processes, self).__init__(processes, True)
		self.processes = processes
		self.validator()

	def __str__(self):
		str_self = 'processes:' + '\n'
		for proc in self.processes:
			str_self += proc.__str__()
		return str_self

	def validator(self):
		'''
		Check the validity of the processes.

		Raises
		------
		TypeError
			When element in processes is not of type Process.
		'''
		try:
			for proc in self.processes:
				if not isinstance(proc, Process):
					raise TypeError(proc, "is not of type Process.")
				proc.validator()
		except Exception as e:
			raise e

	def add_proc(self, proc):
		'''
		Add proc to self.processes.

		Parameters
		----------
		proc : Process
			the process to be added to the processes

		Raises
		------
		TypeError
			When proc is not of type Process.
		ValueError
			When proc's name already exists in processes.
		'''
		try:
			if not isinstance(proc, Process):
				raise TypeError("Parameter proc must be of type Process.")
			for p in self.processes:
				if p.name == proc.name:
					raise ValueError("Process's name must be unique.")
		except Exception as e:
			raise e
		else:
			self.processes.append(proc)
			super(Processes, self).change_flag()

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
			super(Processes, self).change_flag()

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
			super(Processes, self).change_flag()