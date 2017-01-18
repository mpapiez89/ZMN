
from __future__ import division
import numpy as np
import scipy.io as sio;
import matplotlib.pyplot as plt
import itertools
from pylab import *
import copy


########################################
########################################
def Eliminate(tempMat, iMin, k):

    Mat=copy.deepcopy(tempMat);

    for i in range(1,len( tempMat)):
        if i!= iMin:
            div = -(tempMat[i][k]/ tempMat[iMin][k]);
            for j in range(len(tempMat[i])):
                Mat[i][j]= tempMat[i][j]+( tempMat[iMin][j]*div);
        else:
            for j in range(len(tempMat[i])):
                Mat[i][j]=tempMat [ i][j]/tempMat [ iMin][k];
    return Mat;


########################################
########################################
def Iterate(iter, my):

    i = [];

    for f in range(len(iter)-1):
        if iter[f+1][my] == 0:
            v=50000.0 ;
        else:
            v = iter[f+1][len( iter[f+1])-1]/ iter[f + 1] [ my];
        if v>=0:
            i.append(v);
        else:
            i.append(50000.0)
    iter2 = Eliminate(iter, i.index(min(i))+1, my);
    return iter2, i.index(min(i));


########################################
########################################
def ConsoleR(f):

    freeTerm=0
    consoleWR =[];

    if f:
        consoleI = input('Program przyjmuje równania i nierówności w formie znanej z Matlab-a\nex1. \"x1+3*x2+2*x3\" dla funkcji celu,\nex2. \"x1+2*x2+x3<=5\" dla nierówności\n\nPo uzupełnieniu wszystkich równań/nierówności wpisz \"licz\" aby rozwiązać układ\n\nPodaj funkcję celu:\n');
    else:
        consoleI = input("Kolejne równanie/licz: ");

    endW = False;

    if consoleI == "licz":
       endW = True;

    putString = list(consoleI);
    res = "";
    moreThan = False;


    for n in range(len(putString)):
        if n < len(putString) - 1:
            if putString[n] == ".":
                res += putString[n];
            if putString[n].isdigit() or putString[n] == "+" or putString[n] == "-":
                res += putString[n];
            if putString[n] == "x" and putString[n - 1] == "+" and n > 0:
                consoleWR.append(1.0);
                res = "";
            if putString[n] == "x" and putString[n - 1] == "-" and n > 0:
                consoleWR.append(-1.0);
                res = "";
            if putString[n + 1] == "*":
                consoleWR.append(round(float(res), 2));
                res = "";
            if putString[n - 1] == "x" and n > 0:
                res = "";
            if n == 0 and putString[n] == "x":
                consoleWR.append(1.0);
            if putString[n] == ">":
                moreThan = True;
        else:
            if putString[n - 1] != "x" and putString[n].isdigit():
                res += putString[n];
                freeTerm = round(float(res), 2);

    consoleWR.append(freeTerm);

    if moreThan:
        for k in range(len(consoleWR)):
            consoleWR[k] = consoleWR[k] * (-1);
    return consoleWR, endW;

########################################
########################################
def ComputeSimplex(tab):
    while True:
        optimSetChecker = True;
        zj = [];

        for x in range(1, len(tab[0])):
            beta = 0;
            for y in range(1, int(len(tab))):
                beta += cb[y - 1] * tab[y][x];
            zj.append(beta);
        optimSet = [];

        for i in range(len(cj)):
            betaPivot = cj[i] - zj[i];
            optimSet.append(betaPivot);
            if betaPivot > 0 and switchOperator == 1:
                optimSetChecker = False;
            if betaPivot < 0 and switchOperator == 0:
                optimSetChecker = False;
        if optimSetChecker:
            break;
        if switchOperator == 0:
            min1 = optimSet.index(min(optimSet)) + 1;
            tab, z = Iterate(tab, min1);
            cb[z] = cj[min1 - 1];
        else:
            max1 = optimSet.index(max(optimSet)) + 1;
            tab, z = Iterate(tab, max1);
            cb[z] = cj[max1 - 1];

        simplexTab = open('simplexTab.txt', 'a');

        for x in range(len(tab)):
            for y in range(len(tab[x])):
                tab[x][y] = round(tab[x][y], 2);
                simplexTab.write('%.2f' % tab[x][y]);
                simplexTab.write(" \t ");
            simplexTab.write("\n");
        simplexTab.write("\n\n");
        simplexTab.close();


########################################
########################################
def ShowGraph(eqel):
    x = arange(-10, 20, 0.1)
    y = arange(-10, 20, 0.1)
    grid(True)
    xlabel('x')
    ylabel('y')

    def searchEqel(xt, yt, val):
        return val / yt + (-xt / yt * x)

    for i in range(len(eqel) - 1):
        eq1 = searchEqel(eqel[i][1], eqel[i][2], eqel[i][-1])
        eq2 = searchEqel(eqel[i + 1][1], eqel[i + 1][2], eqel[i + 1][-1])
        if np.amax(eq1) > np.amax(eq2):
            temp = eq2
            eq2 = eq1
            eq1 = temp

        xlim(-10, 20)
        ylim(-10, 20)
        hlines(0, -10, 20, color='black')
        vlines(0, -10, 20, color='black')
        plot(x, eq1, color='forestgreen')
        plot(x, eq2, color='red')

    areaF = np.minimum(eq1, eq2)
    fill_between(x, 0, areaF, where=(x > 0) & (eq1 > 0) & (eq2 > 0))
    show()

switchOperator = 1;
v = [];

while True:
    switchOperator = int(input("Wybierz\n0 - minimalizowanie funkcji\n1 - maksymalizowanie\n"));
    if switchOperator == 0 or switchOperator == 1:
        break;
    print("error");
freeTerm = 0;
consoleWR, end = ConsoleR(True);
mnMatrix = len(consoleWR) * 2;
next = [0.0] * (mnMatrix);
next[0] = 1.0;

for n in range(len(consoleWR)):
    if n == len(consoleWR) - 1:
        freeTerm = consoleWR[n];
    else:
        next[n + 1] = consoleWR[n];
next[mnMatrix - 1] = freeTerm;
v += [next];

while True:
    consoleWR2, end = ConsoleR(False);
    if end:
        break;
    ve = [0.0] * (mnMatrix);
    ve[0] = 0.0;
    for n in range(len(consoleWR2)):
        if n == len(consoleWR2) - 1:
            freeTerm = consoleWR2[n];
        else:
            ve[n + 1] = consoleWR2[n];
        ve[mnMatrix - 1] = freeTerm;
    v += [ve];

for n in range(len(v)):
    for k in range(int(mnMatrix / 2), mnMatrix - 1):
        r = n + int(mnMatrix / 2) - 1;
        if r == k:
            v[n][k] = 1.0
        else:
            v[n][k] = 0.0
ShowGraph(v)
print("Wyniki obliczeń zapisane zostaną w pliku simplexTab.txt w formie tabeli znanej z zajęć");


########################################
########################################
simplexTab = open('simplexTab.txt', 'w');

for x in range(2*len(v)):
    if x==0 :
        simplexTab.write('-');
        simplexTab.write("\t ");
    if x > 0 and x<(2*len(v))-1:
        simplexTab.write('x%d' % x);
        simplexTab.write("\t ");
    if x == (2*len(v)-1):
        simplexTab.write('b(i)');
        simplexTab.write("\t ");
simplexTab.write("\n");


for x in range(len(v)):
    for y in range(len(v[x])):
        v[x][y] = round(float(v[x][y]), 2);
        simplexTab.write('%.2f' % v[x][y]);
        simplexTab.write(" \t ");
    simplexTab.write("\n");

simplexTab.write("\n\n");
simplexTab.close();

tab = copy.deepcopy(v);
cj = [];

simplexTab = open('simplexTab.txt', 'a');

for index in range(1, int(len(tab[0])) - 1):
    cj.append(tab[0][index]);
cb = [0.0] * (int(len(cj) / 2));
ComputeSimplex(tab);