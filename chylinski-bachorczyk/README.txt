Aplikacja zosta�a napisana w �rodowisku QT, w razie gdyby nie posiada�a Pani tego IDE dodali�my
plik wykonywalny exe wraz z dolaczonym zestawem bibliotek ktore umozliwiaja jej uruchomienie.

Niestety nie zdazylismy napisac modulu ktory umozliwialby wczytanie danych z pliku.


INPUT:
Funkcj� celu nale�y poda� w postaci tekstu z nast�puj�cymi ograniczeniami:
- zmienne musz� si� zaczyna� od 1 oraz musz� by� one kolejnymi warto�ciami (dla 3 zmiennych: 1,2,3)
- indeks zmiennej podajemy w nawiasach okr�g�ych
- nie mo�na poda� dwukrotnie tego samego indeksu
- funkcja nie mo�e zawiera� operacji matematycznych (np. mno�enia czy dzielenia)
- wsp�czynnik przed zmienn� mo�e by� warto�ci� zmiennoprzecinkow� lub ca�kowit�
- wielko�� liter nie ma znaczenia
- separator dziesi�tny mo�e by� przecinkiem lub kropk�
- znaki bia�e s� pomijane
- zmienn� wraz z wsp�czynnikiem zapisujemy w postaci: "wsp�czynnik x(indeks)" np. 10.4x(2)

ogarniczenia nier�wno�ci:
- lewa strona nier�wno�ci posiada takie same ograniczenia jak funkcja celu 
z tym, �e musi posiada� conajmniej jedn� zmienn� a nie wszystkie.
- prawa strona nier�wno�ci powinna by� liczb� zmiennoprzecinkow� lub ca�kowit�.
-Ka�d� nier�wno�� podajemy w nowej lini

Do p�l tekstowych wprowadzilismy przykladowe dane tak aby mozna bylo "na szybko" 
przetestowac dzialanie aplikacji oraz dawaly poglad na to w jakim formacie powinny 
byc wprowadzane dane.

Program zosta� przetestowany dla nast�puj�cych zestaw�w danych.

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
