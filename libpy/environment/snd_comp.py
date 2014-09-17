import numpy as np

def get_comp(temp):
	"""calcul the seconde component of the template"""

	comp = np.empty(temp.shape)
	for i in range(temp.shape[2]):
		t = temp[:, :, i]
		t1 = t[:, 1:]
		t2 = t[:, :temp.shape[1] - 1]
		comp[:, :temp.shape[1] - 1, i] = (t1 - t2).copy()
		comp[:, temp.shape[1] - 1, i] = 0
	return (comp)
