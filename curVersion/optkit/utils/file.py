'''
The file system of the software.
'''
from ..workflow import *

def save(proj):
	'''
	Save project's data to its directory.
	'''
	if proj.whether_changed():
		if not os.path.exists(proj.directory):
				os.mkdir(proj.directory)
			data_file = os.path.join(proj.directory,'data.txt')
			f = open(data_file,'w')
			try:
				f.write(proj.__str__())
			except Exception as e:
				raise e
			else:
				proj.flags2False()
			finally:
				f.close()
		else:
			pass

def save_as(proj, name, proj_dir):
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
		proj.name = name
		proj.directory = proj_dir
		f.write(proj.__str__())
	except Exception as e:
		raise e
	else:
		proj.flags2False()
	finally:
		f.close()

def open_proj(proj_dir):
	'''
	Load existed project from given directory.

	Parameters
	----------
	proj_dir : str
		the directory of existed project (eg: X:\\...\\{name})

	Returns
	-------
	proj : Project
		the new project be opened
	'''
	f = open(os.path.join(proj_dir, 'data.txt'), 'r')
	try:
		proj_info = f.readline().rstrip('\n').split('\t')
		name = proj_info[0]
		directory = proj_info[1]
		variables = []
		responses = []
		processes = []
		if not f.readline().rstrip('\n') == "variables:":
			raise IOError("Error when parsing the project file.")
		# parse variables
		line = f.readline().rstrip('\n')
		while not line == "responses:":
			variables.append(parse_var(line))
			line = f.readline().rstrip('\n')
		# parse responses
		line = f.readline().rstrip('\n')
		while not line == "processes:":
			responses.append(parse_resp(line))
			line = f.readline().rstrip('\n')
		# parse processes
		line = f.readline().rstrip('\n')
		while not line == '':
			proc, mod_num = parse_proc(line)
			line = f.readline().rstrip('\n')
			for i in range(mod_num):
				proc.add_mod(parse_mod(line))
				line = f.readline().rstrip('\n')
			processes.append(proc)
		# create a new proj
		proj = Project(name, variables, responses, processes, directory)
	except Exception as e:
		raise e
	else:
		proj.flags2False()
		return proj
	finally:
		f.close()

def parse_var(line):
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
		description = parse_description(info[5:])
		return Continuous(name, var_range, baseline, resolution, description)
	elif info[1] == 'Discrete':
		str_range = info[2][1:-1].split(',')
		var_range = []
		for i in str_range:
			var_range.append(float(i))
		baseline = float(info[3])
		description = parse_description(info[4:])
		return Discrete(name, var_range, baseline, description)
	elif info[1] == 'Constant':
		baseline = float(info[2])
		description = parse_description(info[3:])
		return Constant(name, baseline, description)
	else:
		raise IOError("Error when parsing the variables.")

def parse_resp(line):
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
		description = parse_description(info[4:])
		return Objective(name, option, weight, description)
	elif info[1] == 'Constraint':
		resp_min = float(info[2])
		resp_max = float(info[3])
		description = parse_description(info[4:])
		return Constraint(name, resp_min, resp_max, description)
	elif info[1] == 'Monitored':
		description = parse_description(info[2:])
		return Monitored(name, description)
	else:
		raise IOError("Error when parsing the responses.")

def parse_proc(line):
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
	description = parse_description(info[2:])
	proc = Process(name, [], description)
	return (proc, mod_num)

def parse_mod(line):
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
		for var in params.variables:
			if var.name == i:
				inlist.append(var)
				found = True
				break
		if not found:
			for resp in params.responses:
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