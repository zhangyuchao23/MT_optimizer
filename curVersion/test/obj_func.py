'''
Test objective functions for the optimization.
'''
import math

def ackley_func(variables):
	'''
	search domain [-32, 32]
	minimum value is 0 at f(0,0,0,...)
	'''
	sum_of_sq = 0
	sum_of_cos = 0
	dim = len(variables)
	for var in variables:
		sum_of_sq += var.value ** 2
		sum_of_cos += math.cos(2.0 * math.pi * var.value)
	return (-20.0 * math.exp(-0.2 * math.sqrt((1 / float(dim)) * sum_of_sq))
			- math.exp((1 / float(dim)) * sum_of_cos)
			+ 20.0
			+ math.exp(1))

def rastrigin_func(variables):
	'''
	search domain [-5.12, 5.12]
	minimum value is 0 at f(0,0,0,...)
	'''
	dim = len(variables)
	_sum = 0
	for var in variables:
		_sum += va.value ** 2.0 - 10.0 * math.cos(2.0 * math.pi * var.value)
	return 10.0 * d + _sum