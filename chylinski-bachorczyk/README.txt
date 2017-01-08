Aplikacja zosta³a napisana w œrodowisku QT, w razie gdyby nie posiada³a Pani tego IDE dodaliœmy
plik wykonywalny exe wraz z dolaczonym zestawem bibliotek ktore umozliwiaja jej uruchomienie.

Niestety nie zdazylismy napisac modulu ktory umozliwialby wczytanie danych z pliku.


INPUT:
Funkcjê celu nale¿y podaæ w postaci tekstu z nastêpuj¹cymi ograniczeniami:
- zmienne musz¹ siê zaczynaæ od 1 oraz musz¹ byæ one kolejnymi wartoœciami (dla 3 zmiennych: 1,2,3)
- indeks zmiennej podajemy w nawiasach okr¹g³ych
- nie mo¿na podaæ dwukrotnie tego samego indeksu
- funkcja nie mo¿e zawieraæ operacji matematycznych (np. mno¿enia czy dzielenia)
- wspó³czynnik przed zmienn¹ mo¿e byæ wartoœci¹ zmiennoprzecinkow¹ lub ca³kowit¹
- wielkoœæ liter nie ma znaczenia
- separator dziesiêtny mo¿e byæ przecinkiem lub kropk¹
- znaki bia³e s¹ pomijane
- zmienn¹ wraz z wspó³czynnikiem zapisujemy w postaci: "wspó³czynnik x(indeks)" np. 10.4x(2)

ogarniczenia nierównoœci:
- lewa strona nierównoœci posiada takie same ograniczenia jak funkcja celu 
z tym, ¿e musi posiadaæ conajmniej jedn¹ zmienn¹ a nie wszystkie.
- prawa strona nierównoœci powinna byæ liczb¹ zmiennoprzecinkow¹ lub ca³kowit¹.
-Ka¿d¹ nierównoœæ podajemy w nowej lini

Do pól tekstowych wprowadzilismy przykladowe dane tak aby mozna bylo "na szybko" 
przetestowac dzialanie aplikacji oraz dawaly poglad na to w jakim formacie powinny 
byc wprowadzane dane.

Program zosta³ przetestowany dla nastêpuj¹cych zestawów danych.

60x(1) + 30x(2) + 20x(3)

8x(1) + 6x(2) + 1x(3) <= 960
8x(1) + 4x(2) + 3x(3) <= 800
4x(1) + 3x(2) + 1x(3) <= 320


/////////////////////
1000x(1) + 2000x(2)

2x(1) + 2x(2) <= 8
1x(2) <= 3


/////////////////////
1x(1) + 3x(2) + 2x(3)

1x(1) + 2x(2) + 1x(3) <= 5
1x(1) + 1x(2) + 1x(3) <= 4
1x(2) + 2x(3) <= 1


///////////////////// 
-5x(1) - 4x(2) - 6x(3)

1x(1) - 1x(2) + 1x(3) <= 20
3x(1) + 2x(2) + 4x(3) <= 42
3x(1) + 2x(2) <= 30
