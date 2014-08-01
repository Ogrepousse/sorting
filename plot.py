import numpy as np
import matplotlib.pyplot as plt

def trace(a, x = 0, y = 15000, nb = 0):

	b = a[nb, x:y]
	c = np.arange(x, y);
	plt.plot(c, b)
	plt.show()
	print('oui')
