#!/usr/bin/env python3

"""
Mechanika i przepływ gry w rozbiciu na tury, rundy i graczy - wg opisu zawartego w meta/zasady.md.
"""
from copy import deepcopy

from plansza import Salwa

# class Gra:
#     """
#     Abstrakcyjna reprezentacja gry.
#     """

#     def __init__(self, plansza_gracza, plansza_przeciwnika):
#         self.gracz = Gracz(plansza_gracza)
#         self.przeciwnik = Gracz(plansza_przeciwnika)


class Gracz:
    """
    Abstrakcyjna reprezentacja gracza. Śledzi kolejne tury.
    """

    def __init__(self, plansza):
        self.plansza = plansza
        self.tura = Tura(self.plansza)
        self.tury = [self.tura]
        self.ofiary = []  # zatopione statki przeciwnika

    def dodaj_ture(self):
        """Tworzy nową turę i dodaje do listy tur"""
        self.tura = Tura(self.plansza)
        self.tury.append(self.tura)

    def podaj_info_o_rundzie(self):
        """Zwraca informację o turze w formacie: `tura #[liczba] / runda #[liczba] ([ilość statków])."""
        info = "tura #" + str(len(self.tury))
        info += " / runda #" + str(len(self.tura.rundy))
        info += " (" + str(len(self.tura.statki)) + ")"
        return info  # w minuskule!


class Tura:
    """
    Abstrakcyjna reprezentacja tury.
    Śledzi kolejne rundy poprzez monitorowanie własnej listy statków, które jeszcze nie miały swojej rundy. Na koniec każdej rundy zapisuje stan gry (po stronie danego gracza) w postaci migawki planszy
    """

    def __init__(self, plansza):
        self.plansza = plansza
        self.migawka_planszy = None  # wykonywana na koniec każdej rundy
        self.statki = self.plansza.niezatopione[:]  # śledzona jest tylko ilość elementów nie ich zawartość, więc wystarczy płytka kopia
        self.runda = Runda(self.statki[0])
        self.rundy = [self.runda]

    def dodaj_runde(self):
        """Tworzy nową rundę i dodaje do listy rund"""
        self.statki.remove(self.runda.statek)
        self.zrob_migawke()
        self.runda = Runda(self.statki[0])
        self.rundy.append(self.runda)

    def zrob_migawke(self):
        """Tworzy migawkę (głęboką kopię) obiektu planszy i zapisuje w zmiennej."""
        self.migawka_planszy = deepcopy(self.plansza)


class Runda:
    """
    Abstrakcyjna reprezentacja rundy.
    Śledzi salwy statku, który strzela w tej rundzie oraz salwy otrzymane od przeciwnika. . Defaultowo startuje z pierwszym statkiem z listy tury
    """

    def __init__(self, statek):
        self.statek = statek  # wartość zmieniana przez użytkownika via GUI
        # TODO: inicjalizacja śledzenia salw po pierwszym ataku
        self.salwy_oddane = []
        self.salwy_otrzymane = None  # lista salw przeciwnika otrzymywana i zapisywana na początku rundy

    def dodaj_oddana_salwe(self, plansza, *wspolrzedne):
        """Tworzy salwę z otrzymanej listy krotek współrzędnych i dodaje do odpowiedniej listy."""
        pola = []
        for kolumna, rzad in wspolrzedne:
            if plansza.czy_pole_w_planszy(kolumna, rzad):
                pola.append(plansza.podaj_pole(kolumna, rzad))
        self.salwy_oddane.append(Salwa(pola))
