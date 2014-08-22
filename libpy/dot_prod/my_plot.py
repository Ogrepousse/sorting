import numpy as np
import matplotlib.pyplot as plt

def trace(a, copy, cop2, med, mad, x = 0, y = 15000, nb = 0):

	c = np.arange(x, y)
	m = np.ones(y - x) * med
	mp = np.ones(y - x) * (med - 6 * mad)
	mm = np.ones(y - x) * (med + 6 * mad)
	plt.plot(c, copy)
	plt.plot(c, a)
	plt.plot(c, cop2)
	#plt.show()
	print('oui')
