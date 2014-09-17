import numpy as np
import matplotlib.pyplot as plt
import sys

import libpy
from libpy import get_data
from libpy.get_data import get
from libpy import plot
from libpy.plot import my_plot
from libpy import block_fct
from libpy.block_fct import block
from libpy import dot_prod
from libpy.dot_prod import scal_prod
from libpy import environment
from libpy.environment import class_env

if __name__ != "__main__" or len(sys.argv) != 2:
	print(__name__)
	print(len(sys.argv))
	exit(-1)

env = class_env.t_env()
sample = int(sys.argv[1])
x = 0
sig = get.get_stream(x = x, y = sample)
a = np.reshape(sig, (-1, env.nb_elec)).T

#recherche des temps de spike
sp = block.get_spike(env, a)
ti = block.seperate_time(sp)

#creation des blocs de spike pour le fitting
blc = block.get_block(env, sp, ti)
del(sp)
blc = block.divide_block(env, blc)
print(blc)
div = block.begin_end(env, blc)

print("ca commence")

#fitting
b = a.copy()
env.setup_env(a, ti, div)
scal_prod.browse_block(env, a, blc, ti, div)

#for i in range(90, 91):
#	print(i)
#	my_plot.trace(a, b, y = sample - x, nb = i)
#	plt.show()

print('fini')
