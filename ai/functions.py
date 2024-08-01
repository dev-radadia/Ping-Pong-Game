import numpy as np
class sigmoid():
	def f(self,z):
		return 1.0/(1.0+np.exp(-z))
	def fp(self,z):
		return self.f(z)*(1.0-self.f(z))

class elu():
	def __init__(self,alpha):
		self.alpha=alpha
	def f(self,z):
		# return z if z>=0 else self.alpha*(np.exp(z)-1)
		return np.where(z>0,z,self.alpha*(np.exp(z)-1))
	def fp(self,z):
		# return 1 if z>0 else self.alpha*np.exp(z)
		return np.where(z>0,1,self.alpha*np.exp(z))