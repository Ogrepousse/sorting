import numpy as np

def get_mad(a, med):
	"""fonction qui calcul le seuil de tolerance
	prend les donnees a en parametre et la mediane"""

	diff = (a - med[:, np.newaxis])**2
	sq_diff = np.sqrt(diff)
	mad = np.median(sq_diff, axis = 1)
	return (mad)


#pas necessaire il existe deja une fct numpy
def cal_median(a):
	"""calcul la mediane"""

	median = np.sort(a, axis = 1)[:, a.shape[1] / 2]
	return (median)


def ct_bis(env, a, median, mad):
	"""verification du depassement de seuil pour un spike
	et minimum local"""

	b1 = (a.T < median -  env.threshold * mad).T
	b2 = a[:, :a.shape[1] - 1] < a[:, 1:]
	b3 = a[:, 1:] < a[:, :a.shape[1] - 1]
	b1[:, :a.shape[1] - 1] = b1[:, :a.shape[1] - 1] & b2
	b1[:, 1:] = b1[:, 1:] & b3
	return (b1)


def get_spike(env, a, x = 0, y = 0):
	"""renvoi un tableau de boolean pour chaque instant s'il y a eu un spike qui satisfait les criteres de selection ou non"""

	median = cal_median(a)
	mad = get_mad(a, median)
	spike_list = np.sum(ct_bis(env, a, median, mad), axis = 0)
##peut etre ignore
	spike_list[np.where(spike_list > 0)[0]] = 1
	return (spike_list)


def seperate_time(sp):
	"""renvoi les dates ou il y a eu un spike"""

	ind = np.where(sp > 0)[0]
	return (ind)


def get_block(env, sp, ti):
	"""renvoi les dates de spike qui marquent la fin d'un block"""

	ind = ti.copy()
	blc = np.zeros(ind.shape[0], dtype = np.int64)
	blc[:blc.shape[0] - 1] = ind[1:] - ind[: ind.shape[0] - 1]
	x = blc < env.space_block
	ind[x] = 0
	ind[ind.shape[0] - 1] = sp.shape[0] - 1
	ind = ind[np.where(ind != 0)[0]]
	return (ind)


def divide_block(env, blc):
	"""divise les bloc si leur taille est trop grande"""

	t = 0
	size = env.size_block
	div = np.zeros(blc[-1] / size + 1)
	index = 0
	for k in blc:
		while k - t > size:
			t += size
			div[index] = t
			index += 1
		div[index] = k
		index += 1
		t = k
	div = div[np.where(div)]
	return (div)


def	begin_end(env, blc):
	"""renvoi un array a deux dimmensio contenant les dates de debut et de fin de chaque bloc"""

	b_e = np.empty((blc.shape[0], 2))
	inf = 0
	p = 0
	win = env.win_over
	b_e[0, 0] = inf
	if blc[0] + win <= blc[-1]:
		b_e[0, 1] = blc[0] + win
	else:
		b_e[0, 1] = blc[-1]
	if blc.shape[0] == 1:
		b_e[0, 1] = blc[0]
		return (b_e)
	for k in range(1, blc.shape[0] - 1):
		inf = blc[k - 1] - win
		b_e[k, 0] = inf
		if blc[k] + win <= blc[-1]:
			b_e[k, 1] = blc[k] + win
		else:
			b_e[k, 1] = blc[-1]
	b_e[blc.shape[0] - 1, 0] = blc[-2] - win
	b_e[blc.shape[0] - 1, 1] = blc[-1]
	neg = np.where(b_e < 0)[0]
	if neg.shape[0]:
		b_e = b_e[neg[-1]:]
		b_e[0, 0] = 0
	return (b_e)
