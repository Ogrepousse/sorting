import numpy as np
import pyopencl as cl
import pyopencl.array
import sys
import scipy.io
from matplotlib import pyplot as plt

def get_temp():
	a_t = scipy.io.loadmat('../../files/ALL.templates1')
	temp = a_t['templates'].astype(np.float64)
	t = temp.copy()
	return (t)


#initialisation pyopencl
platform = cl.get_platforms()
dev = platform[0].get_devices(device_type = cl.device_type.CPU)
ctx = cl.Context(devices = dev)
queue = cl.CommandQueue(ctx)
mf = cl.mem_flags

fd = open('kern_tens.cl', 'r')
kern = "".join(fd.readlines())
prog = cl.Program(ctx, kern).build()

temp = get_temp()
a = np.random.randint(0, 100, (252, 500)) / 100. - 0.5
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
	prog.get_bij_v1(queue, (time.shape[0], temp.shape[2]), None, np.int32(252), np.int32(129), np.int32(382), a_buf, temp_buf, l_buf, bij_buff)
	cl.enqueue_copy(queue, bij, bij_buff)


def get_b(a, l, temp):
	bij = np.empty((l.shape[0], temp.shape[2]))
	s = np.empty((l.shape[0], 252, 129))
	for i in range(bij.shape[0]):
		si = a[:, l[i] - 129 / 2 : l[i] + 129 / 2 + 1]
		s[i, :, :] = si
	bij = np.tensordot(s[::], temp, 2)
	return (bij)


#tempi = np.empty((252 * 129), dtype = np.float32)
##tempi_buf = cl.Buffer(ctx, mf.WRITE_ONLY, tempi.nbytes)
#prog.get_temp_x(queue, (1,), None, np.int32(252), np.int32(129), np.int32(382), temp_buf, tempi_buf)
#cl.enqueue_copy(queue, tempi, tempi_buf)
#tempi = tempi.reshape(252, 129)

a_bis = np.arange(10*3).reshape(3, 10)
a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = a_bis.reshape(30).astype(np.float32))
api = np.empty(3 * 7, dtype = np.float32)
api_buf = cl.Buffer(ctx, mf.WRITE_ONLY, api.nbytes)
prog.get_sig(queue, (1,), None, np.int32(3), np.int32(7), np.int32(382), a_buf, api_buf)
cl.enqueue_copy(queue, api, api_buf)
api = api.reshape(3, 7)


#plt.show()
print('fini')
