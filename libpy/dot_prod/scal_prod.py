import numpy as np
import scipy.io

#all_temp = scipy.io.loadmat('../files/ALL.templates')
#temp = all_temp['templates']

def get_temp():
	"""recupere les templates sur un fichier matlab"""
	all_temp = scipy.io.loadmat('../files/ALL.templates1')
	temp = all_temp['templates'].astype(np.float64)
	return (temp)

def select_ti(ti, blc, k, a):
	"""recupere les temps de spike ds le block en excluant les spike extreme n'ayant pas assez de points autout pour les produit scalaire"""
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

def browse_bloc(a, blc, ti):
	"""parcour les blocks pour appliquer le fitting"""
	temp = get_temp()
	norme = normalize_temp(temp)
	for k in range(blc.shape[0]):
		l = select_ti(ti, blc, k, a)
		bij = get_bij(a, l, temp)

def get_bij(a, l, temp):
	"""calcul la matrice bij"""
	bij = np.empty((l.shape[0], temp.shape[2]))
	for i in range(bij.shape[0]):
		si = a[:, l[i] - 64 : l[i] + 65]
		for j in range(bij.shape[1]):
			bij[i, j] = np.sum(np.dot(si, temp[:, :, j].T))
	return (bij)

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
