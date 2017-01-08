
def wypiszTablice(tab):
    print("-----------------")
    for row in tab:
        print(row)
    print("-----------------")

def pivotOn(tab, row, col):
 j = 0
 pivot = tab[row][col]
 for x in tab[row]:
  tab[row][j] = tab[row][j] / pivot
  j += 1
 i = 0
 for xi in tab:
  if i != row:
   ratio = xi[col]
   j = 0
   for xij in xi:
    xij -= ratio * tab[row][j]
    tab[i][j] = xij
    j += 1
  i += 1
 return tab

def simplex(tab):
 plik = open('result.txt', 'w') 
 THETA_INFINITE = -1
 opt   = False
 unbounded  = False
 n = len(tab[0])
 m = len(tab) - 1
 
 while ((not opt) and (not unbounded)):
  wypiszTablice(tab)
  for row in tab: 
        plik.write(str(row))
        plik.write("\n") 
  plik.write("\n") 
  min = 0.0
  pivotCol = j = 0
  while(j < (n-m)):
   cj = tab[0][j]
   
   if (cj < min) and (j > 0):
    min = cj
    pivotCol = j
   j += 1   
  if min == 0.0:
   
   opt = True
   continue
  pivotRow = i = 0
  minTheta = THETA_INFINITE
  for xi in tab:
   
   if (i > 0):
    xij = xi[pivotCol]
    if xij > 0:
     theta = (xi[0] / xij)
     if (theta < minTheta) or (minTheta == THETA_INFINITE):
      minTheta = theta
      pivotRow = i
   i += 1
  if minTheta == THETA_INFINITE:
   
   unbounded = True
   continue
  
  tab = pivotOn(tab, pivotRow, pivotCol)
 #wypiszTablice(tab)
 plik.write("Tabela koncowa\n")
 plik.write("Globalny koszt optymalizacji:  ")
 plik.write(str(tab[0][0]))
 plik.close()
 return tab

 


