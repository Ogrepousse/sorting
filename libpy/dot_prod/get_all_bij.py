import numpy as np
import scal_prod

def select_ti_bis(ti, blc, k, a):
	l = ti[np.where(ti <= blc[k, 1])[0]]
	if k > 0:
		l = l[np.where(l > blc[k, 0])[0]]
	if k == 0:
		l = l[np.where(l > 64)[0]]
	if k == blc.shape[0] - 1:
		l = l[np.where(l + 65 < a.shape[1])]
	return (l)


def get_all_time(ti, blc, a):
	all_l = np.zeros((blc.shape[0], ti.shape[0]), dtype = np.int64)
	size = np.empty(blc.shape[0])
	for i in range(all_l.shape[0]):
		l = select_ti_bis(ti, blc, i, a)
		all_l[i, :l.shape[0]] = l
		size[i] = l.shape[0]
	return (all_l, size)


def small_bij(big_bij, k, size):
	bij = big_bij[k, :size[k], :]
	return (bij)


def small_time(all_l, k, size):
	l = all_l[k, :size[k]]
	return (l)


def get_all_bij(blc, all_l, a, temp, size):

	big_bij = np.zeros((blc.shape[0], np.amax(size), temp.shape[2]))
	print('voila', big_bij.shape)
	for i in range(big_bij.shape[0]):
		l = all_l[i, :size[i]]
		bij = scal_prod.get_bij(a, l, temp)
		big_bij[i, :size[i], :] = bij
		print(bij.shape)
	return (big_bij)
