import numpy as np

def scal(t1, t2):
	res = np.sum(t1 * t2)
	return (res)

def omeg(temp, temp2):
	n = 2
	om = np.empty((n, n, 129 * 2 - 1))
	for j in range(n):
		print(j)
		t1 = temp2[:, :, j]
		for i in range(n):
			for k in range(129 * 2 - 1):
				t2 = np.zeros((temp.shape[0], 129))
				if k < 129 - 1:
					t2[:, 129 - 1 - k:] = temp[:, :k + 1, i]
				elif k > 129 - 1:
					t2[:, :257 - k] = temp[:, k - 128:, i]
				else:
					t2 = temp[:, :, i]
				om[j, i, k] = scal(t1, t2)
	return (om)




def omeg_bis(temp, temp2, comp, comp2):
	om = np.empty((temp.shape[2] * 2, temp.shape[2] * 2, 129 * 2 - 1))
	print(temp.shape[2] * 2)
	for j in range(temp.shape[2] * 2):
		print(j)
		if j < temp.shape[2]:
			t1 = temp2[:, :, j]
		else:
			t1 = comp2[:, :, j - temp.shape[2]]
		for i in range(temp.shape[2] * 2):
			if i < temp.shape[2]:
				tmp = temp[:, :, i]
			else:
				tmp = comp[:, :, i - temp.shape[2]]
			for k in range(129 * 2 - 1):
				t2 = np.zeros((temp.shape[0], 129))
				if k < 129 - 1:
					t2[:, 129 - 1 - k:] = tmp[:, :k + 1]
				elif k > 129 - 1:
					t2[:, :257 - k] = tmp[:, k - 128:]
				else:
					t2 = tmp
				om[j, i, k] = scal(t1, t2)
	return (om)
