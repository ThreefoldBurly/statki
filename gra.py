#!/usr/bin/env python3

"""
Mechanika i przepływ gry w rozbiciu na tury, rundy i graczy - wg opisu zawartego w meta/zasady.md.
TODO: któraś z klas tego modułu powinna zapisywać kolejne stany gry na rundę (kolejne migawki 2 głównych obiektów klasy Plansza)
"""
from copy import deepcopy

from plansza import Plansza


class Gra:
    """
    Abstrakcyjna reprezentacja gry
    """

    def __init__(self, gracz, przeciwnik)
        self.gracz = gracz
        self.przeciwnik = przeciwnik


class Gracz:
    """
    Abstrakcyjna reprezentacja gracza
    """

    def __init__(self, plansza)
        self.plansza = plansza
        self.tury = []

    def nowa_tura(self):
        """Tworzy nową turę i dodaje do self.tury"""
        tura = Tura(deepcopy(self.plansza))
        self.tury.append(tura)


class Tura:
    """
    Abstrakcyjna reprezentacja tury
    Otrzymuje przy inicjalizacji KOPIĘ (wykonaną przy pomocy copy.deepcopy) planszy z poprzedniej tury
    """

    def __init__(self, plansza)
        self.plansza = plansza
        self.rundy = []

    def nowa_runda(self):
        """Tworzy nową rundę i dodaje do self.rundy"""
        runda = Runda(deepcopy(self.plansza))
        self.rundy.append(runda)


class Runda:
    """
    Abstrakcyjna reprezentacja rundy.
    Otrzymuje przy inicjalizacji KOPIĘ (wykonaną przy pomocy copy.deepcopy) planszy z poprzedniej rundy
    """

    def __init__(self, plansza)
        self.plansza = plansza
