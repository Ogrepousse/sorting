import numpy as np
import pyopencl as cl
import pyopencl.array
import sys
import scipy.io
from matplotlib import pyplot as plt
from numpy.lib.stride_tricks import as_strided
from fractions import gcd

def get_temp():
	a_t = scipy.io.loadmat('../../files/ALL.templates1')
	temp = a_t['templates'].astype(np.float64)
	t = temp.copy()
	return (t)


#initialisation pyopencl
#platform = cl.get_platforms()
#dev = platform[0].get_devices(device_type = cl.device_type.CPU)
#ctx = cl.Context(devices = dev)
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)
mf = cl.mem_flags

fd = open('kern_tens.cl', 'r')
kern = "".join(fd.readlines())
prog = cl.Program(ctx, kern).build()
fd.close()

temp = get_temp().astype(np.float32)
a = (np.random.randint(0, 100, (252, 500)) / 100. - 0.5).astype(np.float32)
amp = np.random.randint(13, 100, 3) / 100. * 3
time = np.array([150, 250, 350])
for i in range(time.shape[0]):
	a[:, time[i] - 64 : time[i] + 65] += temp[:, :, 0] * amp[i]

x = np.arange(500)
plt.plot(x, a[0, :])
#plt.show()

bij = np.zeros((time.shape[0] * temp.shape[2]), dtype = np.float32)

a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = a.reshape(252 * 500).astype(np.float32))
temp_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = temp.reshape(252*129*382).astype(np.float32))
l_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = time.astype(np.int32))
bij_buff = cl.Buffer(ctx, mf.WRITE_ONLY, bij.nbytes)

def gv1():
	prog.get_bij_v1(queue, (time.shape[0], temp.shape[2]), None, np.int32(252), np.int32(129), np.int32(382), np.int32(500), a_buf, temp_buf, l_buf, bij_buff)
	cl.enqueue_copy(queue, bij, bij_buff)


def get_b():
	"""version actuelle numpy"""
	l = time
	bij = np.empty((l.shape[0], temp.shape[2]))
	s = np.empty((l.shape[0], 252, 129))
	for i in range(bij.shape[0]):
		si = a[:, l[i] - 129 / 2 : l[i] + 129 / 2 + 1]
		s[i, :, :] = si
	bij = np.tensordot(s[::], temp, 2)
	return (bij)

def get_bis(a, l, temp):
	"""version test python (lent)"""
	bij = np.empty((l.shape[0], temp.shape[2]))
	for i in range(l.shape[0]):
		si = a[:, l[i] - 129 / 2 : l[i] + 129 / 2 + 1]
		for j in range(temp.shape[2]):
			bij[i, j] = np.sum(si * temp[:, :, j])
	return (bij)


def get_with_dot():
	"""version produit matricielle avec numpy"""
	b = as_strided(a, (a.shape[1], a.shape[0], a.shape[1]), (a.itemsize, a.shape[1] * a.itemsize, a.itemsize))
	b = b[time - 129 / 2, :, :129]
	b = b.reshape(3, 129*252)
	bij = np.dot(b, temp2.T)
	return (bij)


def	get_with_cl_dot():
	"""version produit matricielle avec opencl"""
	b = as_strided(a, (a.shape[1], a.shape[0], a.shape[1]), (a.itemsize, a.shape[1] * a.itemsize, a.itemsize))
	b = b[time - 129 / 2, :, :129]
	b = b.reshape(3, 129*252)
	b = b.astype(np.float32)

	a_h = b.shape[0]
	a_w = b.shape[1]
	b_h = a_w
	b_w = temp2.shape[1]
	block_size = 1
#	block_size = gcd(a_h, b_w)

	res = np.empty((a_h, b_w), dtype = np.float32)

	kernel_params = {"block_size": block_size, "w_a":a_w, "h_a":a_h, "w_b":b_w}
	print 'lol'
	d_a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = b)
	d_b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = temp2)
	d_c_buf = cl.Buffer(ctx, mf.WRITE_ONLY | mf.COPY_HOST_PTR, hostbuf = res)
	print 'b'
	prog2 = cl.Program(ctx, kern2 % kernel_params).build()
	
	print 'a'
	prog2.matrixMul(queue, res.shape[::-1], (block_size, block_size), d_c_buf, d_a_buf, d_b_buf)
	cl.enqueue_copy(queue, res, d_c_buf).wait()

	return (res)



def lolderire():
	a_h = 7
	a_w = 14
	b_h = a_w
	b_w = 21

	h_a = np.arange(a_h * a_w, dtype = np.float32).reshape(a_h, a_w)
	h_b = np.arange(b_h * b_w, dtype = np.float32).reshape(b_h, b_w)
	h_c = np.empty((a_h, b_w), dtype = np.float32)

	block_size = gcd(a_h, b_w)
#	block_size = 1
	print block_size
	assert a_w % block_size == 0
	assert a_h % block_size == 0
	assert b_w % block_size == 0

#	block_size = 1
	kernel_params = {"block_size": block_size, "w_a": a_w, "h_a":a_h, "w_b": b_w}

	fd = open('dot_matrix.cl', 'r')
	kern2 = "".join(fd.readlines())
	prog2 = cl.Program(ctx, kern2 % kernel_params).build()
	fd.close()

	d_a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = h_a)
	d_b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = h_b)
	d_c_buf = cl.Buffer(ctx, mf.WRITE_ONLY | mf.COPY_HOST_PTR, hostbuf = h_c)

	prog2.matrixMul(queue, h_c.shape[::-1], (block_size, block_size), d_c_buf, d_a_buf, d_b_buf)
	cl.enqueue_copy(queue, h_c, d_c_buf).wait()
	print h_a
	print h_b
	print h_c
	print np.dot(h_a, h_b)
	print np.allclose(np.dot(h_a, h_b), h_c)
	print block_size


def	trans_temp():
	"""transforme le format des templates"""
	temp2 = np.transpose(temp, (2, 0, 1))
	temp2 = temp2.reshape(temp.shape[2], temp.shape[0] * temp.shape[1])
	return (temp2)

temp2 = trans_temp()
temp2 = temp2.astype(np.float32)
fd = open('dot_matrix.cl', 'r')
kern2 = "".join(fd.readlines())
fd.close()

#tempi = np.empty((252 * 129), dtype = np.float32)
#tempi_buf = cl.Buffer(ctx, mf.WRITE_ONLY, tempi.nbytes)
#prog.get_temp_x(queue, (1,), None, np.int32(252), np.int32(129), np.int32(382), temp_buf, tempi_buf)
#cl.enqueue_copy(queue, tempi, tempi_buf)
#tempi = tempi.reshape(252, 129)

#a_bis = np.arange(15*4).reshape(4, 15)
#a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = a_bis.reshape(4 * 15).astype(np.float32))
#api = np.empty(4 * 7, dtype = np.float32)
#api_buf = cl.Buffer(ctx, mf.WRITE_ONLY, api.nbytes)
#prog.get_sig(queue, (1,), None, np.int32(4), np.int32(7), np.int32(382), a_buf, api_buf)
#cl.enqueue_copy(queue, api, api_buf)
#api = api.reshape(4, 7)

#a = np.arange(3*10).reshape(3, 10)
#t = np.arange(3*4*5).reshape(3, 4, 5)
#res = np.empty(1, dtype = np.float32)
#a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = a.reshape(3*10).astype(np.float32))
#t_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = t.reshape(3*4*5).astype(np.float32))


#plt.show()
print('fini')
