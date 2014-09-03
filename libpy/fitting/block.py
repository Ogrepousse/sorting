import numpy as np

def get_mad(a, med):
	"""fonction qui calcul le seuil de tolerance
	prend les donnees a en parametre et la mediane"""
#	mean = a.sum(axis = 1) / a.shape[1]
#	med = cal_median(a)
	diff = (a - med[:, np.newaxis])**2
#	sq_diff = np.sqrt(diff).astype(np.int64)
	sq_diff = np.sqrt(diff)
	#mad = cal_median(sq_diff)
	mad = np.median(sq_diff, axis = 1)
	return (mad)


#pas necessaire il existe deja une fct numpy
def cal_median(a):
	"""calcul la mediane"""
	median = np.sort(a, axis = 1)[:, a.shape[1] / 2]
	return (median)


def ct_bis(a, median, mad):
	"""verification du depassement de seuil pour un spike
	et minimum local"""
	b1 = (a.T < median - 6 * mad).T
	b2 = a[:, :a.shape[1] - 1] < a[:, 1:]
	b3 = a[:, 1:] < a[:, :a.shape[1] - 1]
	b1[:, :a.shape[1] - 1] = b1[:, :a.shape[1] - 1] & b2
	b1[:, 1:] = b1[:, 1:] & b3
	return (b1)


def get_spike(a, x = 0, y = 0):
	"""renvoi un tableau de boolean pour chaque instant s'il y a eu un spike qui satisfait les criteres de selection ou non"""
	median = cal_median(a)
	mad = get_mad(a, median)
	spike_list = np.sum(ct_bis(a, median, mad), axis = 0)
##peut etre ignore
	spike_list[np.where(spike_list > 0)[0]] = 1
	return (spike_list)


def seperate_time(sp):
	"""renvoi les dates ou il y a eu un spike"""
	ind = np.where(sp > 0)[0]
	return (ind)


def get_block(sp):
	"""renvoi les dates de spike qui marquent la fin d'un block"""
	ind = seperate_time(sp)
	blc = np.zeros(ind.shape[0], dtype = np.int64)
	blc[:blc.shape[0] - 1] = ind[1:] - ind[: ind.shape[0] - 1]
	x = blc < 130
	ind[x] = 0
	ind[ind.shape[0] - 1] = sp.shape[0] - 1
	ind = ind[np.where(ind != 0)[0]]
	return (ind)


def divide_block(blc):
	t = 0
	div = np.zeros(blc[-1] / 100 + 1)
	index = 0
	for k in blc:
		while k - t > 100:
			t += 100
			div[index] = t
			index += 1
		div[index] = k
		index += 1
		t = k
	div = div[np.where(div)]
	return (div)
