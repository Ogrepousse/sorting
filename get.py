import numpy as np

def get_stream(x = 1, y = 20000):
	with open('../files/test.filtered', 'rb') as fd:
		ret = -1
		while ret == -1:
			ret = fd.readline().find('EOH')
		fd.read(5)

		#debut des stream
		a = np.fromstring(fd.read(252 * 2), dtype = np.uint16)[:, np.newaxis]
		print(a)
		b = np.zeros((252, 1))
		while x < y:
			b = np.fromstring(fd.read(252 * 2), dtype = np.uint16)[:, np.newaxis]
			a = np.append(a, b, axis = 1)
			x += 1
	print('mdr')
	return (a)
