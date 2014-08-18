import numpy as np

def scal(t1, t2):
	res = 0
#	for i in range(t1.shape[0]):
#		for j in range(t1.shape[1]):
#			res += t1[i, j] * t2[i, j]
	res = np.sum(t1 * t2)
	return (res)

def omeg(temp):
	om = np.empty((temp.shape[2], temp.shape[2], 129 * 2 - 1))
	print(temp.shape[2])
	for j in range(temp.shape[2]):
		print(j)
		t1 = temp[:, :, j]
		for i in range(temp.shape[2]):
			for k in range(129 * 2 - 1):
				t2 = np.zeros((temp.shape[0], 129))
				if k < 129:
					t2[:, 129 - 1 - k:] = temp[:, 129 - 1 - k:, i]
				elif k > 129:
					t2[:, :k - 129] = temp[:, :k - 129, i]
				else:
					t2 = temp[:, :, i][:, 0]
			om[j, i, k] = scal(t1, t2)
	return (om)
