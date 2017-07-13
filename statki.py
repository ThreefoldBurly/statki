#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gra w statki na planszy o arbitralnym rozmiarze.
"""

from random import randint

from wspolne import *

class Plansza(object):
    """Abstrakcyjna reprezentacja planszy"""

    def __init__(self, kolumny, rzedy, zapelnienie = 10, granulacja = 4.0):
        super(Plansza, self).__init__()
        self.kolumny = kolumny # max 69 ze względu na stout
        self.rzedy = rzedy # max. 99
        self.rozmiar = rzedy * kolumny
        self.pola = [ZNACZNIK_PUSTY * kolumny for rzad in xrange(rzedy)] #lista stringów odpowiadających rzędom pól planszy
        self.statki = []

        # UWAGA 1 - plansze o większym rozmiarze wymagają wyższej wartości zapełnienia dla uzyskania tego samego efektu (wynika to z tego że obwiednie statków zajmują stosunkowo więcej miejsca na małej planszy)
        # UWAGA 2 - większe plansze wymagają większej granulacji  
        self.zapelnienie = zapelnienie # stosunek sumarycznego rozmiaru umieszczonych statków do rozmiaru planszy (w procentach)
        #TODO: poprawić obsługę granulacji - większe plansze wymagają większej granulacji (rozumianej jako argument tej metody) dla uzyskania tego samego efektu. Rozważyć wprowadzenie podobnej poprawki do zapełnienia
        self.granulacja = granulacja # współczynnik ograniczający umieszczanie dużych statków na planszy. Musi być większy lub równy 1.0. Przy 1.0 - brak ograniczenia

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

    def oznaczPole(self, znacznik, kolumna, rzad):
        """Oznacza wskazane polę wskazanym znacznikiem"""
        rzad_lista = list(self.pola[rzad - 1])
        rzad_lista[kolumna - 1] = znacznik    
        nowy_rzad = "".join(rzad_lista)
        self.pola[rzad - 1] = nowy_rzad

    def czyPolePuste(self, kolumna, rzad):
        """Sprawdza czy wskazane pole jest puste"""
        if self.pola[rzad - 1][kolumna - 1] == ZNACZNIK_PUSTY:
            return True
        else:
            return False

    def czyPoleWPlanszy(self, kolumna, rzad):
        """Sprawdza czy wskazane pole jest w obrębie planszy"""
        if rzad < 1 or rzad > self.rzedy or kolumna < 1 or kolumna > self.kolumny:
            return False
        else:
            return True 

    def umiescStatek(self, rozmiar, kolumna, rzad):
        """
        Stara się umieścić statek o podanym rozmiarze na planszy. Statek rozrasta się w przypadkowych kierunkach ze wskazanego pola początkowego. W razie sukcesu metoda zwraca umieszczony statek, w razie porażki zwraca None (czyszcząc oznaczone wcześniej pola). 
        """

        licznik_oznaczen = 0
        licznik_iteracji = 0
        sciezka = []
        wspolrz_ozn_pol = []

        while licznik_oznaczen < rozmiar:

            
            # do testów
            assert licznik_iteracji < rozmiar * 3, "Petla metody umiescStatek() klasy Plansza probowala umiescic statek w zbyt wielu iteracjach (prog = 3 * rozmiar statku). Cos jest nie tak. Sprawdz logike metody"
            print
            komunikat = "ITERACJA " + str(licznik_iteracji + 1)
            print komunikat.center(3 * self.kolumny)
            

            if licznik_iteracji == 0: # pole startowe
                if self.czyPoleWPlanszy(kolumna, rzad) and self.czyPolePuste(kolumna, rzad):
                    self.oznaczPole(ZNACZNIK_STATEK, kolumna, rzad)
                    licznik_oznaczen += 1
                    wspolrz_ozn_pol.append((kolumna, rzad))
                else:
                    return None
            else:
                oznaczono = False
                kierunki = KIERUNKI[:]

                while not oznaczono:

                    # obsługa zapętlenia - pętla może się wykonać maksymalnie 4 razy (tyle ile możliwych kierunków ruchu)
                    if len(kierunki) < 1: # wyczerpaliśmy wszystkie możliwe kierunki - trzeba wracać (o ile jest gdzie!)
                        if len(sciezka) > 0:
                            ostatni_kierunek = sciezka[len(sciezka) - 1]
                            if ostatni_kierunek == "prawo":
                                kolumna -= 1
                                print "Cofam: '" + sciezka.pop() + "'" #test
                            elif ostatni_kierunek == "lewo":
                                kolumna += 1
                                print "Cofam: '" + sciezka.pop() + "'" #test
                            elif ostatni_kierunek == "gora":
                                rzad += 1
                                print "Cofam: '" + sciezka.pop() + "'" #test
                            elif ostatni_kierunek == "dol":
                                rzad -= 1
                                print "Cofam: '" + sciezka.pop() + "'" #test
                            print "Uciekam z zapetlenia" #test

                            break
                        else: # nie ma gdzie wracać, jesteśmy w punkcie startowym - NIEUDANE UMIESZCZENIE statku
                            for wspolrzedne_pola in wspolrz_ozn_pol: # czyszczenie planszy
                                kolumna, rzad = wspolrzedne_pola
                                self.oznaczPole(ZNACZNIK_PUSTY, kolumna, rzad)
                            return None

                    kierunek = kierunki[randint(0, len(kierunki) - 1)]
                    if kierunek == "prawo":
                        kolumna += 1
                        if self.czyPoleWPlanszy(kolumna, rzad) and self.czyPolePuste(kolumna, rzad):
                            self.oznaczPole(ZNACZNIK_STATEK, kolumna, rzad)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            wspolrz_ozn_pol.append((kolumna, rzad))
                            #test
                            # print kierunek.center(3 * self.kolumny), str(rzad), str(kolumna)
                        else:
                            kolumna -= 1
                            kierunki.remove(kierunek)
                    elif kierunek == "lewo":
                        kolumna -= 1
                        if self.czyPoleWPlanszy(kolumna, rzad) and self.czyPolePuste(kolumna, rzad):
                            self.oznaczPole(ZNACZNIK_STATEK, kolumna, rzad)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            wspolrz_ozn_pol.append((kolumna, rzad))
                            #test
                            # print kierunek.center(3 * self.kolumny), str(rzad), str(kolumna)
                        else:
                            kolumna += 1
                            kierunki.remove(kierunek)
                    elif kierunek == "gora":
                        rzad -= 1
                        if self.czyPoleWPlanszy(kolumna, rzad) and self.czyPolePuste(kolumna, rzad):
                            self.oznaczPole(ZNACZNIK_STATEK, kolumna, rzad)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            wspolrz_ozn_pol.append((kolumna, rzad))
                            #test
                            # print kierunek.center(3 * self.kolumny), str(rzad), str(kolumna)
                        else:
                            rzad += 1
                            kierunki.remove(kierunek)
                    else: # idziemy w dół
                        rzad += 1
                        if self.czyPoleWPlanszy(kolumna, rzad) and self.czyPolePuste(kolumna, rzad):
                            self.oznaczPole(ZNACZNIK_STATEK, kolumna, rzad)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            wspolrz_ozn_pol.append((kolumna, rzad))
                            #test
                            # print kierunek.center(3 * self.kolumny), str(rzad), str(kolumna)
                        else:
                            rzad -= 1
                            kierunki.remove(kierunek)

            # self.rysujSie() #test
            licznik_iteracji += 1

        print "Umieszczam statek [%d]" % len(wspolrz_ozn_pol) #test
        return Statek(wspolrz_ozn_pol)

    def umiescObwiednieStatku(self, statek):
        """Umieszcza na planszy obwiednię wskazanego statku"""
        
        # wystarczy zaznaczyć wszystkich 8 bezposrednich sąsiadów danego punktu (sprawdzając za kazdym razem czy sa w planszy i czy sa puste)
        for wspolrzedne_pola in statek.wspolrzedne_pol:
            kolumna, rzad = wspolrzedne_pola
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

                x = kolumna + a
                y = rzad + b

                if i != 4 and self.czyPoleWPlanszy(x, y) and self.czyPolePuste(x, y):
                    self.oznaczPole(ZNACZNIK_OBWIEDNIA, x, y)

    def zatopStatek(self, statek):
        """Oznacza pola wskazanego statku jako zatopione"""
        for wspolrzedne_pola in statek.wspolrzedne_pol:
            kolumna, rzad = wspolrzedne_pola
            self.oznaczPole(ZNACZNIK_ZATOPIONY, kolumna, rzad)

    def wypelnijStatkami(self):
        """Wypełnia planszę statkami. Każdy kolejny statek ma losowy rozmiar i jest umieszczany w losowym miejscu. O ilości i rozmiarach statków decyduje zapełnienie i granulacja planszy"""
        licznik_iteracji = 0        
        sum_rozmiar_statkow = int(self.rozmiar * self.zapelnienie / 100)
        akt_rozmiar_statkow = sum_rozmiar_statkow

        while akt_rozmiar_statkow > 0:
            # obsługa granulacji
            max_rozmiar_statku = int(akt_rozmiar_statkow / self.granulacja)
            if max_rozmiar_statku == 0:
                max_rozmiar_statku = 1

            rozmiar_statku = randint(1, max_rozmiar_statku)
            pole_startowe_x = randint(1, self.kolumny)
            pole_startowe_y = randint(1, self.rzedy)

            umieszczony_statek = self.umiescStatek(rozmiar_statku, pole_startowe_x, pole_startowe_y)

            if umieszczony_statek is not None:
                self.umiescObwiednieStatku(umieszczony_statek)
                self.statki.append(umieszczony_statek)
                akt_rozmiar_statkow -= rozmiar_statku

            #obsługa wyjścia    
            if licznik_iteracji > sum_rozmiar_statkow * 10: # wielkość do przetestowania
                print "Ilosc iteracji petli zapelniajacej plansze statkami wieksza od oczekiwanej. Nastapilo przedwczesne przerwanie petli. Umieszczono mniej statkow" #test
                break

            licznik_iteracji += 1


class Statek(object):
    """Abstrakcyjna reprezentacja statku"""

    def __init__(self, wspolrzedne_pol):
        super(Statek, self).__init__()
        self.wspolrzedne_pol = sorted(wspolrzedne_pol) # lista krotek ze współrzędnymi (x, y) pól statku posortowana najpierw wg "x" potem wg "y"
        self.rozmiar = len(wspolrzedne_pol)
        #self.ranga
        #self.nazwa

    def czyZatopiony(self, plansza):
        """Sprawdza czy wszystkie pola statku zostały trafione na wskazanej planszy"""
        licznik_trafien = 0
        for wspolrzedne_pola in self.wspolrzedne_pol:
            kolumna, rzad = wspolrzedne_pola
            if plansza.pola[rzad - 1][ kolumna - 1] == ZNACZNIK_TRAFIONY:
                licznik_trafien += 1
        if licznik_trafien == self.rozmiar:
            return True
        else:
            return False


class Gra(object):
    """Abstrakcyjna reprezentacja interakcji pomiędzy graczem a planszą"""

    def __init__(self):
        super(Gra, self).__init__()
        self.plansza = None

#testy
plansza = Plansza(25, 25)
plansza.rysujSie()
plansza.wypelnijStatkami()
plansza.rysujSie()
