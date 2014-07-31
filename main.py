import numpy as np

with open('../files/test.filtered', 'rb') as fd:
	ret = -1
	while ret == -1:
		print('hello')
		ret = fd.readline().find('EOH')

	#debut des stream
#	a = np.array([], dtype = 'int16')
	a = np.fromstring(fd.read(254 * 2), dtype = np.int16)
	for i in np.arange(10):
		b = np.fromstring(fd.read(254 * 2), dtype = np.int16)
		a = np.vstack((a, b))
	print('lol')
	print(a)
