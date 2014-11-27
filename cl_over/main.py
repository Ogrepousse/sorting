import numpy as np
import pyopencl as cl
import pyopencl.array
import sys

plt = cl.get_platforms()
dev = plt[0].get_devices(device_type = cl.device_type.CPU)
ctx = cl.Context(devices = dev)
queue = cl.CommandQueue(ctx)
mf = cl.mem_flags

fd = open('kern.cl', 'r')
kern = "".join(fd.readlines())
prog = cl.Program(ctx, kern).build()

x = 252
y = 129
z = 100

a = np.arange(x * y * z, dtype = np.float32)
A = a.reshape(x, y, z)
res = np.empty(z * z, dtype = np.float32)

a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = a)
r_buf = cl.Buffer(ctx, mf.WRITE_ONLY, res.nbytes)

def f1():
	prog.test(queue, (z, z), None, np.int32(x), np.int32(y), np.int32(z), a_buf, r_buf)
	cl.enqueue_copy(queue, res, r_buf)
	r = res.reshape(z, z)
	return (r)


def omeg(temp, temp2):
#	n = temp.shape[2]
	n = z
	om = np.empty((n, n))
	for j in range(0, n):
		t1 = temp2[:, :, j].copy()
		for i in range(0, n):
			t2 = temp[:, :, i].copy()
			om[j, i] = np.sum(t1 * t2)
	return (om)

r = f1()
print('hello')
#om = omeg(A, A)
