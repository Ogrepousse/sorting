import numpy as np
import scipy.io
import sys
import prep_bij

#all_temp = scipy.io.loadmat('../files/ALL.templates')
#temp = all_temp['templates']

def get_temp():
	"""recupere les templates depuis un fichier matlab"""

	all_temp = scipy.io.loadmat('../files/ALL.templates1')
	temp = all_temp['templates'].astype(np.float64)
	return (temp)


def get_amp_lim():
	"""recupere les limites hautes et basses des templates depuis un fichier matlab"""

	amp_lim = scipy.io.loadmat('../files/ALL.templates1')['AmpLim'].astype(np.float64)
#	amp_lim = (amp_lim / 0.01) + 32767
	return (amp_lim)


def select_ti(ti, blc, k, a):
	"""recupere les temps de spike ds le block en excluant les spikes extremes n'ayant pas assez de points autour pour les produits scalaires"""

	l = ti[np.where(ti <= blc[k])[0]]
	if k > 0:
		l = l[np.where(win > blc[k - 1])[0]]
	l = l[np.where((l > 64) & (l + 65 < a.shape[1]))]
	return (l)


def normalize_temp(temp):
	"""normlise les templates et renvoi un tableau contenant la norme de chaque template"""

	norme = np.empty(temp.shape[2])
	for i in range(temp.shape[2]):
		norme[i] = np.linalg.norm(temp[:, :, i])
		temp[:, :, i] = temp[:, :, i] / norme[i]
	return (norme)


def calc_bij(temp, si):
	"""dot poduct for matrix"""

#	res = 0
#	for i in range(temp.shape[0]):
#		for j in range(temp.shape[1]):
#			res += temp[i, j] * si[i, j]
	res = np.sum(temp * si)
	return (res)


def get_bij(a, l, temp):
	"""calcul la matrice bij"""

#	print('obtention des bij')
	bij = np.empty((l.shape[0], temp.shape[2]))
	#print(bij.shape[0])
	for i in range(bij.shape[0]):
	#	print(i)
		si = a[:, l[i] - 64 : l[i] + 65]
		for j in range(bij.shape[1]):
			#bij[i, j] = np.sum(np.dot(temp[:, :, j].T, si))
			bij[i, j] = calc_bij(temp[:, :, j], si)
	#print('max', np.amax(bij))
	return (bij)


def is_explored(exploration):
	""" verifie si tout les i ont ete explores"""

#	print(exploration)
	if np.all(exploration == 3):
		return (0)
	return (1)


def get_max(bij, exploration, bij_bool):
	""" renvoi un tuple des coordonnee de la valeur max de bij en eliminant les couple (i,j) visites et les temps i explores"""

	bij[bij_bool] = -sys.maxint - 1
	bij[exploration >= 3, :] = -sys.maxint - 1
	c = np.unravel_index(bij.argmax(), bij.shape)

#	b = bij[bij_bool]
#	m = b.argmax()
#	ind = np.unravel_index(m, b.shape)
#	c = np.where(bij == b[ind])
#	c = (c[0][0], c[1][0])
#	print('mMAXx', bij[c])
	return (c)


def substract_signal(a, l, aij, temp, c):
	"""soustrait au signal le scaled template"""
#	t = get_temp()
	a[:, l[c[0]] - 64 : l[c[0]] + 65] -= aij * temp[:, :, c[1]]
#	a[:, l[c[0]] - 64 : l[c[0]] + 65] = a[:, l[c[0]] - 64 : l[c[0]] + 65] - t[:, :, c[1]]
#	print(t[90, :, c[1]])
#	print('sub', a[143, l[c[0]]], temp[143, 65, c[1]])


def part_aij(bij, norme, a, amp_lim, exploration, bij_bool, temp, l, omeg):
	"""check max bij puis calcul aij verification contrainte aij"""

#	print('exploitation bij')
	c = get_max(bij, exploration, bij_bool)
	bij_bool[c] = True
	aij = bij[c] / norme[c[1]]
	print(aij)
	limit = amp_lim[:, c[1]]
#	print('aij =', aij)
	if aij > limit[0] and aij < limit[1]:
	#	print('substract en', c[0])
		substract_signal(a, l, aij, temp, c)
		maj_bij(bij, c, aij, omeg)
		return (1)
	else:
	#	print('exploration en', c[0])
		exploration[c[0]] += 1
	#	bij_bool[c[0], :] = True
		return (0)


def maj_bij(bij, c, aij, omeg, l):
	ome = omeg[i, :, :]
	n = (l < c[0] + 129) and (l > c[0] - 128)
	t = l[c[0]] - l[n]
	om = ome[:, 
	bij[:, t - 128 : t + 129] -= aij * om


def browse_bloc(a, blc, ti):
	"""parcour les blocks pour appliquer le fitting"""

	b = 1
	temp = get_temp()
	norme = normalize_temp(temp)
	amp_lim = get_amp_lim()
	omeg = np.loadtxt('omeg').reshape(382, 382, 257)
	for k in range(blc.shape[0]):
		print('entre block')
		l = select_ti(ti, blc, k, a)
		exploration = np.zeros(l.shape[0])
		bij_bool = np.zeros((l.shape[0], temp.shape[2]), dtype = bool)
		bij = get_bij(a, l, temp)
		while is_explored(exploration):
		#	if b:
		#		bij = get_bij(a, l, temp)
			
			b = part_aij(bij, norme, a, amp_lim, exploration, bij_bool, temp, l, omeg)


########################################################################
#reecrite en plus aere
def do_stuff(a, blc, ti):
	bij = np.arange(0)
	temp = get_temp()
	for k in range(blc.shape[0]):
		print('AAA')

####
		l = select_ti(ti, blc, k, a)
####

		#l = ti[np.where(ti <= blc[k])[0]]
		#if k > 0:
		#	l = l[np.where(l > blc[k - 1])[0]]
		bij = np.zeros((l.shape[0], temp.shape[2]))
		for i in range(l.shape[0]):
		#if l[i] > 64 and l[i] + 65 < a.shape[1]:
			si = a[:, l[i] - 64 : l[i] + 65]
			for j in range(temp.shape[2]):
				tmp = temp[:, :, j]
				tmp = tmp / np.linalg.norm(tmp)
				bij[i,j] = np.sum(np.dot(si, tmp.T))
#optimisation necessaire
	return (bij)

#calcul errone
#creer une copie a eviter
def get_si(a, l):
#	win = np.array([np.arange(t - 64, t + 65) for t in l])
	si = a.T[np.array([np.arange(t - 64, t + 65) for t in l])].T
	return (si)

#trop lent
def dot_prod(tmp, si):
	print(tmp.shape, si.shape)
	for i in range(tmp.shape[2]):
		for j in range(si.shape[2]):
			t = np.dot(tmp[:, :, i], si[:, :, j].T)
	print('ola')
