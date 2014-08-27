import numpy as np
import matplotlib.pyplot as plt

def gen(set):
	tri = np.array([0, 0, 0.25, 0.75, 1, 0.75, 0.25, 0, 0]) * -1
	dira = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0]) * -1
	sqr = np.array([0.5, 1, 1, 1, 1.5, 1, 1, 1, 0.5]) * -1
	x = np.arange(set)
#	noise = np.zeros(set)
	noise = np.random.ranf(set) / 10
	noise[95:104] += tri
	noise[83: 92] += dira
	noise[113:122] += sqr
	return (noise)
