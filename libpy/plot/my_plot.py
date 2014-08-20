import numpy as np
import matplotlib.pyplot as plt

def trace(a, copy, med, mad, x = 0, y = 15000, nb = 0):

	b = a[nb, x:y]
	cop = copy[nb, x:y]
	c = np.arange(x, y)
	m = np.ones(y - x) * med[nb]
	mp = np.ones(y - x) * (med[nb] - 6 * mad[nb])
	mm = np.ones(y - x) * (med[nb] + 6 * mad[nb])
	print(b.shape, c.shape)
	plt.plot(c, cop, c, b, c, m, c, mp, c, mm)
	#plt.show()
	print('oui')
