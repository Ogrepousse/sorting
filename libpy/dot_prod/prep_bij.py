import numpy as np
import time

def scal(t1, t2):
	res = np.sum(t1 * t2)
	return (res)

def omeg(temp, temp2):
	om = np.empty((temp.shape[2], temp.shape[2], 129 * 2 - 1))
	print(temp.shape[2])
	for j in range(temp.shape[2]):
		print(j)
		t1 = temp2[:, :, j]
		for i in range(temp.shape[2]):
			for k in range(129 * 2 - 1):
				t2 = np.zeros((temp.shape[0], 129))
				if k < 129 - 1:
#					t2[:, 129 - 1 - k:] = temp[:, 129 - 1 - k:, i]
					t2[:, 129 - 1 - k:] = temp[:, :k + 1, i]
				elif k > 129 - 1:
#					t2[:, :k - 129] = temp[:, :k - 129, i]
					t2[:, :257 - k] = temp[:, k - 128:, i]
				else:
					t2 = temp[:, :, i]
				om[j, i, k] = scal(t1, t2)
	return (om)

#def overlap(temp):
#	om = np.empty((temp.shape[2], temp.shape[2], 129 * 2 - 1), dtype = float64)
#	for i in range(temp.shape[2]):
#		t1 = temp[:,:,i]
#		for j in range(temp.shape[2]):
#			for k in range(129 * 2 - 1):
#				t2 = np.zeros((temp.shape[0], temp.shape[1]))
#				if k < 128:
#					t2[:, 128 - k:] = temp[:, :k + 1, j]
#				elif k > 128:
#					t2[:, :]

