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
        self.pola = self.stworzPola()  # lista rzędów (list) pól
        # self.pola = [ZNACZNIKI["pusty"] * kolumny for rzad in xrange(rzedy)]  # lista stringów odpowiadających rzędom pól planszy
        self.statki = []

    def stworzPola(self):
        """Tworzy pola planszy"""
        pola = []
        for y in xrange(1, self.rzedy + 1):
            rzad = []
            for x in xrange(1, self.kolumny + 1):
                rzad.append(Pole(x, y))
            pola.append(rzad)
        return pola

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
            print "  ".join([pole.znacznik for pole in self.pola[i]])

    def podajPole(self, kolumna, rzad):
        """Podaje wskazane pole"""
        return self.pola[rzad - 1][kolumna - 1]

    def oznaczPole(self, znacznik, kolumna, rzad):
        """Oznacza wskazane polę wskazanym znacznikiem"""
        self.pola[rzad - 1][kolumna - 1].znacznik = znacznik

    def czyPolePuste(self, kolumna, rzad):
        """Sprawdza czy wskazane pole jest puste"""
        if self.pola[rzad - 1][kolumna - 1].znacznik == ZNACZNIKI["pusty"]:
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
        ozn_pola = []

        while licznik_oznaczen < rozmiar:

            if licznik_iteracji > rozmiar * 5:  # za dużo iteracji - NIEUDANE UMIESZCZENIE
                return None
            # do testów
            # print
            # komunikat = "ITERACJA " + str(licznik_iteracji + 1)
            # print komunikat.center(3 * self.kolumny)

            if licznik_iteracji == 0:  # pole startowe
                if self.czyPoleWPlanszy(kolumna, rzad) and self.czyPolePuste(kolumna, rzad):
                    self.oznaczPole(ZNACZNIKI["statek"], kolumna, rzad)
                    licznik_oznaczen += 1
                    ozn_pola.append(self.podajPole(kolumna, rzad))
                else:
                    return None  # NIEUDANE UMIESZCZENIE
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
                                sciezka.pop()
                                # print "Cofam: '" + sciezka.pop() + "'"  # test
                            elif ostatni_kierunek == "lewo":
                                kolumna += 1
                                sciezka.pop()
                                # print "Cofam: '" + sciezka.pop() + "'"  # test
                            elif ostatni_kierunek == "gora":
                                rzad += 1
                                sciezka.pop()
                                # print "Cofam: '" + sciezka.pop() + "'"  # test
                            elif ostatni_kierunek == "dol":
                                rzad -= 1
                                sciezka.pop()
                                # print "Cofam: '" + sciezka.pop() + "'"  # test
                            # print "Uciekam z zapetlenia"  # test
                            break

                        else:  # nie ma gdzie wracać, jesteśmy w punkcie startowym - NIEUDANE UMIESZCZENIE statku
                            for pole in ozn_pola:  # czyszczenie planszy
                                kolumna, rzad = pole.podajWspolrzedne()
                                self.oznaczPole(ZNACZNIKI["pusty"], kolumna, rzad)
                            return None

                    kierunek = kierunki[randint(0, len(kierunki) - 1)]
                    if kierunek == "prawo":
                        kolumna += 1
                        if self.czyPoleWPlanszy(kolumna, rzad) and self.czyPolePuste(kolumna, rzad):
                            self.oznaczPole(ZNACZNIKI["statek"], kolumna, rzad)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            ozn_pola.append(self.podajPole(kolumna, rzad))
                            # test
                            # print kierunek.center(3 * self.kolumny), str(rzad), str(kolumna)
                        else:
                            kolumna -= 1
                            kierunki.remove(kierunek)
                    elif kierunek == "lewo":
                        kolumna -= 1
                        if self.czyPoleWPlanszy(kolumna, rzad) and self.czyPolePuste(kolumna, rzad):
                            self.oznaczPole(ZNACZNIKI["statek"], kolumna, rzad)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            ozn_pola.append(self.podajPole(kolumna, rzad))
                            # test
                            # print kierunek.center(3 * self.kolumny), str(rzad), str(kolumna)
                        else:
                            kolumna += 1
                            kierunki.remove(kierunek)
                    elif kierunek == "gora":
                        rzad -= 1
                        if self.czyPoleWPlanszy(kolumna, rzad) and self.czyPolePuste(kolumna, rzad):
                            self.oznaczPole(ZNACZNIKI["statek"], kolumna, rzad)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            ozn_pola.append(self.podajPole(kolumna, rzad))
                            # test
                            # print kierunek.center(3 * self.kolumny), str(rzad), str(kolumna)
                        else:
                            rzad += 1
                            kierunki.remove(kierunek)
                    else:  # idziemy w dół
                        rzad += 1
                        if self.czyPoleWPlanszy(kolumna, rzad) and self.czyPolePuste(kolumna, rzad):
                            self.oznaczPole(ZNACZNIKI["statek"], kolumna, rzad)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            ozn_pola.append(self.podajPole(kolumna, rzad))
                            # test
                            # print kierunek.center(3 * self.kolumny), str(rzad), str(kolumna)
                        else:
                            rzad -= 1
                            kierunki.remove(kierunek)

            # self.rysujSie() #test
            licznik_iteracji += 1

        return Statek(ozn_pola)

    def umiescObwiednieStatku(self, statek):
        """Umieszcza na planszy obwiednię wskazanego statku"""

        # wystarczy zaznaczyć wszystkich 8 bezpośrednich sąsiadów danego punktu (sprawdzając za kazdym razem czy sa w planszy i czy sa puste)
        for pole in statek.pola:
            kolumna, rzad = pole.podajWspolrzedne()
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
                    self.oznaczPole(ZNACZNIKI["obwiednia"], x, y)

    def zatopStatek(self, statek):
        """Oznacza pola wskazanego statku jako zatopione"""
        for pole in statek.pola:
            kolumna, rzad = pole.podajWspolrzedne()
            self.oznaczPole(ZNACZNIKI["zatopiony"], kolumna, rzad)

    def wypelnijStatkami(self, zapelnienie=15, odch_st=9, prz_mediany=-7):
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


class Pole(object):
    """Abstrakcyjna reprezentacja pola planszy"""

    def __init__(self, kolumna, rzad, znacznik=ZNACZNIKI["pusty"]):
        super(Pole, self).__init__()
        self.kolumna = kolumna
        self.rzad = rzad
        self.znacznik = znacznik

    def podajWspolrzedne(self):
        return (self.kolumna, self.rzad)


class Statek(object):
    """Abstrakcyjna reprezentacja statku"""

    nazwy = sklonujNazwyStatkow()  # słownik zawierający listy (wg rang statków) aktualnie dostępnych nazw dla instancji klasy
    rzymskie = dict([[ranga, [u"II", u"III", u"IV", u"V", u"VI", u"VII", u"VIII", u"IX", u"X"]] for ranga in NAZWY_RANG])

    def __init__(self, pola):
        super(Statek, self).__init__()
        self.pola = sorted(pola, key=lambda p: p.podajWspolrzedne())  # lista pól posortowana wg współrzędnych - najpierw wg "x" potem wg "y"
        self.rozmiar = len(pola)
        self.ranga = RANGI_STATKOW[self.rozmiar]
        self.nazwa = self.losujNazwe(self.ranga)

    @classmethod
    def zresetujNazwy(cls, ranga):
        """
        Resetuje wyczerpaną listę nazw dostępnych dla instancji klasy, pobierając ze stałej modułu wspolne.py pełną listę nazw, dodając do każdej nazwy kolejny liczebnik rzymski i zwracając tak zmienioną listę
        """
        assert len(cls.rzymskie[ranga]) > 0, "Wyczerpano liczbe mozliwych nazw dla statkow"
        rzymska = cls.rzymskie[ranga][0]

        nowa_lista = []
        for nazwa in NAZWY_STATKOW[ranga]:
            nowa_lista.append(u" ".join([nazwa, rzymska]))

        cls.rzymskie[ranga].remove(rzymska)
        return nowa_lista

    def losujNazwe(self, ranga):
        """
        Losuje nazwę dla statku o określonej randze z listy w atrybucie klasy. By zapewnić unikalność statku, nazwa po użyciu jest usuwana z listy
        """
        lista_nazw = Statek.nazwy[ranga]
        if len(lista_nazw) > 0:
            nazwa = choice(lista_nazw)
        else:  # obsługa wyczerpania dostępnych nazw dla danej rangi
            lista_nazw = Statek.nazwy[ranga] = self.zresetujNazwy(ranga)
            nazwa = choice(lista_nazw)

        lista_nazw.remove(nazwa)
        return nazwa

    def czyZatopiony(self, plansza):
        """Sprawdza czy wszystkie pola statku zostały trafione na wskazanej planszy"""
        licznik_trafien = 0
        for pole in self.pola:
            kolumna, rzad = pole.podajWspolrzedne()
            if plansza.pola[rzad - 1][kolumna - 1] == ZNACZNIKI["trafiony"]:
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
