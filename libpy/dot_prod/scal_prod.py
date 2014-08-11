import numpy as np
import scipy.io

#all_temp = scipy.io.loadmat('../files/ALL.templates')
#temp = all_temp['templates']

def get_temp():
	"""recupere les templates sur un fichier matlab"""
	all_temp = scipy.io.loadmat('../files/ALL.templates1')
	temp = all_temp['templates'].astype(np.float64)
	return (temp)

def select_ti(ti, blc, k, a):
	l = ti[np.where(ti <= blc[k])[0]]
	if k > 0:
		l = l[np.where(win > blc[k - 1])[0]]
	l = l[np.where((l > 64) & (l + 65 < a.shape[1]))]
	return (l)

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
	##	tmp = temp / np.sum(temp**2, axis = 0)**(1./2)
	#	l = l[np.where(l > 64)]
	#	l = l[np.where(l + 65 < a.shape[1])]
	#	si = np.empty((252, 129, l.shape[0]))
#voir si autre methode sans for
	#	for i in np.arange(l.shape[0]):
	#		si[:, :, i] = a[:, l[i] - 64 : l[i] + 65]
	#	btest = np.empty((l.shape[0], tmp.shape[2])
#		for j in np.arange(btest.shape[0]):
#			btest[i, j]
	return (bij)

def get_si(a, l):
#	win = np.array([np.arange(t - 64, t + 65) for t in l])
	si = a.T[np.array([np.arange(t - 64, t + 65) for t in l])].T
	return (si)

def dot_prod(tmp, si):
	for i in np.arange(tmp.shape[0]):
		t = np.dot(tmp[:, :, i].T, si.T)
