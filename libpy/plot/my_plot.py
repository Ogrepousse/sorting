import numpy as np
import matplotlib.pyplot as plt

def trace(a, copy, med, mad, x = 0, y = 15000, nb = 0):

	c = np.arange(x, y)
	m = np.ones(y - x) * med
	mp = np.ones(y - x) * (med - 6 * mad)
	mm = np.ones(y - x) * (med + 6 * mad)
	plt.plot(c, copy, c, a, c, m, c, mp, c, mm)
	#plt.show()
	print('oui')
