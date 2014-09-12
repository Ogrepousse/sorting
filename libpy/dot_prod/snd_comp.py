import numpy as np

def get_comp(temp):
	comp = np.empty(temp.shape)
	for i in range(temp.shape[2]):
		t = temp[:, :, i]
		t1 = t[:, 1:]
		t2 = t[:, :129 - 1]
		comp[:, :129 - 1, i] = (t1 - t2).copy()
		comp[:, 128, i] = 0
	return (comp)

