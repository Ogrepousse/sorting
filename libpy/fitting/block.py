import numpy as np

def get_mad(a, med):
	"""fonction qui calcul le seuil de tolerance
	prend les donnees a en parametre et la mediane"""
#	mean = a.sum(axis = 1) / a.shape[1]
#	med = cal_median(a)
	diff = (a - med[:, np.newaxis])**2
	sq_diff = np.sqrt(diff).astype(np.int64)
	mad = cal_median(sq_diff)
	return (mad)

def cal_median(a):
	"""calcul la mediane"""
	median = np.sort(a, axis = 1)[:, a.shape[1] / 2]
	return (median)

#def check_thresh(a, median, mad, i):
#	"""renvoie un tableau de boolean pour les 252 electrodes
#	a l'instant i indiquant si le seuil de tolerance est depasse
#	par une electrode donnee et qu'il s'agit d'un minimum local"""
#	b1 = a[:, i] < median - 6 * mad
#	if i != a.shape[1] - 1:
#		b2 = a[:, i] < a[:, i + 1]
#	if i != 0:
#		b3 = a[:, i] < a[:, i - 1]
#	if i == 0:
#		b = b1 & b2
#	elif i == a.shape[1] - 1:
#		b = b1 & b3
#	else:
#		b = b1 & b2 & b3
#	return (b)

def ct_bis(a, median, mad):
	b1 = (a.T < median - 6 * mad).T
	b2 = a[:, :a.shape[1] - 1] < a[:, 1:]
	b3 = a[:, 1:] < a[:, :a.shape[1] - 1]
	b1[:, :a.shape[1] - 1] = b1[:, :a.shape[1] - 1] & b2
	b1[:, 1:] = b1[:, 1:] & b3
	return (b1)

def get_spike(a, x = 0, y = 0):
	"""renvoi un tableau de boolean pour chaque instant s'il y a eu un spike ou non"""
	median = cal_median(a)
	mad = get_mad(a, median)
	spike_list = np.sum(ct_bis(a, median, mad), axis = 0)
#	spike_list = np.zeros(y - x, dtype = np.int64)
#	i = x
#	while i < y:
#		c_t = check_thresh(a, median, mad, i)
#		if True in c_t:
#			spike_list[i - x] = 1
#		i += 1
	return (spike_list)

def seperate_time(sp):
	ind = np.where(sp == True)[0]
	return (ind)
