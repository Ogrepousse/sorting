import numpy as np
import matplotlib.pyplot as plt

def trace(a, copy, x = 0, y = 15000, nb = 0):
	"""trace le signal pour une electrode donnee"""

	b = a[nb, x:y]
	cop = copy[nb, x:y]
	c = np.arange(x, y)
	plt.plot(c, cop, c, b)
