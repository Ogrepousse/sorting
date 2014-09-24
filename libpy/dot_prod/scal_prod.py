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
	a[:, l[c[0]] - 64 : l[c[0]] + 65] -= aij * temp[:, :, c[1]] + alpha * comp2[:, :, c[1]]
#	print(a.shape)
#	x = np.arange(a.shape[1])
#	plt.plot(x, a[99], x, b[99])
#
#	plt.show()



def part_aij(t_env, bij, a, exploration, bij_bool, l, beta_ij, div, k, b):
	"""get i and for max value of bij, then check if aij value is correct"""

	c = get_max(bij, exploration, bij_bool)
	bij_bool[c] = True
	aij = bij[c] / t_env.norme[c[1]]
	alpha = beta_ij[c] / t_env.norme2[c[1]]
	limit = t_env.amp_lim[:, c[1]]
	win = t_env.win_over
	if aij > limit[0] and aij < limit[1]:
		if (l[c[0]] < div[k, 1] - win) and (l[c[0]] > div[k, 0] + win):
			substract_signal(a, l, aij, t_env.temp2, c, alpha, t_env.comp2, limit, b)
			maj_scalar(c, bij, beta_ij, t_env.overlap, l, aij, alpha)
		return (1)
	else:
		exploration[c[0]] += 1
		if exploration[c[0]] >= 3:
			bij_bool[c[0], :] = True
		return (0)


def maj_scalar(c, bij, beta_ij, omeg, l, aij, alpha):
	"""recalculate the value of bij and beta_ij with the precacultate matric overlap"""

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

	ome = omeg[:, c[1], :]
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



def browse_block(t_env, a, blc, ti, div):
	"""browse all block in order to apply the fitting"""

	#recuperation des templates, seconde composante, limite haute et basse, matrice d'overlap
	temp = t_env.temp
	temp2 = t_env.temp2
	comp = t_env.comp
	comp2 = t_env.comp2
	norme = t_env.norme
	norme2 = t_env.norme2
	amp_lim = t_env.amp_lim
	omeg = t_env.overlap
	print('overlap recupere')

	#precalcul de tout les temps de spike et des bij pour chaque bloc
	al = t_env.al
	size = t_env.size
	big_bij = t_env.big_bij
	big_beta = t_env.big_beta
	b = a.copy()

	print('parcours', blc.shape[0])
	#parcours des blocs
	for k in range(blc.shape[0]):
		print('entre block', k)
		l = small_time(al, k, size)
		exploration = np.zeros(l.shape[0])
		bij = small_bij(big_bij, k, size)
		beta_ij = small_bij(big_beta, k, size)
		bij_bool = np.zeros(bij.shape, dtype = bool)
		while is_explored(exploration, bij_bool):
			part_aij(t_env, bij, a, exploration, bij_bool, l, beta_ij, div, k, b)
