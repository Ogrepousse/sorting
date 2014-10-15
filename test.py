import numpy as np
import scipy.io
from matplotlib import pyplot as plt
import math
import sys

def get_overlap():
	"""charge the overlap matrix from an extern file"""

	x = 382 * 2
	y = x
	z = 129 * 2 - 1
	type_size = 8
	tab = np.empty(x * y * z)
	size = 4096
	i = 0
	l = x * y * z * type_size
	n = 0
	fd = open('omeg5', 'rb')
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

def lol():
	o = scipy.io.loadmat('../files/ALL_norm.overlap1')
	over = o['c_overlap'].astype(np.float64)
	v = over.copy()
	return (v)

def mdr():
	temp = get_overlap()
	t1 = temp[:382, :382, :]
	del(temp)
	t2 = lol()
	return (t1, t2)

def get_temp():
	"""get templates from matlab file"""

	all_temp = scipy.io.loadmat('../files/ALL.templates1')
	temp = all_temp['templates'].astype(np.float64)
	t = temp.copy()
	return (t)


def normalize_temp(temp):
	"""normalize the templates and return an array with the value of all the norme"""

	norme = np.empty(temp.shape[2])
	for i in range(temp.shape[2]):
		norme[i] = np.linalg.norm(temp[:, :, i])
		temp[:, :, i] = temp[:, :, i] / norme[i]
	return (norme)


def scal(t1, t2):
	c = t1 * t2
	res = np.sum(c)
	return (res)


def omeg(temp, temp2):
	n = temp.shape[2]
	x = np.arange(129)
	om = np.empty((n, n, 129 * 2 - 1))
	for j in range(0, n):
		print(j)
		t1 = temp2[:, :, j].copy()
		for i in range(0, n):
	#		print(i)
			for k in range(129 * 2 - 1):
				t2 = np.zeros((temp.shape[0], 129))
				boo = temp[:, :, i]
				if k < 129 - 1:
#					t2[:, 129 - 1 - k:] = temp[:, :k + 1, i].copy()
					t2[:, 129 - 1 - k:] = boo[:, :k + 1].copy()
				elif k > 129 - 1:
#					t2[:, :257 - k] = temp[:, k - 128:, i].copy()
					t2[:, :257 - k] = boo[:, k - 128:].copy()
				else:
					t2 = temp[:, :, i].copy()
		#		if i == 0:
		#			plt.plot(x, t2[0, :])
		#			plt.show()
				om[j, i, k] = scal(t1, t2)
	return (om)

def new_omeg(temp, temp2):
	n = temp.shape[2]
	om = np.empty((n, n, 129 * 2 - 1))
	for k in range(129 * 2 - 1):
		print(k)
		decal = np.zeros(temp.shape)
		if k < 129 - 1:
			decal[:, 129 - 1 - k:, :] += temp[:, :k + 1, :]
		elif k > 129 - 1:
			decal[:, :257 - k, :] += temp[:, k - 128:, :]
		else:
			c = temp
		for j in range(n):
			tem = temp2[:, :, j].copy()
			om[j, :, k] = np.tensordot(decal, tem, ((1, 0), (1, 0)))
	return (om)



def test(o, over, i, j):
	a = o[i, j, :]
	b = over[i, j, :]
	print(np.abs(a - b) < 0.00001)


def test2(o, over, i, j):
	print(o[i, j, :])
	print(over[i, j, :])

def test3(o, over):
	c = 0
	for i in range(o.shape[0]):
		print(i)
		for j in range(o.shape[0]):
			a = o[i, j, :]
			a = a[::-1]
			b = over[i, j, :]
			bol = np.abs(a - b) < 0.001
			if np.any(bol == False):
				print('erreur', i, j)
				c = 1
		if c:
			sys.stdin.read(1)
		c = 0

def st(temp, i):
	x = np.arange(129)
	for j in range(252):
		plt.plot(x, temp[j, :, i])
	plt.show()

def maxi(o, over, i, j):
	a = o[i, j, :]
	b = over[i, j, :]
	print(np.max(a))
	print(np.max(b))

def trace(o, over, i = 0, j = 382):
	for k in range(i, j):
		a = o[k, :, :][:, ::-1].reshape(o.shape[2] * o.shape[1])
		b = over[k, :, :].reshape(o.shape[2] * o.shape[1])
		plt.plot(a, b)
	plt.show()


def coef(o, over):
	c = np.ones(382) * -10
	for k in range(382):
		a = o[k, :, :][:, ::-1]
		b = over[k, :, :]
		val = np.where(b != 0)
		if val[0].shape[0] != 0:
			c[k] = (a / b)[val[0][0], val[0][0]]
	return (c)

temp = get_temp()
temp2 = temp.copy()
norme = normalize_temp(temp)
om = omeg(temp, temp)
ome = om.reshape(382 * 382 * 257)
fd =  open('omeg6', 'wb')
fd.write(ome)
#temp3 = temp[:, :, :]
#om = new_omeg(temp3, temp3)
#over = omeg(temp, temp2)

#if len(sys.argv) == 1:
#	over, o2 = mdr()
#
	#o2 = lol()
#	o2 = o2 / math.sqrt(252 * 129)
	#o = o2[252:254, 252:254, :]
#	o = o2

#test3(o2, over)
