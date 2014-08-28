import numpy as np

def get_stream(x = 0, y = 20000):
	with open('../files/ALL.filtered', 'rb') as fd:
		ret = -1
		while ret == -1:
			ret = fd.readline().find('EOH')
		fd.read(5)

		#debut des stream
		fd.read(252 * 2 * x)
		a = np.fromstring(fd.read(252 * 2 * y), dtype = np.uint16)
	#	a = np.reshape(a, (-1, 252))
	#	a = a.T
		a = a.astype(np.int64)
		a = (a - 32767) * 0.01
	return (a)
