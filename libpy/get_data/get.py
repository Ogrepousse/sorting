import numpy as np

def get_stream(x = 0, y = 20000):
	"""recupere les signaux des electrodes depuis un fichier externe"""

	with open('../files/ALL.filtered', 'rb') as fd:
		#suppression du header
		ret = -1
		while ret == -1:
			ret = fd.readline().find('EOH')
		fd.read(5)

		#debut des stream
		#on ignore le debut des signaux si x non null
		fd.read(252 * 2 * x)
		size = 4096
		i = 0
		l = (y - x) * 252 * 2
		n = 0
		a = np.empty((y - x) * 252)
		while l - n > size:
			s = fd.read(size)
			a[n / 2 : (n + size) / 2] = np.fromstring(s, dtype = np.uint16)
			i += 1
			n += size
		s = fd.read(l - n)
		a[i * size / 2:] = np.fromstring(s, dtype = np.uint16)

	#	a = np.fromstring(fd.read(252 * 2 * y), dtype = np.uint16)
	#	a = np.reshape(a, (-1, 252))
	#	a = a.T
		a = a.astype(np.int64)
		a = (a - 32767) * 0.01
	return (a)
