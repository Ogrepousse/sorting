import numpy as np

def stand_dev(a, med):
#	mean = a.sum(axis = 1) / a.shape[1]
#	med = cal_median(a)
	diff = (a - med[:, np.newaxis])**2
	sq_diff = np.sqrt(diff).astype(np.int64)
	mad = cal_median(sq_diff)
	return (mad)

def cal_median(a):
	median = np.sort(a, axis = 1)[:, a.shape[1] / 2]
	return (median)

def check_thresh(a, median, mad, i):
	b1 = a[:, i] < median - 6 * mad
	if i != a.shape[1] - 1:
		b2 = a[:, i] < a[:, i + 1]
	if i != 0:
		b3 = a[:, i] < a[:, i - 1]
	if i == 0:
		b = b1 & b2
	elif i == a.shape[1] - 1:
		b = b1 & b3
	else:
		b = b1 & b2 & b3
	return (b1)

def make_block(a, x = 0, y = 0):
	median = cal_median(a)
	mad = stand_dev(a, median)
	spike_list = np.zeros(y - x, dtype = np.int64)
	i = x
	while i < y:
		c_t = check_thresh(a, median, mad, i)
		if True in c_t:
			spike_list[i - x] = 1
		i += 1
	print(spike_list)
	if 0 in spike_list:
		print('hola')
	else:
		print('oh non')
	return (spike_list)
