'''
This module implements Optimizer class.
'''
import time
from collections import namedtuple
from scipy.spatial import cKDTree
import numpy as np
from . import Swarm
from ...workflow import Continuous, Discrete, Constant

class PSO_Optimizer:
	def __init__(self, particles, neighbour, variables):
		'''
		Parameters
		----------
		particles : int
			the number of the particles in the swarm
		neighbour : int
			the size of a particle's neighbourhood
		variables : list of Variable
			the variables of the project

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
		var_list : list of Variable
			the list of input variables
		upper : ndarray of float, size dimensions
			the upper bound of each dimension
		lower : ndarray of float, size dimensions
			the lower bound of each dimension
		v_limit : ndarray of float, size dimensions
			the limit of velocity. set to (upper-lower)/2
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
		for var in variables:
			if not isinstance(var, Constant):
				self.var_list.append(var)
				_lower.append(var.var_range[0])
				_upper.append(var.var_range[-1])
			else:
				pass
		self.dimensions = len(self.var_list)
		self.pswarm = Swarm(self.particles, self.dimensions)
		_upper = np.array(_upper)
		_lower = np.array(_lower)
		self.lower = np.repeat(_lower[np.newaxis], self.particles, axis=0)
		self.upper = np.repeat(_upper[np.newaxis], self.particles, axis=0)
		self.v_limit = (self.upper - self.lower) / 40
		self.pswarm.initiate(self.lower, self.upper)
		self.post_process()

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
				for var_index in range(self.dimensions):
					self.var_list[var_index].value = self.pswarm.position[j][var_index]
				p_eval = obj_func()
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
		print("Total time: {}".format(time_total))
	
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
				std_pos[j][i] = std_pos[j][i] / self.var_list[i].baseline
		# use cKDTree to get neighbour 
		tree = cKDTree(std_pos)
		_, nb_index = tree.query(std_pos, k=self.neighbour, p=2)
		# calculate local_best
		if self.neighbour == 1:
			local_best = self.pswarm.pbest_pos
		else:
			index_min = self.pswarm.pbest_eval[nb_index].argmin(axis=1)
			local_best = self.pswarm.pbest_pos[nb_index[np.arange(self.particles), index_min]]

		# update veloctiy
		w = 0.5 * (iterations - current_iter) / iterations + 0.4
		cognitive = 2 * np.random.uniform(0, 1, (self.particles, self.dimensions)) \
					* (self.pswarm.pbest_pos - self.pswarm.position)
		social = 2 * np.random.uniform(0, 1, (self.particles, self.dimensions)) \
				 * (local_best - self.pswarm.position)
		temp_velocity = w * self.pswarm.velocity + cognitive + social
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
		Approximate the discrete variables' value to the set.
		'''
		for var_index in range(self.dimensions):
			if isinstance(self.var_list[var_index], Discrete):
				for p in range(self.particles):
					v = self.pswarm.position[p][var_index]
					self.pswarm.position[p][var_index] = self.var_list[var_index].var_range[-1]
					for set_index in range(len(self.var_list[var_index].var_range)):
						if v <= self.var_list[var_index].var_range[set_index]:
							if set_index == 0:
								self.pswarm.position[p][var_index] = self.var_list[var_index].var_range[0]
								break
							else:
								if (v - self.var_list[var_index].var_range[set_index-1]) < \
									(self.var_list[var_index].var_range[set_index] - v):
									self.pswarm.position[p][var_index] = self.var_list[var_index].var_range[set_index-1]
									break
								else:
									self.pswarm.position[p][var_index] = self.var_list[var_index].var_range[set_index]
									break
						else:
							pass
			else:
				pass