import pyopencl as cl
from pyopencl import array as cl_array
import numpy as np
import scipy.io
from matplotlib import pyplot as plt
import math
import sys


def get_temp():
	"""get templates from matlab file"""

	all_temp = scipy.io.loadmat('../../files/ALL.templates1')
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
#	n = temp.shape[2]
	n = 3
	x = np.arange(129)
	om = np.empty((n, n, 129 * 2 - 1))
	for j in range(0, n):
		print(j)
		t1 = temp2[:, :, j].copy()
		for i in range(0, n):
			for k in range(129 * 2 - 1):
				t2 = np.zeros((temp.shape[0], 129))
				boo = temp[:, :, i]
				if k < 129 - 1:
					t2[:, 129 - 1 - k:] = boo[:, :k + 1].copy()
				elif k > 129 - 1:
					t2[:, :257 - k] = boo[:, k - 128:].copy()
				else:
					t2 = temp[:, :, i].copy()
				om[j, i, k] = scal(t1, t2)
	return (om)

#def omeg_gpu(temp, temp2, ctx, queue):
#	for i in range(1, 129 - 1):
#		t1 = cl.array.to_device(queue, temp[:-i])
#		t2 = cl.array.to_device(queue, temp2[i:]


temp = get_temp()
#normalize_temp(temp)
#o = omeg(temp, temp)

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

fd = open("kern.cl", 'r')
kern = "".join(fd.readlines())
#print(kern)
prog = cl.Program(ctx, kern).build()
mf = cl.mem_flags



#t1 = temp[:, :, 0].reshape(252 * 129).astype(np.float32)
#t2 = temp[:, :, 1].reshape(252 * 129).astype(np.float32)

n = int(sys.argv[1])

t1 = np.arange(n, dtype = np.float32)
t2 = np.arange(n, dtype = np.float32)

a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = t1)
b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = t2)
c_buf = cl.Buffer(ctx, mf.READ_WRITE, t1.nbytes)
e_buf = cl.LocalMemory(t1.nbytes)


res = np.empty_like(t1, dtype = np.float32)
res2 = np.empty(1, dtype = np.float32)

d_buf = cl.Buffer(ctx, mf.WRITE_ONLY, res2.nbytes)

def lol():
#	prog.mat_dot_and_sum(queue, t1.shape, None, inte[0], inte[0], a_buf, b_buf, c_buf, d_buf)
	prog.mat_dot(queue, t1.shape, None, a_buf, b_buf, c_buf)
	cl.enqueue_copy(queue, res, c_buf)
	prog.init(queue, res2.shape, None, d_buf)
	prog.mat_sum(queue, t1.shape, None, c_buf, d_buf)

print('b')
prog.mat_reduce(queue, t1.shape, (n,), a_buf, b_buf, e_buf, d_buf)
cl.enqueue_copy(queue, res2, d_buf)
print('a')

print(res2[0])
print(np.sum(t1 * t2))

