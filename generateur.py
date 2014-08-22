import numpy as np
import matplotlib.pyplot as plt

def gen():
	tri = np.array([0, 0, 0.25, 0.75, 1, 0.75, 0.25, 0, 0]) * -1
	sqr = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0]) * -1
	x = np.arange(200)
	noise = np.random.ranf(200) / 10
	noise[95:104] += tri
	noise[93: 102] += sqr
	return (noise)


#plt.plot(x, noise)
#plt.show()
