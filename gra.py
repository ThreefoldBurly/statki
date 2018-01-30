#!/usr/bin/env python3

"""
Mechanika i przepływ gry w rozbiciu na tury, rundy i graczy - wg opisu zawartego w meta/zasady.md.
"""
from copy import deepcopy


class Gra:
    """
    Abstrakcyjna reprezentacja gry.
    """

    def __init__(self, plansza_gracza, plansza_przeciwnika):
        self.gracz = Gracz(plansza_gracza)
        self.przeciwnik = Gracz(plansza_przeciwnika)


class Gracz:
    """
    Abstrakcyjna reprezentacja gracza. Śledzi kolejne tury danego gracza.
    """
    # TODO: sprawdzić czy ta klasa jest w ogóle potrzebna (na razie wygląda na to, że zamiast niej wystarczyłoby w klasie Gra zamienić zmienne 'gracz' i 'przeciwnik' na listę tur gracza i listę tur przeciwnika)

    def __init__(self, plansza):
        self.plansza = plansza
        self.tura = Tura(self.plansza)
        self.tury = [self.tura]

    def dodaj_ture(self):
        """Tworzy nową turę i dodaje do listy tur"""
        self.tura = Tura(self.plansza)
        self.tury.append(self.tura)


class Tura:
    """
    Abstrakcyjna reprezentacja tury.
    Śledzi kolejne rundy poprzez monitorowanie własnej listy statków, które jeszcze nie miały swojej rundy.
    """

    def __init__(self, plansza):
        self.plansza = plansza
        self.statki = self.plansza.niezatopione[:]  # śledzona jest tylko ilość elementów nie ich zawartość, więc wystarczy płytka kopia
        self.runda = Runda(self.plansza)
        self.rundy = [self.runda]

    def dodaj_runde(self):
        """Tworzy nową rundę i dodaje do listy rund"""
        self.statki.remove(self.rundy[-1].statek)
        self.runda = Runda(self.plansza)
        self.rundy.append(self.runda)


class Runda:
    """
    Abstrakcyjna reprezentacja rundy.
    Śledzi salwy statku, który strzela w tej rundzie oraz strzały otrzymane od przeciwnika. Na koniec rundy zapisuje stan gry (po stronie danego gracza) w postaci migawki planszy.
    """

    def __init__(self, plansza):
        self.plansza = plansza
        self.migawka_planszy = None  # wykonywana na koniec rundy
        self.statek = None  # wartość ustalana przez użytkownika via GUI
        # zmienne poniżej przechowują tylko wspólrzędne zamiast pełnych obiektów pól planszy przeciwnika, żeby zachować kompartmentację informacji, co będzie miało znaczenie przy implementacji komunikacji sieciowej dla gry osobowej (aplikacje będą wysyłać sobie nawzajem tylko proste liczby całkowite)
        self.strzaly_wyslane = []  # lista krotek współrzędnych pól na planszy przeciwnika (kolumna, rzad), w które zostały oddane strzały
        self.strzaly_otrzymane = []  # lista krotek współrzędnych pól na planszy gracza (kolumna, rzad), w które strzelił przeciwnik

    def wybierz_statek(self, statek):
        self.statek = statek

    def dodaj_strzal_wyslany(self, kolumna, rzad):
        self.strzały_wyslane.append((kolumna, rzad))

    def dodaj_strzal_otrzymany(self, kolumna, rzad):
        self.strzały_otrzymane.append((kolumna, rzad))

    def zrob_migawke(self):
        self.migawka_planszy = deepcopy(self.plansza)
