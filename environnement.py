class t_env(object):
	def __init__(self):
		self.space_block = 130 #maximum time between two spike in a same block
		self.size_block = 500 #maximum length for a block
		self.win_over = 129 #size of the overlap window between each block
		print('environnement cree')	
