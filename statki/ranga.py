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
    Ranga statku. Dane dla obiektów tej klasy są parsowane przez 'statek.pamiec.Parser'.
    """

    def __init__(self, nazwa, symbol, zakres, sila_ognia, nazwy_statkow, liczebniki,
                 liczba_mnoga, biernik):
        self.nazwa = nazwa
        self.symbol = symbol
        self.zakres = zakres  # zakres rozmiarów statku
        self.sila_ognia = sila_ognia
        self.nazwy_statkow = nazwy_statkow
        self.pula_nazw = self.nazwy_statkow[:]  # pula aktualnie dostępnych nazw statków dla tej rangi
        self.liczebniki = liczebniki  # liczebniki rzymskie dodawane do nazw statków po wyczerpaniu puli (potrzebne bardziej do testów - przy założonych ograniczeniach rozmiarów planszy (i w efekcie możliwej ilości statków) konieczność użycia tej zmiennej jest zbliżona do zera)
        self.liczba_mnoga = liczba_mnoga
        self.biernik = biernik

        self.max_ilosc_nazw = len(self.nazwy_statkow) * len(self.liczebniki)

    def __eq__(self, other):
        """
        Przeładowanie operatora '=='. Rangi są równe, jeśli ich nazwy, symbole, zakresy, siła ognia i nazwy statków są równe.
        """
        if isinstance(self, other.__class__):
            if (self.nazwa, self.symbol, self.zakres, self.sila_ognia, self.nazwy_statkow) == (other.nazwa, other.symbol, other.zakres, other.sila_ognia, other.nazwy_statkow):
                return True
            return False
        return NotImplemented

    def __hash__(self):
        """
        Zwróć hash rangi. Potrzebne również dla pełnego przeładowania operatora "==" (dla porównań przy poprawnej obsłudze wyjątkowości w zbiorach).
        """
        return hash((self.nazwa, self.symbol, tuple(self.zakres), tuple(self.sila_ognia),
                     tuple(self.nazwy_statkow)))

    def resetuj_pule_nazw(self):
        """
        Resetuj wyczerpaną pulę nazw statków, dodając do każdej nazwy kolejny liczebnik rzymski.
        """
        # przy rozmiarach planszy dyktowanych przez GUI prawdopodobieństwo konieczności użycia chociaż raz tej metody jest nikłe, nie mówiąc o wyczerpaniu całej puli
        if not self.liczebniki:
            raise ValueError("Wyczerpano liczbę możliwych nazw dla statków ({})".format(
                self.max_ilosc_nazw))

        liczebnik = self.liczebniki.pop(0)
        self.pula_nazw = [" ".join([nazwa, liczebnik]) for nazwa in self.nazwy_statkow]

    def losuj_nazwe_statku(self):
        """
        Losuj nazwę dla statku z dostępnej puli nazw. By zapewnić unikalność statku, po użyciu usuń nazwę z puli.
        """
        if not self.pula_nazw:
            self.resetuj_pule_nazw()
        nazwa = choice(self.pula_nazw)
        self.pula_nazw.remove(nazwa)
        return nazwa
