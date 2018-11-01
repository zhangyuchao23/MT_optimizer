from ..optkit.workflow import Continuous, Discrete
from ..optkit.algorithm.PSO import PSO_Optimizer
from .obj_func import ackley_func

variables = []
#var_range = list(range(-32, 33))
for i in range(20):
	name = 'var' + str(i)
	variables.append(Continuous(name, (-32,32), 1, 100))
	#variables.append(Discrete(name, var_range, 1))

opt = PSO_Optimizer(30, 20, variables)
opt.optimize(100, ackley_func, variables)