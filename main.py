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
import generateur

set = 2000
x = 0
a = get.get_stream(x = x, y = set)
b = np.ones(a.shape[0], dtype = bool)
a[b] = generateur.gen(set)

print(a)
median = block.cal_median(a)
mad = block.get_mad(a, median)
print(mad[90])
print(median[90])
#block.check_thresh(a, median, mad, 1000)
sp = block.get_spike(a)
ti = block.seperate_time(sp)
blc = block.get_block(sp)

print(ti)
print(blc)

#preparation
print("ca commence")


#fitting
b = a.copy()
scal_prod.browse_bloc(a, blc, ti)

#debug
#temp = scal_prod.get_temp()
#temp2 = temp.copy()
#norme = scal_prod.normalize_temp(temp)
#l = scal_prod.select_ti(ti, blc, 0, a)
#bij = scal_prod.get_bij(a, l, temp)
#omeg = np.loadtxt('omeg4').reshape(3, 3, 257)

#precalcul
#om = prep_bij.omeg(temp, temp2).reshape(temp.shape[2], temp.shape[2] * 257)
#np.savetxt('omeg4', om)
#ome = prep_bij.omeg(temp)

#si = scal_prod.get_si(a, scal_prod.select_ti(ti, blc, 0, a))
#tmp = scal_prod.get_temp()
#scal_prod.dot_prod(tmp, si)

#t = np.ones(set) * -1
#x = np.arange(set)
#t[blc] = 0
#plt.plot(x, sp, x, t)
#plt.show()
my_plot.trace(a, b, median, mad, y = set - x, nb = 1)
plt.show()
#for i in range(382):
#	my_plot.trace(a, b, median, mad, y = set - x, nb = i)
#	plt.show()
#print(bij)
print('fini')
