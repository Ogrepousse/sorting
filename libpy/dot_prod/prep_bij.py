import numpy as np

def omeg(temp):
	om = np.empty((temp.shape[2], temp.shape[2], 129)
	for j in range(temp.shape[2]):
		t1 = temp[:, :, j]
		for i in range(temp.shape[2]):
			for k in range(129):
				t2 = np.zeros(temp.shape[0], 129)
				t2[:, 
