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
from libpy.dot_prod import get_all_bij


set = 5000
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
blc = block.get_block(sp, ti)
blc = block.divide_block(blc)
#print(blc)
div = block.begin_end(blc)
#print(div)
#(al, size) = get_all_bij.get_all_time(ti, div, a)

#l = get_all_bij.small_time(al, 0, size)
#temp = scal_prod.get_temp()
#norme = scal_prod.normalize_temp(temp)
#bij = scal_prod.get_bij(a, l, temp)

#preparation
print("ca commence")

#div = np.array([[0, 499], [500, 999], [1000, 1499], [1500, 1999]])

#fitting
b = a.copy()
scal_prod.browse_bloc(a, blc, ti, div)

#debug
#temp = scal_prod.get_temp()
#temp2 = temp.copy()


#bb2 = get_all_bij.get_all_bij_test(div, al, a, temp, size)
#bb = get_all_bij.get_all_bij(div, al, a, temp, size)
#bij = get_all_bij.small_bij(bb, 0)

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
#for i in range(90, 91):
#	print(i)
#	my_plot.trace(a, b, median, mad, y = set - x, nb = i)
#	plt.show()
#print(bij)
print('fini')
