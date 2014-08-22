import numpy as np

def scal(t1, t2):
	res = np.sum(t1 * t2)
	return (res)

def omeg(temp):
	om = np.empty((temp.shape[0], temp.shape[0], 129 * 2 - 1))
	print(temp.shape[0])
	for j in range(temp.shape[0]):
		print(j)
		t1 = temp[j, :]
		for i in range(temp.shape[0]):
			for k in range(129 * 2 - 1):
				t2 = np.zeros(129)
				if k < 129 - 1:
#					t2[:, 129 - 1 - k:] = temp[:, 129 - 1 - k:, i]
					t2[129 - 1 - k:] = temp[i, :k + 1]
				elif k > 129 - 1:
#					t2[:, :k - 129] = temp[:, :k - 129, i]
					t2[:257 - k] = temp[i, k - 128:]
				else:
					t2 = temp[i, :]
				om[j, i, k] = scal(t1, t2)
	#################erreur indent####################"""
	return (om)
