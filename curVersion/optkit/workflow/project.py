'''
Run(), check_validity() check the validity of whole proj before run.

Define class Project, the highest hierarchy of the workflow.
'''
import os
from queue import Queue
from . import Node, Processes, Parameters, Module, Process
from ..parameter import *

class Project(Node):
	def __init__(self, 
				 name='untitled', 
				 procs=Processes([]),
				 params=Parameters([],[]),
				 directory=''):
		'''
		Initiate class Project.

		Attributes
		----------
		child : procs & params
			the child should be procs and params
		changedFlag : bool
			whether the project has been changed
		name : str
			the name of the project
		procs : Processes
			the processes of the project
		params :	Parameters
			the parameters of the project
		directory : str
			the work directory of the project (eg: X:\\...\\{name})
		'''
		super(Project, self).__init__([procs, params], True)
		self.name = str(name)
		self.procs = procs
		self.params = params
		self.directory = directory
		self.validator()

	def __str__(self):
		str_self = self.name + '\n' + self.params.__str__() + self.procs.__str__()
		return str_self


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
			if not isinstance(self.procs, Processes):
				raise TypeError("Parameter procs must be of type Processes.")
			self.procs.validator()
			if not isinstance(self.params, Parameters):
				raise TypeError("Parameter params must be of type Parameters.")
			self.params.validator()
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

	def save(self):
		'''
		Save the project's data to the project's directory.
		'''
		if self.whether_changed():
			if not os.path.exists(self.directory):
				os.mkdir(self.directory)
			data_file = os.path.join(self.directory,'data.txt')
			f = open(data_file,'w')
			try:
				self.write_data(f)
			except Exception as e:
				raise e
			else:
				self.flags2False()
			finally:
				f.close()
		else:
			pass

	def save_as(self, name, proj_dir):
		'''
		Save the project to a new directory and with new name.

		Parameters
		----------
		name : str
			the new name of the project
		proj_dir : str
			the new work directory of the project (eg: X:\\...\\{name})
		'''
		if not os.path.exists(proj_dir):
			os.mkdir(proj_dir)
		f = open(os.path.join(proj_dir,'data.txt'), 'w')
		try:
			self.name = name
			self.write_data(f)
		except Exception as e:
			raise e
		else:
			self.directory = proj_dir
			self.flags2False()
		finally:
			f.close()

	def load_from(self, proj_dir):
		'''
		Load existed project from given directory.

		Parameters
		----------
		proj_dir : str
			the directory of existed project (eg: X:\\...\\{name})
		'''
		f = open(os.path.join(proj_dir, 'data.txt'), 'r')
		try:
			self.read_data(f)
		except Exception as e:
			raise e
		else:
			self.directory = proj_dir
			self.changedFlag = False
		finally:
			f.close()

	def write_data(self, f):
		'''
		Write project data to file.

		Parameters
		----------
		f : file
			target file for writing
		'''
		f.write(self.__str__())
		
	def read_data(self, f):
		'''
		Read project data from file.

		Parameters
		----------
		f : file
			source file for reading
		'''
		try:
			self.name = f.readline().rstrip('\n')
			self.procs = Processes([])
			self.params = Parameters([],[])
			if not f.readline().rstrip('\n') == "variables:":
				raise IOError("Error when parsing the project file.")
			# parse variables
			line = f.readline().rstrip('\n')
			while not line == "responses:":
				self.params.add_var(self.parse_var(line))
				line = f.readline().rstrip('\n')
			# parse responses
			line = f.readline().rstrip('\n')
			while not line == "processes:":
				self.params.add_resp(self.parse_resp(line))
				line = f.readline().rstrip('\n')
			# parse processes
			line = f.readline().rstrip('\n')
			while not line == '':
				proc, mod_num = self.parse_proc(line)
				line = f.readline().rstrip('\n')
				for i in range(mod_num):
					proc.add_mod(self.parse_mod(line))
					line = f.readline().rstrip('\n')
				self.procs.add_proc(proc)
		except Exception as e:
			raise e
		else:
			self.flags2False()


	def parse_var(self, line):
		'''
		Parse a string to a variable.
		
		Parameters
		----------
		line : str

		Returns
		-------
		var : Variable
		'''
		info = line.split('\t')
		name = info[0]
		if info[1] == 'Continuous':
			str_range = info[2][1:-1].split(',')
			var_range = (float(str_range[0]), float(str_range[1]))
			baseline = float(info[3])
			resolution = int(info[4])
			description = self.parse_description(info[5:])
			return Continuous(name, var_range, baseline, resolution, description)
		elif info[1] == 'Discrete':
			str_range = info[2][1:-1].split(',')
			var_range = []
			for i in str_range:
				var_range.append(float(i))
			baseline = float(info[3])
			description = self.parse_description(info[4:])
			return Discrete(name, var_range, baseline, description)
		elif info[1] == 'Constant':
			baseline = float(info[2])
			description = self.parse_description(info[3:])
			return Constant(name, baseline, description)
		else:
			raise IOError("Error when parsing the variables.")

	def parse_resp(self, line):
		'''
		Parse a string to a response.

		Parameters
		----------
		line : str

		Returns
		-------
		resp : Response
		'''
		info = line.split('\t')
		name = info[0]
		if info[1] == 'Objective':
			if info[2] == 'min':
				option = 0
			elif info[2] == 'max':
				option = 1
			else:
				raise IOError("Error when parsing the responses.")
			weight = float(info[3])
			description = self.parse_description(info[4:])
			return Objective(name, option, weight, description)
		elif info[1] == 'Constraint':
			resp_min = float(info[2])
			resp_max = float(info[3])
			description = self.parse_description(info[4:])
			return Constraint(name, resp_min, resp_max, description)
		elif info[1] == 'Monitored':
			description = self.parse_description(info[2:])
			return Monitored(name, description)
		else:
			raise IOError("Error when parsing the responses.")

	def parse_proc(self, line):
		'''
		Parse a string to a process.

		Parameters
		----------
		line : str

		Returns
		-------
		proc : Process
		mod_num : int
			the number of modules the process has
		'''
		info = line.split('\t')
		name = info[0]
		mod_num = int(info[1])
		description = self.parse_description(info[2:])
		proc = Process(name, [], description)
		return (proc, mod_num)

	def parse_mod(self, line):
		'''
		Parse a string to a module.

		Parameters
		----------
		line : str

		Returns
		-------
		mod : Module
		'''
		info = line.split('\t')
		name = info[0]
		portal = info[1]
		str_inlist = info[2][1:-1].split(',')
		inlist = []
		for i in str_inlist:
			found = False
			for var in self.params.variables:
				if var.name == i:
					inlist.append(var)
					found = True
					break
			if not found:
				for resp in self.params.responses:
					if resp.name == i:
						inlist.append(resp)
						found = True
						break
			if not found:
				raise IOError("Error when parsing module.")
		str_outlist = info[3][1:-1].split(',')
		outlist = []
		for i in str_outlist:
			found = False
			for resp in self.params.responses:
				if resp.name == i:
					outlist.append(resp)
					found = True
					break
			if not found:
				raise IOError("Error when parsing module.")
		description = self.parse_description(info[4:])
		return Module(name, portal, inlist, outlist, description)

	def parse_description(self, l):
		'''
		Parse description.

		Parameters
		----------
		l : list
			a list of string

		Returns
		-------
		description : str
		'''
		description = ''
		for i in range(len(l)-1):
			description += l[i] + '\t'
		description += l[-1]
		return description