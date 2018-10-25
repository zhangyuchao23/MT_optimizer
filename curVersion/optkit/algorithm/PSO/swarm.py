'''
This module implements Swarm class.
'''
import numpy as np
from attr import attrs,attrib
from attr.validators import instance_of

@attrs
class Swarm:
	'''
	A Swarm Class

	This class represents a swarm of particles.

	Attributes
	----------
	particles : int
		number of particles in the swarm
	dimensions : int
		number of dimensions in the swarm
	position : numpy.ndarray of n-dimension list of float
		current position of every particle
	velocity : numpy.ndarray of n-dimension list of float
		current velocity of every particle
	evaluation : numpy.ndarray of float
		current evaluation of every position
	pbest_pos : numpy.ndarray of n-dimension list of float
		personal best position for every particle
	pbest_eval : numpy.ndarray of float
		personal best evaluation for every particle
	gbest_pos : numpy.ndarray of float
		the global best position of the swarm
	gbest_eval : float
		the global best evaluation of the swarm
	'''
	# need attribute
	particles = attrib(type=int, validator=instance_of(int))
	dimensions = attrib(type=int, validator=instance_of(int))
	# have default
	position = attrib(type=np.ndarray, default=np.array([]), validator=instance_of(np.ndarray))
	velocity = attrib(type=np.ndarray, default=np.array([]), validator=instance_of(np.ndarray))
	evaluation = attrib(type=np.ndarray, default=np.array([]), validator=instance_of(np.ndarray))
	pbest_pos = attrib(type=np.ndarray, default=np.array([]), validator=instance_of(np.ndarray))
	pbest_eval = attrib(type=np.ndarray, default=np.array([]), validator=instance_of(np.ndarray))
	gbest_pos = attrib(type=np.ndarray, default=np.array([]), validator=instance_of(np.ndarray))
	gbest_eval = attrib(type=float, default=np.inf, validator=instance_of(float,int))

	def initiate(self, lower, upper):
		'''
		Generate swarm's position & velocity.
		
		Parameters:
		upper : ndarray of float, size dimensions
			the upper bound of dimensions
		lower : ndarray of float, size dimensions
			the lower bound of dimensions
		'''
		self.position = np.random.uniform(low=lower, high=upper, size=(self.particles, self.dimensions))
		self.velocity = (upper - lower) * np.random.random_sample(size=(self.particles, self.dimensions))
			- (upper - lower) / 2
		self.pbest_pos = self.position.copy()