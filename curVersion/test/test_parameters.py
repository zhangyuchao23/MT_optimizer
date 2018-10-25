from ..optkit.parameter import *
from ..optkit.workflow import Parameters

# test declaration
var_cont = Continuous('var_cont', (1.0, 10.0), 5, 100, 'Continuous variable.')
var_disc = Discrete('var_disc', [1, 2, 3, 4, 5, 6, 7], 3, 'Discrete variable.')
var_const = Constant('var_const', 9, 'Constant variable.')

var_list = [var_cont, var_disc, var_const]

resp_obj = Objective('resp_obj', 0, 1.0, 'Objective response.')
resp_constr1 = Constraint('resp_constr1', 0, 10, 'Constraint response.')
resp_constr2 = Constraint('resp_constr2', -10, 10, 'Constraint response.')
resp_moni = Monitored('resp_moni','Monitored response.')

resp_list = [resp_obj, resp_constr1, resp_constr2, resp_moni]

param = Parameters(variables=var_list, responses=resp_list)
'''
print(param)
print()
# test add_var, del_var, add_resp, del_resp
param.add_var(var_disc)
#param.del_var(var_list[1])
param.add_resp(resp_cons)
#param.del_resp(resp_moni)

print(param)
print()
# test edit
param.edit_var(var_cont, name='var1', var_range=(1, 100), resolution=1000)
param.edit_var(var_disc, baseline=5)
param.edit_resp(resp_obj, option=1, weight=2.0)

print(param)
'''