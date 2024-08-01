#FeedForward Neural Network
import numpy as np
import random
from . import functions

class FNN():
	def __init__(self, num_neurons, activation=functions.sigmoid()):
		self.num_neurons=num_neurons
		self.num_layers=len(num_neurons)
		self.acfunc=activation
		self.reset()

	def compute_oup(self,inp):
		tmpinp=inp
		for bi,wei in zip(self.bias,self.weights):
			tmpinp=self.acfunc.f(np.dot(wei,tmpinp)+bi)
		return tmpinp

	def reset(self):
		self.bias=[np.random.randn(size,1) for size in self.num_neurons[1:]]
		self.weights=[np.random.randn(size2,size1)/np.sqrt(size1) for size1,size2 in zip(self.num_neurons[:-1],self.num_neurons[1:])]

	def setBias(self,bias):
		self.bias=bias
		
	def setWeights(self,weights):
		self.weights=weights
