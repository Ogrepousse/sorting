import env_fct
import snd_comp
import get_all_bij as gab

class t_env(object):
	def __init__(self):
		self.nb_elec = 252 #number of electrodes
		self.space_block = 130 #maximum time between two spike in a same block
		self.size_block = 500 #maximum length for a block
		self.win_over = 129 #size of the overlap window between each block
		self.threshold = 6 #threshold factor for spike discrimination
		print('environnement cree')

	def set_temp(self):
		self.temp = env_fct.get_temp()
		self.temp2 = self.temp.copy()
		self.temp_size = self.temp.shape[1]

	def set_comp(self):
		self.comp = snd_comp.get_comp(self.temp)
		self.comp2 = self.comp.copy()

	def set_norme(self):
		self.norme = env_fct.normalize_temp(self.temp)
		self.norme2 = env_fct.normalize_temp(self.comp)

	def set_lim(self):
		self.amp_lim = env_fct.get_amp_lim()

	def set_overlap(self):
		self.overlap = env_fct.get_overlap()

	def set_time(self, a, ti, div):
		self.al, self.size = gab.get_all_time(self, a, ti, div)

	def set_bij(self, a, div):
		self.big_bij = gab.get_all_bij(a, div, self.al, self.temp, self.size)
		self.big_beta = gab.get_all_bij(a, div, self.al, self.comp, self.size)

	def setup_env(self, a, ti, div):
		self.set_temp()
		self.set_comp()
		self.set_norme()
		self.set_lim()
		self.set_overlap()
		self.set_time(a, ti, div)
		self.set_bij(a, div)
