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
	sys.exit(-1)

t_env = class_env.t_env()
sample = int(sys.argv[1])
x = 0
fd, head = get.read_header(t_env)
t_env.data_form(head)
del(head)

def loop_file(t_env, sample):
	end = 0
	t_env.setup_one()
	total = 0
	sig = 0
	bol = 0
	while end == 0 and total < int(sys.argv[1]):
		y = int(sys.argv[1]) - total
		if y > t_env.mega_block:
			y = t_env.mega_block
		else:
			bol = 2
		if type(sig) is int:
			bol = 0
#		sig = get.get_stream(t_env, x = 0, y = int(sys.argv[1]))
#		end = 1
		print('y =', y)
		sig, end = get.get_stream3(t_env, fd, bol, sig, y = y)
		bol = 1
		if sig.shape[0] == 0:
			print('A PLUS')
			break
		a = np.reshape(sig, (-1, t_env.nb_elec)).T.copy()
		sample = a.shape[1]
		total += y

		(median, mad, ti, blc, div) = first_part(a)
		print("ca commence")
		b = a.copy()
	#	core(t_env, a, ti, blc, div)

		display(a, b, sample, x, median, mad)
	del(t_env.overlap)


def first_part(a):
		#### for plotting #####
		median = block.cal_median(a)
		mad = block.get_mad(a, median)
		#######################

		#recherche des temps de spike
		sp = block.get_spike(t_env, a)
		ti = block.seperate_time(sp)

		#creation des blocs de spike pour le fitting
		blc = block.get_block(t_env, sp, ti)
		del(sp)
		blc = block.divide_block(t_env, blc)
	#	print(blc)
		div = block.begin_end(t_env, blc)
		return (median, mad, ti, blc, div)


def core(t_env, a, ti, blc, div):
	t_env.setup_two(a, ti, div)
	scal_prod.browse_block(t_env, a, blc, ti, div)

#core()
def display(a, b, sample, x, median, mad):
#	print('shape', a.shape)
	for i in range(99, 100):
#		print(i)
		my_plot.trace(a, b, median, mad, y = sample - x, nb = i)
		plt.show()

loop_file(t_env, sample)

print('fini')
