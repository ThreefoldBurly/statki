#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gra w statki na planszy o arbitralnym rozmiarze.
"""

from random import randint, choice

from wspolne import *


class Plansza(object):
    """Abstrakcyjna reprezentacja planszy do gry w statki"""

    def __init__(self, kolumny, rzedy):
        super(Plansza, self).__init__()
        self.kolumny = kolumny  # max 69 ze względu na stout - ograniczenie nie zawarte w kodzie
        self.rzedy = rzedy  # max. 99 - ograniczenie nie zawarte w kodzie
        self.rozmiar = rzedy * kolumny
        self.pola = [ZNACZNIK_PUSTY * kolumny for rzad in xrange(rzedy)]  # lista stringów odpowiadających rzędom pól planszy
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

            if licznik_iteracji > rozmiar * 5:  # za dużo iteracji - nieudane umieszczenie
                return None
            # do testów
            # print
            # komunikat = "ITERACJA " + str(licznik_iteracji + 1)
            # print komunikat.center(3 * self.kolumny)

            if licznik_iteracji == 0:  # pole startowe
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
                    if len(kierunki) < 1:  # wyczerpaliśmy wszystkie możliwe kierunki - trzeba wracać (o ile jest gdzie!)
                        if len(sciezka) > 0:
                            ostatni_kierunek = sciezka[len(sciezka) - 1]
                            if ostatni_kierunek == "prawo":
                                kolumna -= 1
                                # print "Cofam: '" + sciezka.pop() + "'"  # test
                            elif ostatni_kierunek == "lewo":
                                kolumna += 1
                                # print "Cofam: '" + sciezka.pop() + "'"  # test
                            elif ostatni_kierunek == "gora":
                                rzad += 1
                                # print "Cofam: '" + sciezka.pop() + "'"  # test
                            elif ostatni_kierunek == "dol":
                                rzad -= 1
                                # print "Cofam: '" + sciezka.pop() + "'"  # test
                            # print "Uciekam z zapetlenia"  # test

                            break
                        else:  # nie ma gdzie wracać, jesteśmy w punkcie startowym - NIEUDANE UMIESZCZENIE statku
                            for wspolrzedne_pola in wspolrz_ozn_pol:  # czyszczenie planszy
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
                            # test
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
                            # test
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
                            # test
                            # print kierunek.center(3 * self.kolumny), str(rzad), str(kolumna)
                        else:
                            rzad += 1
                            kierunki.remove(kierunek)
                    else:  # idziemy w dół
                        rzad += 1
                        if self.czyPoleWPlanszy(kolumna, rzad) and self.czyPolePuste(kolumna, rzad):
                            self.oznaczPole(ZNACZNIK_STATEK, kolumna, rzad)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            wspolrz_ozn_pol.append((kolumna, rzad))
                            # test
                            # print kierunek.center(3 * self.kolumny), str(rzad), str(kolumna)
                        else:
                            rzad -= 1
                            kierunki.remove(kierunek)

            # self.rysujSie() #test
            licznik_iteracji += 1

        return Statek(wspolrz_ozn_pol)

    def umiescObwiednieStatku(self, statek):
        """Umieszcza na planszy obwiednię wskazanego statku"""

        # wystarczy zaznaczyć wszystkich 8 bezpośrednich sąsiadów danego punktu (sprawdzając za kazdym razem czy sa w planszy i czy sa puste)
        for wspolrzedne_pola in statek.wspolrzedne_pol:
            kolumna, rzad = wspolrzedne_pola
            a = 0  # współczynnik przesunięcia w pionie (x)
            b = 0  # współczynnik przesunięcia w poziomie (y)

            for i in xrange(9):
                if i in xrange(3):  # 1szy rząd sąsiadów
                    a = -1
                    b = i - 1
                elif i in xrange(3, 6):  # 2gi rząd sąsiadów
                    a = 0
                    b = i - 4
                else:  # 3ci rząd sąsiadów
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

    def wypelnijStatkami(self, zapelnienie=15, odch_st=9, prz_mediany=-8):
        """
        Wypełnia planszę statkami. Każdy kolejny statek ma losowy rozmiar w zakresie 1-20 i jest umieszczany w losowym miejscu. O ilości i rozmiarach statków decydują parametry metody
        """
        # zapelnienie to wyrażony w procentach stosunek sumarycznego rozmiaru umieszczonych statków do rozmiaru planszy

        # odch_st to odchylenie standardowe w rozkładzie Gaussa, z którego losowany jest rozmiar statku
        # czym wyższa wartość, tym większy rozrzut rozmiarów

        # prz_mediany to przesunięcie mediany w rozkładzie Gaussa, z którego losowany jest rozmiar statku
        # wartość ujemna spowoduje losowanie większej ilości małych statków
        # wartość dodatnia spowodują losowanie większej ilości dużych statków
        # zero (brak przesunięcia) powoduje losowanie wg standardowego rozkładu normalnego,
        # gdzie mediana jest średnią arytmetyczną przedziału losowania

        # wartości domyślne parametrów zostały ustalone po testach
        # większa granulacja rozmiarów statków (z zapewnieniem sporadycznego występowania dużych statków) zapewnia ciekawszą grę
        min_rozmiar_statku = 1
        max_rozmiar_statku = 20
        mediana = (min_rozmiar_statku + max_rozmiar_statku) / 2.0  # 10.5

        licznik_iteracji = 0
        sum_rozmiar_statkow = int(self.rozmiar * zapelnienie / 100)
        akt_rozmiar_statkow = sum_rozmiar_statkow

        while akt_rozmiar_statkow > 0:
            rozmiar_statku = podajIntZRozkladuGaussa(mediana, odch_st, min_rozmiar_statku, max_rozmiar_statku, prz_mediany)
            if rozmiar_statku > akt_rozmiar_statkow:
                continue
            pole_startowe_x = randint(1, self.kolumny)
            pole_startowe_y = randint(1, self.rzedy)

            umieszczony_statek = self.umiescStatek(rozmiar_statku, pole_startowe_x, pole_startowe_y)

            if umieszczony_statek is not None:
                self.umiescObwiednieStatku(umieszczony_statek)
                self.statki.append(umieszczony_statek)
                # print "\nUmieszczony statek: %s [%d]" % (umieszczony_statek.ranga, umieszczony_statek.rozmiar)  # test
                akt_rozmiar_statkow -= rozmiar_statku

            # obsługa wyjścia
            if licznik_iteracji > sum_rozmiar_statkow * 10:  # wielkość do przetestowania
                print u"Ilość iteracji pętli zapełniającej planszę statkami większa od oczekiwanej. Nastąpiło przedwczesne przerwanie petli. Umieszczono mniej statków"  # test
                break

            licznik_iteracji += 1

        self.statki.sort(key=lambda s: s.rozmiar, reverse=True)  # nie wierzę że to było takie proste!

        # do testów
        sum_rozmiar = 0
        for statek in self.statki:
            sum_rozmiar += statek.rozmiar
            print '\nUmieszczony statek: %s "%s" [%d]' % (statek.ranga, statek.nazwa, statek.rozmiar)
        print u"\nWszystkich umieszczonych statków: %d. Ich sumaryczny rozmiar: [%d]" % (len(self.statki), sum_rozmiar)


class Statek(object):
    """Abstrakcyjna reprezentacja statku"""

    def __init__(self, wspolrzedne_pol):
        super(Statek, self).__init__()
        self.wspolrzedne_pol = sorted(wspolrzedne_pol)  # lista krotek ze współrzędnymi (x, y) pól statku posortowana najpierw wg "x" potem wg "y"
        self.rozmiar = len(wspolrzedne_pol)
        self.ranga = RANGI_STATKOW[self.rozmiar]
        self.nazwa = self.losujNazwe(self.ranga)

    def losujNazwe(self, ranga):
        """Losuje nazwę dla statku o określonej randze z listy w słowniku NAZWY_STATKOW modulu wspolne.py. By zapewnić unikalność statku, nazwa po użyciu jest usuwana z listy"""
        lista_nazw = NAZWY_STATKOW[ranga]
        nazwa = choice(lista_nazw)
        lista_nazw.remove(nazwa)
        return nazwa

    def czyZatopiony(self, plansza):
        """Sprawdza czy wszystkie pola statku zostały trafione na wskazanej planszy"""
        licznik_trafien = 0
        for wspolrzedne_pola in self.wspolrzedne_pol:
            kolumna, rzad = wspolrzedne_pola
            if plansza.pola[rzad - 1][kolumna - 1] == ZNACZNIK_TRAFIONY:
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


# testy
plansza = Plansza(50, 50)
plansza.rysujSie()
plansza.wypelnijStatkami()
plansza.rysujSie()
