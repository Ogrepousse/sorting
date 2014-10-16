import re

import env_fct
import snd_comp
import get_all_bij as gab

class t_env(object):
	def __init__(self):
		self.space_block = 130 #maximum time between two spike in a same block
		self.size_block = 500 #maximum length for a block
		self.win_over = 129 #size of the overlap window between each block
		self.threshold = 6 #threshold factor for spike discrimination
		self.nb_octet = 2 #number of octet for the data
		self.mega_block = 900000 #number of units of time to divide the signal
		self.fdout = open('output', 'w')
		self.index = 0
		print('environnement cree')

	def data_form(self, head):
		"""get information from the header of the data"""
	
		adc = int(re.findall('\d+', head[4])[0])
		el = float(re.findall('\d+.\d+', head[5])[0])
		nb = len(re.findall('\d+', head[6]))

		self.adc = adc #ADC zero
		self.el = el #El
		#El and ADC are used for data conversion
		self.nb_elec = nb #number of electrode

	def set_temp(self):
		"""get the templates and make a copy for normalization"""

		self.temp = env_fct.get_temp()
#temp2 plus vraiment necessaire
		self.temp2 = self.temp.copy()
		self.temp_size = self.temp.shape[1] #template width
		self.nb_temp = self.temp.shape[2] #number of templates

	def set_comp(self):
		"""get the template's second component"""

		self.comp = snd_comp.get_comp(self.temp)
		self.comp2 = self.comp.copy()

	def set_norme(self):
		"""normalize the templates and the second component and stocks the norme"""

		self.norme = env_fct.normalize_temp(self.temp)
		self.norme2 = env_fct.normalize_temp(self.comp)

	def set_lim(self):
		"""get limit for templates"""

		self.amp_lim = env_fct.get_amp_lim()
		for i in range(self.amp_lim.shape[1]):
			self.amp_lim[:, i] *= self.norme[i]
		self.norme = env_fct.normalize_temp(self.temp)	

	def set_overlap(self):
		"""get the overlap matrix"""

		self.overlap_a = env_fct.get_overlap(self, 1, 'omeg6')
	#	self.overlap_b = env_fct.get_overlap(self, 1, 'omeg8')
	#	self.overlap_c = env_fct.get_overlap(self, 1, 'omeg7')
	#	self.overlap_d = env_fct.get_overlap(self, 1, 'omeg9')
#		self.overlap = env_fct.get_overlap(self)

	def del_overlap(self):
		try:
			del(self.overlap_a)
		except AttributeError:
			print('i')
#		del(self.overlap_b)
#		del(self.overlap_c)
#		del(self.overlap_d)

	def set_time(self, a, ti, div):
		"""get all the spike time for all the blocks"""

		self.al, self.size = gab.get_all_time(self, a, ti, div)

	def set_bij(self, a, div):
		"""calculate all bij and beta_ij for each blocks"""

		self.big_bij = gab.get_all_bij(self, a, div, self.al, self.temp, self.size)
		self.big_beta = gab.get_all_bij(self, a, div, self.al, self.comp, self.size)

	def setup_two(self, a, ti, div):
		"""use to load all the data needed for the fitting"""

		self.set_time(a, ti, div)
		self.set_bij(a, div)

	def setup_one(self):
		self.set_temp()
		self.set_comp()
		self.set_norme()
		self.set_lim()
#		self.set_overlap()

	def maj_bij(self, k, b_past):
		if k > 0:
			l = self.al[k, :self.size[k]]
			l1 = self.al[k - 1, :self.size[k - 1]]
#			b_past = self.big_bij[k - 1, :self.size[k - 1], :]
			b1 = gab.first_part(b_past, l1, l, k)
			bij = self.big_bij[k, :self.size[k], :]
			bij[0 : b1.shape[0], :] = b1
			self.big_bij[k, :self.size[k], :] = bij
