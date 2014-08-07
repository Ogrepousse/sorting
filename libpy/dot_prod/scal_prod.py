import numpy as np
import scipy.io

#all_temp = scipy.io.loadmat('../files/ALL.templates')
#temp = all_temp['templates']

def do_stuff(a, blc, ind):
	for k in np.arange(blc.shape[0] - 1):
		if k == 0:
			s = a[:, 0:blc[k]]
		else:
			s = a[:, blc[k - 1]:blc[k]]
