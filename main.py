import numpy as np
import matplotlib.pyplot as plt

with open('../files/test.filtered', 'rb') as fd:
	ret = -1
	while ret == -1:
		ret = fd.readline().find('EOH')

	#debut des stream
	a = np.fromstring(fd.read(252 * 2), dtype = np.int16)[:, np.newaxis]
	print(a.shape)
	b = np.zeros((252, 1))
	print('B', b.shape)
	x = 1
#	for i in np.arange(120):
	while b.shape[0] == 252:
	#	print('bbb', b.shape)
		b = np.fromstring(fd.read(252 * 2), dtype = np.int16)[:, np.newaxis]
		a = np.append(a, b, axis = 1)
		x += 1

b = a[0]
print('x =', x)
c = np.arange(x);
print(b)
print(c)
plt.plot(c, b)
plt.show()
print('lol')
