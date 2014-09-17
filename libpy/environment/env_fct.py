import numpy as np
import scipy.io
import sys
import matplotlib.pyplot as plt
import snd_comp
import get_all_bij


def get_temp():
	"""get templates from matlab file"""

	all_temp = scipy.io.loadmat('../files/ALL.templates1')
	temp = all_temp['templates'].astype(np.float64)
	t = temp.copy()
	return (t)


def get_amp_lim():
	"""get limit for template from matlab file"""

	amp_lim = scipy.io.loadmat('../files/ALL.templates1')['AmpLim'].astype(np.float64)
	return (amp_lim)


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

	bij = np.empty((l.shape[0], temp.shape[2]))
	s = np.empty((l.shape[0], 252, 129))
	for i in range(bij.shape[0]):
		si = a[:, l[i] - 64 : l[i] + 65]
		s[i, :, :] = si
	bij = np.tensordot(s[::], temp, 2)
	return (bij)


def get_overlap(env):
	"""charge the overlap matrix from an extern file"""

	x = env.nb_temp * 2
	y = x
	z = env.temp_size * 2 - 1
	type_size = 8
	tab = np.empty(x * y * z)
	size = 4096
	i = 0
	l = x * y * z * type_size
	n = 0
	fd = open('omeg4', 'rb')
	while l - n > size:
		s = fd.read(size)
		tab[n / type_size : (n + size) / type_size] = np.fromstring(s, dtype = np.float64)
		i += 1
		n += size
	s = fd.read(l - n)
	tab[i * size / type_size:] = np.fromstring(s, dtype = np.float64)
	fd.close()
	tab = tab.reshape(x, y, z)
	return (tab)
