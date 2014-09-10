import numpy as np
import scipy.io
import sys
import prep_bij
import matplotlib.pyplot as plt
import snd_comp
import get_all_bij

#all_temp = scipy.io.loadmat('../files/ALL.templates')
#temp = all_temp['templates']

def get_temp():
	"""get templates from matlab file"""

	all_temp = scipy.io.loadmat('../files/ALL.templates1')
	temp = all_temp['templates'].astype(np.float64)
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
		l = l[np.where(l > blc[k - 1])[0]]
	if k == 0:
		l = l[np.where(l > 64)[0]]
	if k == blc.shape[0] - 1:
		l = l[np.where(l + 65 < a.shape[1])]
	return (l)


def normalize_temp(temp):
	"""normalize the templates and return an array with the value of all the norme"""

	norme = np.empty(temp.shape[2])
	for i in range(temp.shape[2]):
		norme[i] = np.linalg.norm(temp[:, :, i])
		temp[:, :, i] = temp[:, :, i] / norme[i]
	return (norme)


def calc_bij(temp, si):
	"""dot poduct for matrix"""

	res = np.sum(temp * si)
	return (res)


def get_bij(a, l, temp):
	"""calculate the matrix bij"""

#	print('obtention des bij')
	bij = np.empty((l.shape[0], temp.shape[2]))
#	print(l.shape)
	for i in range(bij.shape[0]):
		si = a[:, l[i] - 64 : l[i] + 65]
		for j in range(bij.shape[1]):
			bij[i, j] = calc_bij(si, temp[:, :, j])
	return (bij)


def is_explored(exploration, bij_bool):
	"""return 0 if all the time have been explored, return 1 otherwise"""

#	print(exploration)
	if np.all(exploration == 3):
		return (0)
	if np.all(bij_bool == True):
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


def substract_signal(a, l, aij, temp, c, predic, alpha, comp2):
	"""substract the template to the signal"""
	a[:, l[c[0]] - 64 : l[c[0]] + 65] -= aij * temp[:, :, c[1]] + alpha * comp2[:, :, c[1]]
#	predic[l[c[0]] - 64 : l[c[0]] + 65] += aij * temp[90, :, c[1]]


def part_aij(bij, norme, a, amp_lim, exploration, bij_bool, temp, l, omeg, temp2, predic, beta_ij, norme2, comp2, div, k):
	"""get i and for max value of bij, then check if aij value is correct"""

#	print('exploitation bij')
	c = get_max(bij, exploration, bij_bool)
	bij_bool[c] = True
	aij = bij[c] / norme[c[1]]
	alpha = beta_ij[c] / norme2[c[1]]
	limit = amp_lim[:, c[1]]
	win = 129
	if aij > limit[0] and aij < limit[1]:
		if (l[c[0]] < div[k, 1] - win) and (l[c[0]] > div[k, 0] + win):
			substract_signal(a, l, aij, temp2, c, predic, alpha, comp2)
			maj_scalar(c, bij, beta_ij, omeg, l, aij, alpha)
		#	maj_bij(bij, c, aij, omeg, l, beta_ij, alpha)
		return (1)
	else:
		exploration[c[0]] += 1
		return (0)


def maj_scalar(c, bij, beta_ij, omeg, l, aij, alpha):
	omeg_a = omeg[:bij.shape[1], :bij.shape[1], :]
	omeg_b = omeg[:bij.shape[1], bij.shape[1]:, :]
	omeg_c = omeg[bij.shape[1]:, :bij.shape[1], :]
	omeg_d = omeg[bij.shape[1]:, bij.shape[1]:, :]
	maj_bij(bij, c, aij, omeg_a, l)
	maj_bij(bij, c, alpha, omeg_b, l)
	maj_bij(beta_ij, c, aij, omeg_c, l)
	maj_bij(beta_ij, c, alpha, omeg_d, l)


def maj_bij(bij, c, aij, omeg, l):
	"""update the bij matrix with the precalculate matrix omeg"""

#	print('maj bij')
	ome = omeg[c[1], :, :]
	n1 = l < l[c[0]] + 129
	n2 = l > l[c[0]] - 128
	n = n1 & n2
	l2 = l[n]
	linf = l2[l2 <= l[c[0]]]
	lsup = l2[l2 > l[c[0]]]
	t1 = np.where(np.in1d(l, linf) == True)[0]
	t2 = np.where(np.in1d(l, lsup) == True)[0]
	om_inf = ome[:, linf - l[c[0]] + 128]
	om_sup = ome[:, lsup - l[c[0]] + 128]
	bij[t1, :] = bij[t1, :] - aij * om_inf.T
	bij[t2, :] = bij[t2, :] - aij * om_sup.T


def get_overlap():
	tab = np.empty(764*764*257)
	size = 4096
	i = 0
	l = 764 * 764 * 257 * 8
	n = 0
	fd = open('omeg4', 'rb')
	while l - n > size:
		s = fd.read(size)
		tab[n / 8 : (n + size) / 8] = np.fromstring(s, dtype = np.float64)
		i += 1
		n += size
	s = fd.read(l - n)
#	print(i)
	tab[i * size / 8:] = np.fromstring(s, dtype = np.float64)
	fd.close()
	tab = tab.reshape(764, 764, 257)
	return (tab)


def browse_bloc(a, blc, ti, div):
	"""browse all block in order to apply the fitting"""

	b = 0
	predic = np.zeros(a.shape[1])
	temp = get_temp()
	temp2 = temp.copy()
	comp = snd_comp.get_comp(temp)
	comp2 = comp.copy()
	norme2 = normalize_temp(comp)
	norme = normalize_temp(temp)
	amp_lim = get_amp_lim()
	omeg = get_overlap()
	print('overlap recupere')

	(al, size) = get_all_bij.get_all_time(ti, div, a)
	print('size', size)
	print('ola', al.shape)
	big_bij = get_all_bij.get_all_bij(div, al, a, temp, size)
	big_beta = get_all_bij.get_all_bij(div, al, a, comp, size)

	print('parcours', blc.shape[0])
	for k in range(blc.shape[0]):
		print('entre block', k)
		l = get_all_bij.small_time(al, k, size)
	#	print('sapristi', l1.dtype)
	#	l = select_ti(ti, blc, k, a)
	#	print('diantre', l.dtype)
		exploration = np.zeros(l.shape[0])
	#	bij_bool = np.zeros((l.shape[0], temp.shape[2]), dtype = bool)
	#	print('top')
		bij = get_all_bij.small_bij(big_bij, k, size)
	#	bij = get_bij(a, l, temp)
		beta_ij = get_all_bij.small_bij(big_beta, k, size)
	#	beta_ij = get_bij(a, l, comp)
		bij_bool = np.zeros(bij.shape, dtype = bool)
	#	print('pot')
		while is_explored(exploration, bij_bool):
		#	if b:
		#		bij = get_bij(a, l, temp)
			b = part_aij(bij, norme, a, amp_lim, exploration, bij_bool, temp, l, omeg, temp2, predic, beta_ij, norme2, comp2, div, k)
