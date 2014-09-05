import numpy as np

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
	all_l = np.zeros((blc.shape[0], ti.shape[0]))
	for i in range(all_l.shape[0]):
		l = select_ti_bis(ti, blc, i, a)
		all_l[i, :l.shape[0]] = l
	return (all_l)


def calc_bij(temp, si):
	return (np.sum(temp * si))


def get_all_bij(blc, all_l, a, temp):
	big_bij = np.zeros((all_l.shape[0], ti.shape[0], temp.shape[2]))
	for i in range(big_bij.shape[0]):
		
