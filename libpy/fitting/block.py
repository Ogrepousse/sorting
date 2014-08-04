import numpy as np

def make_block(a, x = 0, y = 1):
	median = np.sort(a, axis = 1)[:, a.shape[1] / 2]
	n = a - median[:, np.newaxis]
	print(n)
