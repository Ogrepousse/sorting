import numpy as np
import scipy.io

#all_temp = scipy.io.loadmat('../files/ALL.templates')
#temp = all_temp['templates']

def get_temp():
	all_temp = scipy.io.loadmat('../files/ALL.templates1')
	temp = all_temp['templates'].astype(np.float64)
	return (temp)

def do_stuff(a, blc, ti):
	bij = np.arange(0)
	temp = get_temp()
	for k in np.arange(blc.shape[0]):
		l = ti[np.where(ti <= blc[k])[0]]
		if k > 0:
			l = l[np.where(l > blc[k - 1])[0]]
		bij = np.zeros((l.shape[0], temp.shape[2]))
		for i in np.arange(bij.shape[0]):
			if l[i] > 64 and l[i] + 65 < a.shape[1]:
				si = a[:, l[i] - 64 : l[i] + 65]
				for j in np.arange(temp.shape[2]):
					tmp = temp[:, :, j]
					tmp = tmp / np.linalg.norm(tmp)
					bij[i,j] = np.sum(si * tmp)
#optimisation necessaire
				tmp = tmp
				btest = 
	return(bij)
