import numpy as np
import scipy.io
import sys
import prep_bij
import time
import my_plot
import matplotlib.pyplot as plt

#all_temp = scipy.io.loadmat('../files/ALL.templates')
#temp = all_temp['templates']

def get_temp():
	"""get templates from matlab file"""


	tri = np.array([0, 0, 0.25, 0.75, 1, 0.75, 0.25, 0, 0]) * -1
	sqr = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0]) * -1
	s1 = np.zeros(129)
	s1[64 - 4: 64 + 5] += tri
	s2 = np.zeros(129)
	s2[64 - 4: 64 + 5] += sqr
	temp = np.array([s1, s2])
	#all_temp = scipy.io.loadmat('../files/ALL.templates1')
	#temp = all_temp['templates'].astype(np.float64)
	return (temp)


def get_amp_lim():
	"""recupere les limites hautes et basses des templates depuis un fichier matlab"""

	amp_lim = scipy.io.loadmat('../files/ALL.templates1')['AmpLim'].astype(np.float64)
#	amp_lim = (amp_lim / 0.01) + 32767
	return (amp_lim)


def select_ti(ti, blc, k, a):
	"""
	recupere les temps de spike ds le block en excluant les spikes extremes n'ayant pas assez de points autour pour les produits scalaires"""

	l = ti[np.where(ti <= blc[k])[0]]
	if k > 0:
		l = l[np.where(win > blc[k - 1])[0]]
	l = l[np.where((l > 64) & (l + 65 < a.shape[0]))]
	return (l)


def normalize_temp(temp):
	"""normalize the templates and return an array with the value of all the norme"""

	norme = np.empty(temp.shape[0])
	for i in range(temp.shape[0]):
		norme[i] = np.linalg.norm(temp[i, :])
		temp[i, :] = temp[i, :] / norme[i]
	return (norme)


def calc_bij(temp, si):
	"""dot poduct for matrix"""

	res = np.sum(temp * si)
	return (res)


def get_bij(a, l, temp):
	"""calculate the matrix bij"""

	print('obtention des bij')
	bij = np.empty((l.shape[0], temp.shape[0]))
	for i in range(bij.shape[0]):
		si = a[l[i] - 64 : l[i] + 65]
		for j in range(bij.shape[1]):
			bij[i, j] = calc_bij(si, temp[j,:])
	return (bij)


def is_explored(exploration, bij_bool):
	"""return 0 if all the time have been explored, return 1 otherwise"""

#	print(exploration)
	if np.all(exploration == 3):
		print('A')
		return (0)
	if np.all(bij_bool == True):
		print('B')
		return (0)
	return (1)


def get_max(bij, exploration, bij_bool):
	"""return a tuple with the coordinates of the max value of bij, tuples (i, j) already visited and time i explored are ignored"""

	bij[bij_bool] = -sys.maxint - 1
	bij[exploration >= 3, :] = -sys.maxint - 1
	c = np.unravel_index(bij.argmax(), bij.shape)

############################## A MODIFIER EVENTUELLEMENT #################
#	b = bij[bij_bool]
#	m = b.argmax()
#	ind = np.unravel_index(m, b.shape)
#	c = np.where(bij == b[ind])
#	c = (c[0][0], c[1][0])
#	print('mMAXx', bij[c])
	return (c)


def substract_signal(a, l, aij, temp, c, predic):
	"""substract the template to the signal"""
	a[l[c[0]] - 64 : l[c[0]] + 65] -= aij * temp[c[1], :]
	predic[l[c[0]] - 64 : l[c[0]] + 65] += aij * temp[c[1], :]



def part_aij(bij, norme, a, amp_lim, exploration, bij_bool, temp, l, omeg, temp2, predic, copy):
	"""get i and for max value of bij, then check if aij value is correct"""

#	print('exploitation bij')
	c = get_max(bij, exploration, bij_bool)
	print('c = ', c)
	bij_bool[c] = True
	aij = bij[c] / norme[c[1]]
	print('aij = ', aij)
	limit = amp_lim[0]
	if aij > limit[0] and aij < limit[1]:
		substract_signal(a, l, aij, temp2, c, predic)
		print('lol')
	#	maj_bij(bij, c, aij, omeg, l)
		my_plot.trace(a, predic, copy, 0, 0, y = 200)
		plt.show()
		return (1)
	else:
		exploration[c[0]] += 1
		return (0)


def maj_bij(bij, c, aij, omeg, l):
	"""update the bij matrix with the precalculate matrix omeg"""

	print('maj bij')
	print(c)
	ome = omeg[c[1], :, :]
	n1 = l < l[c[0]] + 129
	n2 = l > l[c[0]] - 128
	print(l)
	print(n1, n2)
	n = n1 & n2
	l2 = l[n]
	linf = l2[l2 <= l[c[0]]]
	lsup = l2[l2 > l[c[0]]]
	t1 = np.where(np.in1d(l, linf) == True)[0]
	t2 = np.where(np.in1d(l, lsup) == True)[0]
	print(t1, t2)
	om_inf = ome[:, linf - l[c[0]] + 128]
	om_sup = ome[:, lsup - l[c[0]] + 128]
	print('###############')
	print(aij * om_inf.T)
	print(aij * om_sup.T)
	bij[t1, :] = bij[t1, :] - aij * om_inf.T
	bij[t2, :] = bij[t2, :] - aij * om_sup.T


def browse_bloc(a, blc, ti):
	"""browse all block in order to apply the fitting"""

	b = 1
	copy = a.copy()
	predic = np.zeros(a.shape[0])
	temp = get_temp()
	temp2 = temp.copy()
	print('temp.shape = ', temp.shape)
	norme = normalize_temp(temp)
	print('norme = ', norme)
	amp_lim = np.array([[0.8, 1.5]])
	omeg = np.loadtxt('omeg3').reshape(temp.shape[0], temp.shape[0], 257)
#	omeg = 0
	for k in range(blc.shape[0]):
		print('entre block')
		l = select_ti(ti, blc, k, a)
		print(l)
		exploration = np.zeros(l.shape[0])
		bij_bool = np.zeros((l.shape[0], temp.shape[0]), dtype = bool)
		print('top')
		bij = get_bij(a, l, temp)
	#	print('bij = ', bij)
		print('pot')
		while is_explored(exploration, bij_bool):
		#	time.sleep(5)
			print('expl = ', exploration)
			if b:
				bij = get_bij(a, l, temp)
				print(bij, bij_bool)
			print(bij)
			b = part_aij(bij, norme, a, amp_lim, exploration, bij_bool, temp, l, omeg, temp2, predic, copy)
