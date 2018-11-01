'''
Define class Process.
'''
from queue import Queue
from . import Node, Module

class Process(Node):
	def __init__(self,
				 name,
				 modules=[],
				 description=''):
		'''
		Initiate class Process.

		Attributes
		----------
		child : modules
			the child is equal to the modules
		changedFlag : bool
			whether the process has been changed
		name : str
			the name of the module
		modules : list of Module
			the modules of the process
		organized : list of list of Module
			store topol-sorted modules
		description : str
			the description of the module
		'''
		super(Process, self).__init__(modules, True)
		self.name = str(name)
		self.modules = modules
		self.organized = []
		self.description = str(description)
		self.validator()

	def __str__(self):
		str_self = self.name + '\t' + str(len(self.modules)) + '\t' + self.description + '\n'
		for mod in self.modules:
			str_self += mod.__str__() + '\n'
		return str_self

	def print_organized(self):
		'''
		print for test
		'''
		s0 = '['
		for l in range(len(self.organized)-1):
			s1 = '['
			for mod in range(len(self.organized[l])-1):
				s1 += self.organized[l][mod].name + ','
			s1 += self.organized[l][-1].name + ']'
			s0 += s1 + ','
		s0 += '['
		for mod in range(len(self.organized[-1])-1):
			s0 += self.organized[-1][mod].name + ','
		s0 += self.organized[-1][-1].name + ']'
		s0 += ']'
		return s0

	def validator(self):
		'''
		Check whether the elements in self.modules are all of type Module.
		'''
		try:
			for mod in self.modules:
				if not isinstance(mod, Module):
					raise TypeError("Elements of modules must be of type Module.")
				mod.validator()
		except Exception as e:
			raise e

	def edit(self, **kwargs):
		'''
		Support edition of name and description.
		'''
		if 'name' in kwargs:
			self.name = str(kwargs['name'])
		if 'description' in kwargs:
			self.description = str(kwargs['description'])

	def add_mod(self, mod):
		'''
		Add module to self.modules
		'''
		try:
			if not isinstance(mod, Module):
				raise TypeError("Parameter mod must be of type Module.")
			for m in self.modules:
				if m.name == mod.name:
					raise	ValueError("Module's name must be unique.")
		except Exception as e:
			raise e
		else:
			self.modules.append(mod)
			super(Process, self).change_flag()

	def del_mod(self, mod):
		'''
		Delete module from self.modules
		'''
		try:
			if not mod in self.modules:
				raise ValueError("Module not found.")
			else:
				self.modules.remove(mod)
		except Exception as e:
			raise e
		else:
			print("delete ", mod)
			super(Process, self).change_flag()

	def edit_mod(self, mod, **kwargs):
		'''
		Edit the attributes of module.
		'''
		try:
			if not mod in self.modules:
				raise ValueError("Module not found.")
			else:
				if 'name' in kwargs:
					for m in self.modules:
						if m.name == kwargs['name']:
							raise ValueError("Module's name must be unique.")
				self.modules[self.modules.index(mod)].edit(**kwargs)
		except Exception as e:
			raise e
		else:
			super(Process, self).change_flag()

	def organize(self, resp_list):
		'''
		Reorganize the modules in order to parallelize

		Parameters
		----------
		resp_list : project.parameters.responses
			When the project call this function, the project need to pass the responses.
		'''
		# Form a directed graph of modules.
		# sourceMatrix : module -> response
		# targetMatrix : response -> module
		# moduleGraph : module -> module (the product of sourceMatrix & targetMatrix)
		sourceMatrix = []
		targetMatrix = []
		moduleGraph = []
		module_num = len(self.modules)
		for mod in self.modules:
			stemp = []
			ttemp = []
			for resp in resp_list:
				if resp in mod.outlist:
					stemp.append(1)
				else:
					stemp.append(0)
				if resp in mod.inlist:
					ttemp.append(1)
				else:
					ttemp.append(0)
			sourceMatrix.append(stemp)
			targetMatrix.append(ttemp)
		for i in range(module_num):
			temp = []
			for j in range(module_num):
				addition = 0
				for n in range(len(resp_list)):
					addition += sourceMatrix[i][n] * targetMatrix[j][n]
				temp.append(addition)
			moduleGraph.append(temp)
		# Calculate the indegree of each module and initiate the queue.
		# topol_info : [[indegree, topol_order],...]
		# topol_que : the queue used to topol-sort
		# temp_organized : the temporary organized list of modules
		topol_que = Queue()
		topol_info = []
		temp_organized = []
		for i in range(module_num):
			indegree = 0
			for j in range(module_num):
				indegree += moduleGraph[j][i]
			if indegree == 0:
				topol_info.append([indegree, 0])
				topol_que.put(i)
				if len(temp_organized) == 0:
					temp_organized.append([])
				temp_organized[0].append(self.modules[i])
			else:
				topol_info.append([indegree, -1])
		# topol-sort
		while not topol_que.empty():
			mod_index = topol_que.get()
			for i in range(module_num):
				if not moduleGraph[mod_index][i] == 0:
					topol_info[i][0] -= 1
					if topol_info[i][0] == 0:
						topol_info[i][1] = topol_info[mod_index][1] + 1
						topol_que.put(i)
						if len(temp_organized) <= topol_info[i][1]:
							temp_organized.append([])
						temp_organized[topol_info[i][1]].append(self.modules[i])
		# circle detection & set self.organized
		try:
			for mod_info in topol_info:
				if mod_info[1] == -1:
					raise ValueError("Circle structure exist in the topology.")
		except Exception as e:
			raise e
		else:
			self.organized = temp_organized

	def run_proc(self):
		'''
		Run every module in the process.
		
		Returns
		-------
		evaluation : float
			the evaluation of the design
		'''
		if self.organized == []:
			raise ValueError("Process is not organized yet.")
		for step in self.organized:
			for mod in step:
				mod.execute()
		return evaluate()##################
