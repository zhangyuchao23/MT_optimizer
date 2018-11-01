from ..optkit.workflow import *

# test declaration
var_cont = Continuous('var_cont', (1.0, 10.0), 5, 100, 'Continuous variable.')
var_disc = Discrete('var_disc', [1, 2, 3, 4, 5, 6, 7], 3, 'Discrete variable.')
var_const = Constant('var_const', 9, 'Constant variable.')

var_list = [var_cont, var_disc, var_const]

resp_obj1 = Objective('resp_obj1', 0, 1.0, 'Objective response.')
resp_obj2 = Objective('resp_obj2', 0, 1.0, 'Objective response.')
resp_constr1 = Constraint('resp_constr1', 0, 10, 'Constraint response.')
resp_constr2 = Constraint('resp_constr2', -10, 10, 'Constraint response.')
resp_moni = Monitored('resp_moni','Monitored response.')

resp_list = [resp_obj1, resp_obj2, resp_constr1, resp_constr2, resp_moni]

mod1 = Module('mod1', 'General', [var_cont, var_const], [resp_obj1, resp_obj2, resp_constr1, resp_moni])
proc1 = Process('proc1', [mod1])
proj = Project('proj', var_list, resp_list, [proc1])

print(proj)

proj.del_resp(resp_obj2)

print(proj)
for p in proj.processes:
	for m in p.modules:
		for r in m.outlist:
			print(r)