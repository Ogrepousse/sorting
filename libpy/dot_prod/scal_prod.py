import numpy as np
import scipy.io
import sys
import matplotlib.pyplot as plt


def small_bij(big_bij, k, size):
	"""return bij for a given bloc"""

	bij = big_bij[k, :size[k], :]
	return (bij)


def small_time(all_l, k, size):
	"""return an array of the spike time in a given block"""

	l = all_l[k, :size[k]]
	return (l)


def is_explored(exploration, bij_bool):
	"""return 0 if all the time have been explored, return 1 otherwise"""

	if np.all(exploration == 3):
		return (0)
	if np.all(bij_bool == True):
		return (0)
	return (1)


def get_max(bij, exploration, bij_bool):
	"""return a tuple with the coordinates of the max value of bij, tuples (i, j) already visited and time i explored are ignored"""

	bij[bij_bool] = -sys.maxint - 1
	c = np.unravel_index(bij.argmax(), bij.shape)

############################## A MODIFIER EVENTUELLEMENT #################
#	b = bij[bij_bool]
#	m = b.argmax()
#	ind = np.unravel_index(m, b.shape)
#	c = np.where(bij == b[ind])
#	c = (c[0][0], c[1][0])
#	print('mMAXx', bij[c])
	return (c)


def substract_signal(a, l, aij, temp, c, alpha, comp2, limit, b):
	"""substract the template to the signal"""
#	alpha = 0
	a[:, l[c[0]] - 64 : l[c[0]] + 65] -= aij * temp[:, :, c[1]] + alpha * comp2[:, :, c[1]]


def part_aij(t_env, bij, a, exploration, bij_bool, l, beta_ij, div, k, b, b_save, b_prec):
	"""get i and for max value of bij, then check if aij value is correct"""

	c = get_max(bij, exploration, bij_bool)
	bij_bool[c] = True
	aij = bij[c] / t_env.norme[c[1]]
	alpha = beta_ij[c] / t_env.norme2[c[1]]
	limit = t_env.amp_lim[:, c[1]]
	win = t_env.win_over
	if aij > limit[0] and aij < limit[1]:
		if (l[c[0]] < div[k, 1] - win) and (l[c[0]] > div[k, 0] + win):
			aij = bij[c]
			t_env.fdout.write(str(aij) + ' ' + str(c[1]) + ' ' + str(l[c[0]] + t_env.index) + '\n')
			substract_signal(a, l, aij, t_env.temp, c, alpha, t_env.comp2, limit, b)
			maj_scalar(t_env, c, bij, beta_ij, l, aij, alpha)
		#	maj_scalar(t_env, c, b_save, beta_ij, l, aij, alpha)
		return (1)
	else:
		exploration[c[0]] += 1
		if exploration[c[0]] >= 3:
			bij_bool[c[0], :] = True
		return (0)


def maj_scalar(t_env, c, bij, beta_ij, l, aij, alpha):
	"""recalculate the value of bij and beta_ij with the precacultate matric overlap"""

	omeg_a = t_env.overlap_a
	omeg_b = t_env.overlap_b
	omeg_c = t_env.overlap_c
	omeg_d = t_env.overlap_d
	maj_bij(t_env, bij, c, aij, omeg_a, l)
	maj_bij(t_env, bij, c, alpha, omeg_b, l)
	maj_bij(t_env, beta_ij, c, aij, omeg_c, l)
	maj_bij(t_env, beta_ij, c, alpha, omeg_d, l)


def maj_bij(t_env, bij, c, aij, omeg, l):
	"""update the bij matrix with the precalculate matrix omeg"""


	len = t_env.temp_size
	ome = omeg[:, c[1], :]
	n1 = l < l[c[0]] + len
	n2 = l > l[c[0]] - (len)
	n = n1 & n2
	l2 = l[n]
	linf = l2[l2 <= l[c[0]]]
	lsup = l2[l2 > l[c[0]]]
	t1 = np.where(np.in1d(l, linf) == True)[0]
	t2 = np.where(np.in1d(l, lsup) == True)[0]
	om_inf = ome[:, linf - l[c[0]] + (len - 1)]
	om_sup = ome[:, lsup - l[c[0]] + (len - 1)]
	bij[t1, :] = bij[t1, :] - aij * om_inf.T
	bij[t2, :] = bij[t2, :] - aij * om_sup.T


def get_bij(a, l, temp):
	"""calculate the matrix bij"""

#	print('obtention des bij')
#	print(l.shape)
#	r = np.arange(-64, 65).reshape(129, 1)
#	l2 = l.reshape(1, l.shape[0])
#	s = a[:, r + l2]
#	bij = np.tensordot(s[::], temp, ([0, 1], [0, 1]))

	bij = np.empty((l.shape[0], temp.shape[2]))
	s = np.empty((l.shape[0], a.shape[0], temp.shape[1]))
	for i in range(bij.shape[0]):
		si = a[:, l[i] - temp.shape[1] / 2 : l[i] + (temp.shape[1] / 2 + 1)]
		s[i, :, :] = si
	bij = np.tensordot(s[::], temp, 2)
	return (bij)



def browse_block(t_env, a, blc, ti, div):
	"""browse all block in order to apply the fitting"""
	### a supprimer ###
	b = a.copy()
	###################

	print('parcours', blc.shape[0])
	#parcours des blocs
	b_save = 0
	for k in range(blc.shape[0]):
		print('entre block', k)
		l = small_time(t_env.al, k, t_env.size)
		exploration = np.zeros(l.shape[0])
		bij = small_bij(t_env.big_bij, k, t_env.size)
		b_save = bij.copy()
		beta_ij = small_bij(t_env.big_beta, k, t_env.size)
		bij_bool = np.zeros(bij.shape, dtype = bool)
		bol = 0
		bij2 = bij
		while is_explored(exploration, bij_bool):
	#		if bol:
	#			bij = get_bij(a, l, t_env.temp)
			b_prec = bij2.copy()
			bol = part_aij(t_env, bij, a, exploration, bij_bool, l, beta_ij, div, k, b, b_save, b_prec)

