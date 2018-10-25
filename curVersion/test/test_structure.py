from ..optkit.workflow import *
from ..optkit.parameter import *
from .test_parameters import param

path = 'E:\\Code\\Marvel_tech_proj\\curVersion\\test\\test_proj'
proj = Project(name='test_proj', params=param, directory=path)

# establish the structure
mod1 = Module('mod1', 'General', [proj.params.variables[0]], [proj.params.responses[3]], 'module 1')
mod2 = Module('mod2', 'General', [proj.params.variables[2], proj.params.responses[3]], [proj.params.responses[1]], 'module 2')
mod3 = Module('mod3', 'General', proj.params.responses[1:3], [proj.params.responses[0]], 'module 3')
mod4 = Module('mod4', 'General', [proj.params.variables[1]], [proj.params.responses[2]], 'module 4')

proj.procs.add_proc(Process('proc0', [], 'proc0'))
proj.procs.processes[0].add_mod(mod1)
proj.procs.processes[0].add_mod(mod2)
proj.procs.processes[0].add_mod(mod3)
proj.procs.processes[0].add_mod(mod4)

proj.procs.add_proc(Process('proc1', [], 'proc1'))
proj.procs.add_proc(Process('proc2', [mod1], 'proc2'))

print(proj)

# test process.organize()
proj.procs.processes[0].organize(proj.params.responses)
print(proj.procs.processes[0].print_organized())

# test project.save() save_as() load_from()
proj.save()
proj.save_as('testP','E:\\Code\\Marvel_tech_proj\\curVersion\\test\\testP')
proj2 = Project(name='untitiled',directory=path)
proj2.load_from('E:\\Code\\Marvel_tech_proj\\curVersion\\test\\testP')
print(proj2)