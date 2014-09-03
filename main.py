import numpy as np
import matplotlib.pyplot as plt

import libpy
from libpy import get_data
from libpy.get_data import get
from libpy import plot
from libpy.plot import my_plot
from libpy import fitting
from libpy.fitting import block
from libpy import dot_prod
from libpy.dot_prod import scal_prod
from libpy.dot_prod import prep_bij
from libpy.dot_prod import snd_comp


set = 2000
x = 0
sig = get.get_stream(x = x, y = set)
a = np.reshape(sig, (-1, 252)).T
#print(a)
median = block.cal_median(a)
mad = block.get_mad(a, median)
#print(mad[90])
#print(median[90])
#block.check_thresh(a, median, mad, 1000)
print('ouai')
sp = block.get_spike(a)
ti = block.seperate_time(sp)
#print(ti)
blc = block.get_block(sp)
print('nb blc', blc.shape)

#preparation
print("ca commence")


#fitting
b = a.copy()
scal_prod.browse_bloc(a, blc, ti)

#debug
#temp = scal_prod.get_temp()
#temp2 = temp.copy()
#comp = snd_comp.get_comp(temp)
#comp2 = comp.copy()
#norme = scal_prod.normalize_temp(temp)
#scal_prod.normalize_temp(comp)
#print(temp.shape)
#np.savetxt('temp', temp.reshape(252, 129 * 382))
#np.savetxt('temp2', temp2.reshape(252, 129 * 382))
#np.savetxt('comp', comp.reshape(252, 129 * 382))
#np.savetxt('comp2', comp2.reshape(252, 129 * 382))

#cx = np.arange(temp.shape[1])
#plt.plot(cx, temp[9, :, 54])
#plt.show()
#for i in range(temp.shape[2]):
#	if np.any(comp[0, :, i]):
#		print(i)
#		plt.plot(x, comp[0, :, i], x, temp[0, :, i])
#		plt.show();

#l = scal_prod.select_ti(ti, blc, 0, a)
#bij = scal_prod.get_bij(a, l, temp)
#omeg = np.loadtxt('omeg').reshape(382, 382, 257)

#precalcul
#om = prep_bij.omeg_bis(temp, temp2, comp, comp2)
#ome = om.reshape(382*2, 382*2 * 257)
#np.savetxt('omeg3', ome)


#si = scal_prod.get_si(a, scal_prod.select_ti(ti, blc, 0, a))
#tmp = scal_prod.get_temp()
#scal_prod.dot_prod(tmp, si)

#t = np.ones(set) * -1
#x = np.arange(set)
#t[blc] = 0
#plt.plot(x, sp, x, t)
#plt.show()
#my_plot.trace(a, b, median, mad, y = set - x, nb = 90)
#cx = np.arange(a.shape[1])
#plt.plot(cx, a[90], cx, b[90])
#plt.show()
for i in range(90, 91):
	print(i)
	my_plot.trace(a, b, median, mad, y = set - x, nb = i)
	plt.show()
#print(bij)
print('fini')
