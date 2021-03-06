import numpy as np
import matplotlib.pyplot as plt

def trace(a, copy, med, mad, x = 0, y = 15000, nb = 0):
	"""trace le signal pour une electrode donnee"""

	b = a[nb, x:y]
	cop = copy[nb, x:y]
	c = np.arange(x, y)
	m = np.ones(y - x) * med[nb]
	mp = np.ones(y - x) * (med[nb] - 6 * mad[nb])
	mm = np.ones(y - x) * (med[nb] + 6 * mad[nb])
	plt.plot(c, cop, c, b, c, m, c, mp, c, mm)
#	plt.axvline(x = 1389)
#	plt.axvline(x = 500 + 129)
#	plt.axvline(x = 500 - 129)
