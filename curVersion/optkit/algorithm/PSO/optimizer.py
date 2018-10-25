'''
This module implements Optimizer class.
'''
import time
from collections import namedtuple
from scipy.spatial import cKDTree
import numpy as np
import swarm
from ..utils.shared_data import variables

class Optimizer:
	'''
	An optimizer class.

	Attributes
	----------
	particles : int
		the number of the particles in the swarm
	dimensions : int
		the number of the dimensions
	neighbour : int
		the size of a particle's neighbourhood
	pswarm : Swarm
		the particle swarm of this optimizer
	history : list of namedtuple
		store every iteration's gbest_pos, gbest_eval, pbest_pos, pbest_eval, position, velocity, evaluation
	History : type
		a structure and the basic element of history
	var_list : list of str
		the list of names of input variables
	upper : ndarray of float, size dimensions
		the upper bound of each dimension
	lower : ndarray of float, size dimensions
		the lower bound of each dimension
	v_limit : ndarray of float, size dimensions
		the limit of velocity. set to (upper-lower)/2
	'''
	def __init__(self, particles, neighbour):
		'''
		Initialize the optimizer.
		'''
		self.particles = particles
		self.neighbour = neighbour
		'''
		self.history = []
		self.History = namedtuple(
			'History',
			[
				'gbest_eval',
				'gbest_pos',
				'pbest_eval',
				'pbest_pos',
				'position',
				'evaluation',
				'velocity'
			])
		'''
		self.var_list = []
		_upper = []
		_lower = []
		for key in variables:
			if not variables[key].type == 3:
				self.var_list.append(key)
				_lower.append(variables[key].range[0])
				_upper.append(variables[key].range[-1])
			else:
				pass
		self.dimensions = len(var_list)
		self.pswarm = Swarm(particles, dimensions)
		_upper = np.array(_upper)
		_lower = np.array(_lower)
		self.lower = np.repeat(_lower[np.newaxis], self.particles, axis=0)
		self.upper = np.repeat(_upper[np.newaxis], self.particles, axis=0)
		self.v_limit = (self.upper - self.lower) / 2
		self.pswarm.initiate(lower, upper)

	def optimize(self, iterations, obj_func):
		'''
		for iterations
			for particles
				pre-process the variables, run obj_func
				update pbest
			update gbest
			record history
			update velocity, position
		'''
		time_init = time.time()
		# do optimization
		for i in range(iterations):
			time_start = time.time()
			# get evaluation
			_evaluation = []
			for j in range(self.particles):
				obj_in = self.pre_process(j)
				p_eval = obj_func(obj_in)
				_evaluation.append(p_eval)
			self.pswarm.evaluation = np.array(_evaluation)

			# update pbest
			if i == 0:
				self.pswarm.pbest_eval = self.pswarm.evaluation.copy()
			else:
				for j in range(self.particles):
					if self.pswarm.evaluation[j] < self.pswarm.pbest_eval[j]:
						self.pswarm.pbest_eval[j] = self.pswarm.evaluation[j]
						self.pswarm.pbest_pos[j] = self.pswarm.position[j]
					else:
						pass

			# update gbest
			self.pswarm.gbest_eval = self.pswarm.pbest_eval.min(axis=0)
			self.pswarm.gbest_pos = self.pswarm.pbest_pos[self.pswarm.pbest_eval.argmin(axis=0)]

			# update velocity & position
			self.update_swarm(iterations, i)

			# post process the data of the value
			self.post_process()

			# print iteration result / record history
			time_consume = time.time() - time_start
			print("Iteration {}/{}: best position: {}; best evaluation: {}; time consume: {}.".format(
				i, iterations, self.pswarm.gbest_pos, self.pswarm.gbest_eval, time_consume))
		# print result
		time_total = time.time() - time_init
		print("---------------Optimization Done---------------")
		print("Best position: {}".format(self.pswarm.gbest_pos))
		print("Best evaluation: {}".format(self.pswarm.gbest_eval))
		print("Total time: {}".format(self.pswarm.time_total))

			
	def pre_process(self, p_num):
		'''
		Process the values of variables that the algorithm generate.
		For continuous value, find the value and add to the list;
		For discrete value, approximate the value to the set;
		For constant value, add to the list.
		
		Parameter
		---------
		p_num : int
			indicate the particle number and used to refer values in position

		Return
		------
		obj_in : list of dual-tuple (var_name,var_value)
			The first index of the tuple is the variable's name.
			The second index of the tuple is the variable's value.
		'''
		obj_in = []
		for i in variables:
			if variables[i].type == 1:
				index = self.var_list.index(i)
				obj_in.append((i,self.swarm.position[p_num][index]))
			elif variables[i].type == 2:
				index = self.var_list.index(i)
				value = self.swarm.position[p_num][index]
				for j in range(len(variables[i].range)-1):
					if variables[i].range[j] < value and variables[i].range[j+1] > value:
						if (value - variables[i].range[j]) <= (variables[i].range[j+1] - value):
							value = variables[i].range[j]
						else:
							value = variables[i].range[j+1]
					else:
						pass
				obj_in.append((i,value))
			else:
				obj_in.append((i,variables[i].value))

		return obj_in

	def update_swarm(self, iterations, current_iter):
		'''
		Update the velocity and position of the swarm.
		First, calculate the neighbour of each particle using cKDTree. Before calculating distances
		between particles, different dimensions of the position need to be standardized.
		Second, calculate the local best of each particle.
		Finally, update the velocity and position basing on:
			v(t+1) = w * v(t) + c1 * rand() * (pbest-x) + c2 * rand() * (lbest-x)
			x(t+1) = x(t) + v(t)
			c1 = c2 = 2
			w = (w_init - w_end) * (iteration - current_iter) / iteration + w_end, where w_init = 0.9, w_end = 0.4
		Bound exceeding handling: 
			v_{i}(t+1) = v^_{i}(t+1) if |v^_{i}(t+1)| < v_{i}_limit else v_{i}_limit or -v_{i}_limit
			x_{i}(t+1) = x^_{i}(t+1) if lower < x^_{i}(t+1) < upper else lower or upper
				where v^ and x^ mean the temp value and i means the ith dimension.

		Attributes
		----------
		iterations : int
			the total iterations of the algorithm, used for calculating w.
		current_iter : int
			the current iteration, used for calculating w.
		'''
		# standardize the position, std_pos = pos/baseline
		std_pos = self.pswarm.position.copy()
		for i in range(self.dimensions):
			for j in range(self.particles):
				std_pos[j][i] = std_pos[j][i] / variables[self.var_list[i]].value

		# use cKDTree to get neighbour
		tree = cKDTree(std_pos)
		_, nb_index = tree.query(std_pos, k=self.neighbour, p=2)

		# calculate local_best
		if k == 1:
			local_best = self.pswarm.pbest_pos
		else:
			index_min = self.pswarm.pbest_eval[nb_index].argmin(axis=1)
			local_best = self.pswarm.pbest_pos[nb_index[np.arange(self.particles), index_min]]

		# update veloctiy
		w = 0.5 * (iterations - current_iter) / iterations + 0.4
		cognitive = 2 * np.random.uniform(0, 1, (self.particles, self.dimensions))
					  * (self.pswarm.pbest_pos - self.pswarm.position)
		social = 2 * np.random.uniform(0, 1, (self.particles, self.dimensions))
				   * (local_best - self.pswarm.position)
		temp_velocity = w * self.pswarm.veloctiy + cognitive + social
		'''
		# if velocity exceed the limit, don't change.
		mask = np.logical_and(temp_velocity >= -self.v_limit, temp_velocity <= self.v_limit)
		self.pswarm.veloctiy = np.where(mask, temp_velocity, self.pswarm.veloctiy)
		'''
		mask = temp_velocity >= -self.v_limit
		temp_velocity = np.where(mask, temp_velocity, -self.v_limit)
		mask = temp_velocity <= self.v_limit
		self.pswarm.velocity = np.where(mask, temp_velocity, self.v_limit)

		# update position
		temp_position = self.pswarm.position + self.pswarm.velocity
		mask = temp_position >= self.lower
		temp_position = np.where(mask, temp_position, self.lower)
		mask = temp_position <= self.upper
		self.pswarm.position = np.where(mask, temp_position, self.upper)

	def post_process(self):
		'''
		Approximate the discrete varialbes' value to their range.
		'''
		var_list_len = len(self.var_list)
		for i in range(var_list_len):
			temp_var = variables[self.var_list[i]]
			if temp_var.var_type == 2:
				for j in range(particles):
					_len = len(temp_var.var_range) - 1
					approximate = False
					for k in range(_len):
						if self.pswarm.position[j][i] <= (temp_var.var_range[k] + temp_var.var_range[k+1]) / 2:
							self.pswarm.position[j][i] = temp_var.var_range[k]
							approximate = True
					if not approximate:
						self.pswarm.position[j][i] = temp_var.var_range[-1]