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
#t_env.adc = 32767
#t_env.el = 0.01
#t_env.nb_elec = 252
#fd = open('sim4.filtered')
del(head)
lol = []

def loop_file(t_env, sample):
	end = 0
	t_env.setup_one()
	total = 0
	sig = 0
	bol = 0
	i = 0
	while end == 0 and total < int(sys.argv[1]):
		t_env.fdout.write("megablock " + str(i) + "\n")
		print('index', t_env.index)
		y = int(sys.argv[1]) - total
		if y > t_env.mega_block:
			y = t_env.mega_block
		else:
			bol = 2
		if type(sig) is int:
			bol = 0
	#	sig, nd = get.get_stream2(t_env, fd, x = 0, y = int(sys.argv[1]))
	#	end = 1
		print('y =', y)
		sig, end = get.get_stream3(t_env, fd, bol, sig, y = y)
		bol = 1
		if sig.shape[0] == 0:
			print('A PLUS')
			break
		a = np.reshape(sig, (-1, t_env.nb_elec)).T.copy()
	#################################################
		lol.append(a.copy())
######################################################
		sample = a.shape[1]
		total += y


		(median, mad, ti, blc, div) = first_part(a)
		print("ca commence")
		b = a.copy()
		core(t_env, a, ti, blc, div)
		if t_env.index == 0:
			t_env.index += y - t_env.win_mega
		else:
			t_env.index += y
		i += 1
		display(a, b, sample, median, mad)
	t_env.fdout.close()
	t_env.del_overlap()
	median = block.cal_median(a)
	mad = block.get_mad(a, median)
#	display(a, b, sample, median, mad)


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

		#delete this line
		blc = np.array([blc[-1]])

		del(sp)
		print('ti', ti)
		print('blc1', blc)
		blc = block.divide_block(t_env, blc)
		print('blc2', blc)
		div = block.begin_end(t_env, blc)
		print('div', div)
		return (median, mad, ti, blc, div)

@profile
def core(t_env, a, ti, blc, div):
	t_env.setup_two(a, ti, div)
	scal_prod.browse_block(t_env, a, blc, ti, div)


def display(a, b, sample, median, mad):
	ra = [105, 110, 123, 139, 143, 155, 158]
#	ra = [105]
#	ra = [17, 23, 55, 59]
#	ra = [93, 122, 143, 144]
	for i in [99]:
		print(i)
		my_plot.trace(a, b, median, mad, y = sample, nb = i)
		plt.show()

def display2(a, b, sample, median, mad):
	ra = [105, 110, 123, 139, 143, 155, 158]
#	ra = [105]
#	ra = [17, 23, 55, 59]
#	ra = [93, 122, 143, 144]
	for i in range(16):
		for j in range(16):
		#	print(i)
			if i * 16 + j >= 252:
				break
			plt.subplot(16, 16, (i) * 16 + j + 1) 
			my_plot.trace(a, b, median, mad, y = sample, nb = i * 16 + j)
	plt.show()

t_env.mega_block = 50000
t_env.size_block = 500
loop_file(t_env, sample)

#mdr = lol
#t_env2 = class_env.t_env()
#sample = int(sys.argv[1])
#x = 0
#t_env2.adc = 32767
#t_env2.el = 0.01
#t_env2.nb_elec = 252
#t_env2.mega_block = 20000
#fd = open('sim2.filtered')
#lol = []
#loop_file(t_env2, sample)

print('fini')
