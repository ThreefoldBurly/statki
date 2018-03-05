"""

    statki.ranga
    ~~~~~~~~~~~~~~

    Ranga statku.

"""

from collections import namedtuple
from random import choice

Rangi = namedtuple("Rangi", "kuter patrolowiec korweta fregata niszczyciel krazownik pancernik")


class Ranga:
    """
    Reprezentacja rangi statku. Dane dla obiektów tej klasy są parsowane przez 'statek.pamiec.Parser'
    """

    def __init__(self, nazwa, symbol, zakres, sila_ognia, nazwy_statkow, liczebniki, liczba_mnoga, biernik):
        self.nazwa = nazwa
        self.symbol = symbol
        self.zakres = zakres  # zakres rozmiarów statku
        self.sila_ognia = sila_ognia
        self.nazwy_statkow = nazwy_statkow
        self.pula_nazw_statkow = self.nazwy_statkow[:]  # pula aktualnie dostępnych nazw statków dla tej rangi
        self.liczebniki = ["II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]  # liczebniki rzymskie dodawane do nazw statków po wyczerpaniu puli (potrzebne bardziej do testów - przy założonych ograniczeniach rozmiarów planszy (i w efekcie możliwej ilości statków) konieczność użycia tej zmiennej jest zbliżona do zera)
        self.liczba_mnoga = liczba_mnoga
        self.biernik = biernik

    def __eq__(self, other):
        """
        Przeładowanie operatora '=='. Rangi są równe, jeśli ich nazwy są równe.
        """
        if isinstance(self, other.__class__):
            if self.nazwa == other.nazwa:
                return True
            return False
        return NotImplemented

    def __hash__(self):
        """
        Przeładowanie operatora "==" (dla porównań przy poprawnej obsłudze wyjątkowości w zbiorach)
        """
        return hash(tuple(sorted(self.__dict__.items())))

    def resetuj_pule_nazw(self):
        """
        Resetuje wyczerpaną pulę nazw statków, dodając do każdej nazwy kolejny liczebnik rzymski. Przy rozmiarach planszy dyktowanych przez GUI prawdopodobieństwo konieczności użycia chociaż raz tej metody jest nikłe.
        """
        assert len(self.liczebniki) > 0, "Wyczerpano liczbę możliwych nazw dla statków ({})".format(len(self.nazwy_statkow * len(liczebniki)))

        liczebnik = self.liczebniki.pop(0)
        self.pula_nazw = [" ".join([nazwa, liczebnik]) for nazwa in self.nazwy_statkow]

    def losuj_nazwe_statku(self):
        """
        Losuje nazwę dla statku z dostępnej puli nazw. By zapewnić unikalność statku, nazwa po użyciu jest usuwana z puli.
        """
        if len(self.pula_nazw_statkow) < 1:
            self.resetuj_pule_nazw()
        nazwa = choice(self.pula_nazw_statkow)
        self.pula_nazw_statkow.remove(nazwa)
        return nazwa
