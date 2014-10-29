import numpy as np

def read_header(t_env, file_name = '../files/ALL.filtered'):

	fd = open(file_name, 'rb')
	ret = -1
	head = []
	while ret == -1:
		s = fd.readline()
		head.append(s)
		ret = s.find('EOH')
	fd.read(5)
	return (fd, head)


def get_stream3(t_env, fd, bol, sig, y = 20000):
	"""recupere les signaux des electrodes depuis un fichier externe"""

	#debut des stream
	octet = t_env.nb_octet
	size = 4096
	i = 0
	win = t_env.win_mega
	n = 0
	if bol == 0:
		y += win
	l = y * t_env.nb_elec * octet
	a = np.empty(y * t_env.nb_elec)
	b = 0

	while l - n > size:
		s = fd.read(size)
#simplifier le if avec size et len(s)
		if (len(s) == size):
			a[n / octet : (n + size) / octet] = np.fromstring(s, dtype = np.uint16)
		else:
			a[n / octet : (n + len(s)) / octet] = np.fromstring(s, dtype = np.uint16)
			b = 1
		i += len(s)
		n += size
	s = fd.read(l - n)
	if len(s) > 0 and len(s) == l - n:
		a[i / octet:] = np.fromstring(s, dtype = np.uint16)
	elif len(s) > 0:
		b = 1
		a[i / octet : (i + len(s)) / octet] = np.fromstring(s, dtype = np.uint16)
		i += len(s)
	if b:
		a = a[: i / octet]
	a = a.astype(np.int64)
	a = (a - t_env.adc) * t_env.el
	if bol == 1 and b != 1:
		y += 2 * win
		full = np.empty(y * t_env.nb_elec)
		full[: win * 2 * t_env.nb_elec] = sig[sig.shape[0] - (win * 2 * t_env.nb_elec):]
		full[win * 2 * t_env.nb_elec :] = a
	elif bol == 2 or (b == 1 and bol != 0):
		y += win
		full = np.empty(win * 2 * t_env.nb_elec + a.shape[0])
		full[: win * 2 * t_env.nb_elec] = sig[sig.shape[0] - (win * 2 * t_env.nb_elec):]
		full[win * 2 * t_env.nb_elec :] = a
	else:
		full = a
	return (full, b)
