import numpy as np

def get_stream(x = 1, y = 20000):
	with open('../files/test.filtered', 'rb') as fd:
		ret = -1
		while ret == -1:
			ret = fd.readline().find('EOH')
		fd.read(5)

		#debut des stream
		a = np.fromstring(fd.read(252 * 2 * (y - x + 1)), dtype = np.uint16)
		a = np.reshape(a, (-1, 252))
		a = a.T
	return (a)
