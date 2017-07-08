#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint

ZNACZNIK_PUSTY = "0"
ZNACZNIK_PUDLO = "x"
ZNACZNIK_TRAFIONY = "T"
ZNACZNIK_ZATOPIONY = "Z"
ZNACZNIK_STATEK = "&"
ZNACZNIK_OBWIEDNIA = "."
KIERUNKI = ["prawo", "lewo", "gora", "dol"]

class Plansza(object):
    """Abstrakcyjna reprezentacja planszy"""

    def __init__(self, rzedy, kolumny, zapelnienie = 20):
        super(Plansza, self).__init__()
        self.rzedy = rzedy
        self.kolumny = kolumny
        self.rozmiar = rzedy * kolumny
        self.zapelnienie = zapelnienie # stosunek sumarycznego rozmiaru umieszczonych statków do rozmiaru planszy
        self.pola = [ZNACZNIK_PUSTY * kolumny for rzad in xrange(rzedy)] #lista stringów odpowiadających rzędom pól planszy
        self.statki = []

    def rysujSie(self):
        """Rysuje planszę"""

        # numeracja kolumn
        print
        print "    " + "  ".join([str(liczba) for liczba in xrange(1, self.kolumny + 1) if liczba < 10]) + " " + " ".join([str(liczba) for liczba in xrange(1, self.kolumny + 1) if liczba >= 10])
        print
        for i in xrange(len(self.pola)):
            # numeracja rzędów
            if i + 1 < 10:
                print str(i + 1) + "  ",
            else:
                print str(i + 1) + " ",
            # właściwe pola planszy
            print "  ".join(self.pola[i])

    def oznaczPole(self, znacznik, rzad, kolumna):
        """Oznacza wskazane polę wskazanym znacznikiem"""
        rzad_lista = list(self.pola[rzad - 1])
        rzad_lista[kolumna - 1] = znacznik    
        nowy_rzad = "".join(rzad_lista)
        self.pola[rzad - 1] = nowy_rzad

    def czyPoleWolne(self, rzad, kolumna):
        """Sprawdza czy wskazane pole jest niezajęte"""
        if self.pola[rzad - 1][kolumna - 1] == ZNACZNIK_PUSTY:
            return True
        else:
            return False

    def czyPoleWPlanszy(self, rzad, kolumna):
        """Sprawdza czy wskazane pole jest w obrębie planszy"""
        if rzad < 1 or rzad > self.rzedy or kolumna < 1 or kolumna > self.kolumny:
            return False
        else:
            return True 

    def umiescStatek(self, rozmiar, rzad, kolumna):
        """Umieszcza statek o podanym rozmiarze na planszy. Statek rozrasta się w przypadkowych kierunkach ze wskazanego pola początkowego"""
        licznik_oznaczen = 0
        licznik_iteracji = 0
        sciezka = []
        wspolrzedne_pol = []

        while licznik_oznaczen < rozmiar and licznik_iteracji < 50:
            
            print # do testów
            komunikat = "ITERACJA " + str(licznik_iteracji + 1)
            print komunikat.center(3 * self.kolumny)
            

            if licznik_iteracji == 0:
                self.oznaczPole(ZNACZNIK_STATEK, rzad, kolumna)
                licznik_oznaczen += 1
                wspolrzedne_pol.append((rzad, kolumna))
            else:
                oznaczono = False
                licznik_zapetlenia = 0

                while not oznaczono:
                    licznik_zapetlenia += 1

                    # obsługa zapętlenia
                    if licznik_zapetlenia > 50:
                        ostatni_kierunek = sciezka[len(sciezka) - 1]
                        if ostatni_kierunek == "prawo":
                            kolumna -= 1
                            print "Cofam: '" + sciezka.pop() + "'"
                        elif ostatni_kierunek == "lewo":
                            kolumna += 1
                            print "Cofam: '" + sciezka.pop() + "'"
                        elif ostatni_kierunek == "gora":
                            rzad += 1
                            print "Cofam: '" + sciezka.pop() + "'"
                        elif ostatni_kierunek == "dol":
                            rzad -= 1
                            print "Cofam: '" + sciezka.pop() + "'"
                        print "Uciekam z zapetlenia"

                        break

                    kierunek = KIERUNKI[randint(0, 3)]
                    if kierunek == "prawo":
                        kolumna += 1
                        if self.czyPoleWPlanszy(rzad, kolumna) and self.czyPoleWolne(rzad, kolumna):
                            self.oznaczPole(ZNACZNIK_STATEK, rzad, kolumna)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            wspolrzedne_pol.append((rzad, kolumna))
                            #test
                            # print kierunek.center(3 * self.kolumny), str(rzad), str(kolumna)
                        else:
                            kolumna -= 1
                    elif kierunek == "lewo":
                        kolumna -= 1
                        if self.czyPoleWPlanszy(rzad, kolumna) and self.czyPoleWolne(rzad, kolumna):
                            self.oznaczPole(ZNACZNIK_STATEK, rzad, kolumna)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            wspolrzedne_pol.append((rzad, kolumna))
                            #test
                            # print kierunek.center(3 * self.kolumny), str(rzad), str(kolumna)
                        else:
                            kolumna += 1
                    elif kierunek == "gora":
                        rzad -= 1
                        if self.czyPoleWPlanszy(rzad, kolumna) and self.czyPoleWolne(rzad, kolumna):
                            self.oznaczPole(ZNACZNIK_STATEK, rzad, kolumna)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            wspolrzedne_pol.append((rzad, kolumna))
                            #test
                            # print kierunek.center(3 * self.kolumny), str(rzad), str(kolumna)
                        else:
                            rzad += 1
                    else: # idziemy w dół
                        rzad += 1
                        if self.czyPoleWPlanszy(rzad, kolumna) and self.czyPoleWolne(rzad, kolumna):
                            self.oznaczPole(ZNACZNIK_STATEK, rzad, kolumna)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            wspolrzedne_pol.append((rzad, kolumna))
                            #test
                            # print kierunek.center(3 * self.kolumny), str(rzad), str(kolumna)
                        else:
                            rzad -= 1

            self.rysujSie() # do testów
            licznik_iteracji += 1

        self.statki.append(Statek(wspolrzedne_pol))

    def umiescObwiednieStatku(self, statek):
        """Oznacza pola obwiedni wskazanego statku"""
        
        # wystarczy zaznaczyć wszystkich 8 bezposrednich sąsiadów danego punktu (sprawdzając za kazdym razem czy sa w planszy i czy sa wolne)
        for wspolrzedne_pola in statek.wspolrzedne_pol:
            rzad, kolumna = wspolrzedne_pola
            a = 0 # współczynnik przesunięcia w pionie (x)
            b = 0 # współczynnik przesunięcia w poziomie (y)

            for i in xrange(9):
                if i in xrange(3): # 1szy rząd sąsiadów
                    a = -1
                    b = i - 1
                elif i in xrange(3, 6): # 2gi rząd sąsiadów
                    a = 0
                    b = i - 4
                else: # 3ci rząd sąsiadów
                    a = 1
                    b = i - 7

                x = rzad + a
                y = kolumna + b

                if i != 4 and self.czyPoleWPlanszy(x, y) and self.czyPoleWolne(x, y):
                    self.oznaczPole(ZNACZNIK_OBWIEDNIA, x, y)

    def zatopStatek(self, statek):
        """Oznacza pola wskazanego statku jako zatopione"""
        for wspolrzedne_pola in statek.wspolrzedne_pol:
            rzad, kolumna = wspolrzedne_pola
            self.oznaczPole(ZNACZNIK_ZATOPIONY, rzad, kolumna)


class Statek(object):
    """Abstrakcyjna reprezentacja statku"""

    def __init__(self, wspolrzedne_pol):
        super(Statek, self).__init__()
        self.wspolrzedne_pol = sorted(wspolrzedne_pol) # lista krotek ze współrzędnymi (x, y) posortowana najpierw wg "x" potem wg "y"
        self.rozmiar = len(wspolrzedne_pol)

    def czyZatopiony(self, plansza):
        """Sprawdza czy wszystkie pola statku zostały trafione na wskazanej planszy"""
        licznik_trafien = 0
        for wspolrzedne_pola in self.wspolrzedne_pol:
            rzad, kolumna = wspolrzedne_pola
            if plansza.pola[rzad - 1, kolumna - 1] == ZNACZNIK_TRAFIONY:
                licznik_trafien += 1
        if licznik_trafien == self.rozmiar:
            return True
        else:
            return False


class Gra(object):
    """Abstrakcyjna reprezentacja interakcji pomiędzy graczem a planszą"""

    def __init__(self):
        super(Gra, self).___init___()
        self.plansza = None

plansza = Plansza(20, 20)
plansza.rysujSie()
plansza.umiescStatek(15, 10, 10)
statek = plansza.statki[0]
plansza.umiescObwiednieStatku(statek)
plansza.rysujSie()
plansza.zatopStatek(statek)
plansza.rysujSie()
# plansza.rysujSie()    