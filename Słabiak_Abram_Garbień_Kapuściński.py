#!/usr/bin/python
#ZAłOŻENIA:
#program poprawnie oblicza simplex min i max dla nierówności
#podczas wczytywania funkcji z terminala współczynniki zerowe również należy wpisać(tak jak w przykładzie)
#sprawdzenie poprawności podawanego równania stoi po stronie użytkownika ;)
#program wczytuje wartości z pliku sc50b.mat ale niestety ma problemy z rozwiązaniem zadania
#program wyświetla kolejne tabele simplex w pliku wynik.txt


from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import copy


def Wyswietlanie(tablica):

	x = arange(-5, 15.1, 0.1)
	y = arange(-5, 15.1, 0.1)

	def find_equation(temp_x, temp_y, val):
		return val / temp_y + (-temp_x / temp_y * x)

	for i in range(len(tablica)-1):
		y1=find_equation(tablica[i][1], tablica[i][2], tablica[i][-1])
		y2=find_equation(tablica[i+1][1], tablica[i+1][2], tablica[i+1][-1])

		if np.amax(y1) > np.amax(y2):
			temp = y2
			y2 = y1
			y1 = temp

		xlim(-5, 15)
		ylim(-5, 15)
		hlines(0, -5, 15, color='k')
		vlines(0, -5, 15, color='k')
		grid(True)

		xlabel('x')
		ylabel('y')
		title('Wykres')

		plot(x, y1, color='b')
		plot(x, y2, color='r')

	bottom = np.minimum(y1, y2)
	fill_between(x, 0, bottom, where=(x > 0) & (y1 > 0) & (y2 > 0))
	show()

def GausJordan(tab1, minBeta, Yjeb):
	tab2=copy.deepcopy(tab1);
	print(tab1);
	for x in range(1,len(tab1)):
		if x!=minBeta:
			dzielnik = -(tab1[x][Yjeb]/tab1[minBeta][Yjeb]);
			for y in range(len(tab1[x])):
				tab2[x][y]=tab1[x][y]+(tab1[minBeta][y]*dzielnik);
		else:
			for y in range(len(tab1[x])):
				tab2[x][y]=tab1[x][y]/tab1[minBeta][Yjeb];
	return tab2;
			
def Iteracja(li, Y):
	beta = [];
	for x in range(len(li)-1):
		if li[x+1][Y]==0:
			b=10000.0;
		else:
			b = li[x+1][len(li[x+1])-1]/li[x+1][Y];
		if b>=0:
			beta.append(b);
		else:
			beta.append(10000.0)
	print(beta);
	print(Y);
	li2 = GausJordan(li, beta.index(min(beta))+1, Y);
	return li2, beta.index(min(beta));
	
def CzytanieZKonsoli(funkcjaCelu):
	wyrazWolny=0
	liPomoc=[];
	if funkcjaCelu:
		funkcja = input("Napisz funkcje celu w formie 'x1+0*x2+2*x3': ");
	else:
		funkcja = input("Napisz warunek w formie 'x1+0*x2+x3<=5': ");
	koniecWpisywania=False;
	if	funkcja=="simplex":
		koniecWpisywania=True;
	#funkcja="-21*x1+13*x2+x3-x4<52";
	napis = list(funkcja);
	cyfra="";
	wieksze=False;
	for n in range(len(napis)):
		if n<len(napis)-1:
			if napis[n]==".":
				cyfra+=napis[n];
			if napis[n].isdigit() or napis[n]=="+" or napis[n]=="-":
				cyfra+=napis[n];
			if napis[n]== "x" and napis[n-1]=="+" and n>0:
				liPomoc.append(1.0);
				cyfra = "";
			if napis[n] == "x" and napis[n - 1] == "-" and n>0:
				liPomoc.append(-1.0);
				cyfra = "";
			if napis[n+1]=="*":
				liPomoc.append(round(float(cyfra),2));
				cyfra="";
			if napis[n-1]=="x" and n>0:
				cyfra="";
			if n==0 and napis[n]=="x":
				liPomoc.append(1.0);
			if napis[n]==">":
				wieksze=True;
		else:
			if napis[n-1]!="x" and napis[n].isdigit():
				cyfra += napis[n];
				wyrazWolny = round(float(cyfra),2);
	liPomoc.append(wyrazWolny);
	if wieksze:
		for x in range(len(liPomoc)):
			liPomoc[x]=liPomoc[x]*(-1);
	return liPomoc, koniecWpisywania;
	
def CzytanieZPliku():
	import scipy.io as sio;
	mat_contents = sio.loadmat('sc50b.mat');

	f = mat_contents['f'];
	import itertools
	Fun = list(itertools.chain(*f));
	fFun = [];
	fFun.append(1.0);
	for item in Fun:
		if float(item) == 0:
			fFun.append(0.0);
		else:
			fFun.append(round(float(item), 2));
	for i in range(30):
		fFun.append(0.0);

	A = mat_contents['A'];
	row = [];
	for i in range(30):
		column = [];
		column.append(0.0);
		for j in range(48):
			column.append(round(A[i, j], 2));
		row.append(column);

	for j in range(30):
		for i in range(30):
			if i == j:
				row[i].append(1.0);
			else:
				row[i].append(0.0);
	b = mat_contents['b'];
	for i in range(30):
		row[i].append(b[i]);

	return row;

#################################################

zPlikuCzyZKonsoli=1
while True:
	zPlikuCzyZKonsoli = int(input("Wybierz '0' jeżeli chcesz czytac z pliku lub '1' jeżeli chcesz czytac z konsoli: "));
	if zPlikuCzyZKonsoli == 0 or zPlikuCzyZKonsoli== 1:
		break;
	print("Zły format. Powtórz!!!");

minOrMax=1;
li=[];
if zPlikuCzyZKonsoli==1:
	while True:
		minOrMax = int(input("Wybierz '0' jeżeli chcesz minimalizować funckje lub '1' jeżeli maksymalizować: "));
		if minOrMax == 0 or minOrMax == 1:
			break;
		print("Zły format. Powtórz!!!");
	liMoja=[]
	wyrazWolny=0;
	liPomoc, koniec=CzytanieZKonsoli(True);
	wilekiscTablic=len(liPomoc)*2;
	li0=[0.0]*(wilekiscTablic);
	li0[0]=1.0;
	for n in range(len(liPomoc)):
		if n==len(liPomoc)-1:
			wyrazWolny=liPomoc[n];
		else:
			li0[n+1]=liPomoc[n];
	li0[wilekiscTablic-1]=wyrazWolny;
	li+=[li0];
	print(li0)
	while True:
		print("Jezeli chcesz przerwac wpisywanie warunków napisz 'simplex'")
		liPomoc2, koniec=CzytanieZKonsoli(False);
		if koniec:
			break;
		liKolejne = [0.0] * (wilekiscTablic);
		liKolejne[0] = 0.0;
		for n in range(len(liPomoc2)):
			if n == len(liPomoc2) - 1:
				wyrazWolny = liPomoc2[n];
			else:
				liKolejne[n + 1] = liPomoc2[n];
			liKolejne[wilekiscTablic - 1] = wyrazWolny;
		li += [liKolejne];

	for n in range(len(li)):
		for k in range(int(wilekiscTablic / 2), wilekiscTablic - 1):
			r=n+int(wilekiscTablic / 2)-1;
			if r==k:
				li[n][k] = 1.0
			else:
				li[n][k] = 0.0
	Wyswietlanie(li)


if zPlikuCzyZKonsoli==0:
	li=CzytanieZPliku()

F = open('wynik.txt', 'w');
for x in range(len(li)):
	for y in range(len(li[x])):
		li[x][y] = round(float(li[x][y]), 2);
		F.write('%.2f' % li[x][y]);
		F.write(" \t ");
	F.write("\n");
F.write("\n");
F.close();
#li = [[1.0, 1.0, 3.0, 2.0, 0.0, 0.0, 0.0, 0.0],[0.0, 1.0, 2.0, 1.0, 1.0, 0.0, 0.0, 5.0],[0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 4.0],[0.0, 0.0, 1.0, 2.0, 0.0, 0.0, 1.0, 1.0]];
#li=[[1.0, 1.0, 1.0, 0.0, 0.0, 0.0], [0.0, 2.0, 1.0, 1.0, 0.0, 4.0], [0.0, 1.0, 2.0, 0.0, 1.0, 3.0]];
tab=copy.deepcopy(li);
cj = [];
for index in range(1, int(len(tab[0]))-1):
	cj.append(tab[0][index]);
cb=[0.0]*(int(len(cj)/2));


while True:
	czyOptymalny = True;
	zj = [];

	for x in range(1, len(tab[0])):
		zjPomoc = 0;
		for y in range(1, int(len(tab))):
			zjPomoc += cb[y - 1] * tab[y][x];
		zj.append(zjPomoc);
	wskaznikOptymalnosci = [];
	for i in range(len(cj)):
		wsk = cj[i] - zj[i];
		wskaznikOptymalnosci.append(wsk);
		if wsk > 0 and minOrMax == 1:
			czyOptymalny = False;
		if wsk < 0 and minOrMax == 0:
			czyOptymalny = False;

	if czyOptymalny:
		print(tab);
		print("Jest optymalny!")
		break;

	if minOrMax == 0:
		bMin = wskaznikOptymalnosci.index(min(wskaznikOptymalnosci)) + 1;
		tab, indexMinBeta = Iteracja(tab, bMin);
		cb[indexMinBeta] = cj[bMin - 1];
	else:
		bMax = wskaznikOptymalnosci.index(max(wskaznikOptymalnosci)) + 1;
		tab, indexMinBeta = Iteracja(tab, bMax);
		cb[indexMinBeta] = cj[bMax - 1];

	F = open('wynik.txt', 'a');
	for x in range(len(tab)):
		for y in range(len(tab[x])):
			tab[x][y]=round(tab[x][y], 2);
			F.write('%.2f' % tab[x][y]);
			F.write(" \t ");
		F.write("\n");
	F.write("\n");
	F.close();
	print("\n")
