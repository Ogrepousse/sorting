import numpy as np
import env_fct

def select_ti_bis(env, a, ti, div, k):
	"""get the spike time in a bloc excluding extrem spike"""

	l = ti[np.where(ti <= div[k, 1])[0]]
	if k > 0:
		l = l[np.where(l > div[k, 0])[0]]
#	if k == 0:
	l = l[np.where(l > env.temp_size / 2)[0]]
#	if k == div.shape[0] - 1:
	l = l[np.where(l + env.temp_size / 2 + 1 < a.shape[1])]
	return (l)


def get_all_time(env, a, ti, div):
	"""return a two dimensionnal array with all the spike for each bloc"""

	all_l = np.zeros((div.shape[0], ti.shape[0]), dtype = np.int64)
	size = np.empty(div.shape[0])
	for i in range(all_l.shape[0]):
		l = select_ti_bis(env, a, ti, div, i)
#		print('fill', l)
		all_l[i, :l.shape[0]] = l
		size[i] = l.shape[0]
	return (all_l, size)


def first_part(bij, l1, l2, i):
	#variable i useless
	"""get part of the precedent bij to avoid to calculate the same value twice (bij have an overlap between them)"""

	l = np.where(l2 <= l1[-1])[0]
#	print('hoho', l)
	nb = np.where(l2 <= l1[-1])[0].shape[0]
#	print('nb', nb)
	b1 = bij[-nb :, :].copy()
	if nb:
		bol = 1
	else:
		bol = 0
	return (b1, bol)


def get_all_bij(env, a, div, all_l, temp, size):
	"""return an array with all the bij calculate for eache bloc"""

	big_bij = np.zeros((div.shape[0], np.amax(size), temp.shape[2]))
#	print('voila', big_bij.shape)
	bij = np.empty((0, temp.shape[2]))
	l1 = np.zeros(1)
	for i in range(big_bij.shape[0]):
		l = all_l[i, :size[i]]
#		print('l', l.shape)
#		print(l)
#		print(' ')
#		print(l1)
		b1, bol = first_part(bij, l1, l, i)
		l2 = l[np.where(l > l1[-1])[0]]
		b2 = env_fct.get_bij(env, a, l2, temp)
		bij = np.empty((size[i], temp.shape[2]))
	#	print('a', bij.shape)
	#	print('b', b1.shape)
	#	print('c', b2.shape)
		if bol:
			bij[0 : b1.shape[0], :] = b1
			bij[b1.shape[0] :, :] = b2
		else:
			bij = b2
		l1 = l
		big_bij[i, :size[i], :] = bij
	return (big_bij)
