import numpy as np
import random
from ai.fnn import *
from ai import functions

class QLearner():
	def __init__(self, num_actions, input_size):		
		self.num_actions=num_actions
		self.input_size=input_size

		self.brain= FNN([input_size,100,100,num_actions],activation=functions.elu(1.0))

	def updateIntent(self,state):
		biggest=-1000.0
		newAction=0

		qvals=self.brain.compute_oup(self.createBrainArray(state))

		for action in range(self.num_actions):
			if qvals[action][0]>biggest:
				biggest=qvals[action][0]
				newAction=action

		self.intent=newAction

	def quadraticCostDerivative(self, good, almostgood):
		return almostgood-good

	def createBrainArray(self,state):
		return np.asarray([[state[i]] for i in range(self.input_size)])

	def loadMemory(self, identifier):
		b=None
		w=None
		try:
			w=np.load(identifier+"_w.npy",allow_pickle=True)
			b=np.load(identifier+"_b.npy",allow_pickle=True)
		except IOError:
			print("No memory/bad memory found, creating fresh ones...\n")
			return

		self.brain.setBias(b)
		self.brain.setWeights(w)
	def getIntent(self):
		return self.intent