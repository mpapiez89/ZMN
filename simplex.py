from __future__ import division
from numpy import *
import csv

class Simplex:
 
	def __init__(self, f):
		self.f = [1] + f
		self.A = []
		self.b = []
		f=open('wyjscie.txt', 'w')
 
	def dodajWiersz(self, A, b):
		self.A.append([0] + A)
		self.b.append(b)
 
	def obrocKolumne(self):
		l = 0
		idx = 0
		for i in range(1, len(self.f)-1):
			if self.f[i] < l:
				l = self.f[i]
				idx = i
		if idx == 0: return -1
		return idx
 
	def obrocWiersz(self, kolumna):
		rhs = [self.A[i][-1] for i in range(len(self.A))]
		lhs = [self.A[i][kolumna] for i in range(len(self.A))]
		r = []
		for i in range(len(rhs)):
			if lhs[i] == 0:
				r.append(99999999 * abs(max(rhs)))
				continue
			r.append(rhs[i]/lhs[i])
		return argmin(r)
 
	def wyswietl(self, i):
		print '\nIteracja %s: '%(i), '\n', matrix([self.f] + self.A)
		f=open('wyjscie.txt','ab')
		f.write('Iteracja %s:\n'%(i))
		savetxt(f, matrix([self.f] + self.A), delimiter='\t', fmt='%10.5f')
 
	def obroc(self, wiersz, kolumna):
		e = self.A[wiersz][kolumna]
		self.A[wiersz] /= e
		for r in range(len(self.A)):
			if r == wiersz: continue
			self.A[r] = self.A[r] - self.A[r][kolumna]*self.A[wiersz]
		self.f = self.f - self.f[kolumna]*self.A[wiersz]
		 
	def licz(self):
		licznik=1
		for i in range(len(self.A)):
			self.f += [0]
			j = [0 for r in range(len(self.A))]
			j[i] = 1
			self.A[i] += j + [self.b[i]]
			self.A[i] = array(self.A[i], dtype=float)
		self.f = array(self.f + [0], dtype=float)
		self.wyswietl(licznik)
		licznik+=1
		while not min(self.f[1:-1]) >= 0:
			c = self.obrocKolumne()
			r = self.obrocWiersz(c)
			self.obroc(r,c)
			self.wyswietl(licznik)
			licznik+=1
			 
if __name__ == '__main__':
	set_printoptions(precision=3)
	fTemp = []
	aTemp = []
	with open('wejscie.csv', 'r') as csvfile:
		wiersze = csv.DictReader(csvfile, delimiter=',')
		for wiersz in wiersze:
			lenght = len(wiersz)
			if(wiersz['operator']=='==>' and wiersz['wart']=='MIN'):
				for i in range(1,lenght-1):
					fTemp.append(float(wiersz['x'+str(i)]))
				s = Simplex(fTemp)
			elif(wiersz['operator']=='==>' and wiersz['wart']=='MAX'):
				for i in range(1,lenght-1):
					fTemp.append(-1*float(wiersz['x'+str(i)]))
				s = Simplex(fTemp)
			elif(wiersz['operator']=='<='):
				for i in range(1,lenght-1):
					aTemp.append(float(wiersz['x'+str(i)]))
				s.dodajWiersz(aTemp, int(wiersz['wart']))
			elif(wiersz['operator']=='>='):
				for i in range(1,lenght-1):
					aTemp.append(-1*float(wiersz['x'+str(i)]))
				s.dodajWiersz(aTemp, int(wiersz['wart']))
			else:
				f=open('wyjscie.txt','ab')
				f.write('Wystapil blad podczas wczytywania pliku :(')
			aTemp=[]
    
	#alter = Simpex([-1,-3,-2])
	#alter.dodajWiersz([1, 2, 1], 5)
    #alter.dodajWiersz([1, 1, 1], 4)
    #alter.dodajWiersz([0, 1, 2], 1)
    #alter.wynik()
	
	s.licz()
