"""

    testy.test_pamiec
    ~~~~~~~~~~~~~~~~~~

    Testy jednostkowe modułu 'statki.pamiec'.

"""

import unittest
from unittest import mock  # TODO: patchowanie statycznego kodu jest bardziej skomplikowane niż się spodziewałem (patch jest aplikowany w momencie gdy wszystko co statyczne jest już dawno załadowane/wykonane)
# TODO: przeprojektować moduł 'pamięc' tak by operacje I/O nie odbywały się przy każdym imporcie
import os

from statki.pamiec import Loader, Parser
from statki.ranga import Ranga

BLEDNY_FORMAT = "plansza\nkolumny\n8,25\nrzedy\n8,30"
SCIEZKA = "testy/dane.json"
DANE_RANG = [{
    "nazwa": "kuter",
    "symbol": "T",
    "zakres": [1, 2],
    "sila_ognia": [1],
    "nazwy_statkow": ["Basior", "Bażant", "Bąk"],
    "liczba_mnoga": ["kuter", "kutry", "kutrów"],
    "biernik": "kuter"
}, {
    "nazwa": "patrolowiec",
    "symbol": "L",
    "zakres": [2, 4],
    "sila_ognia": [2],
    "nazwy_statkow": ["Akinakes", "Assegal", "Atlati"],
    "liczba_mnoga": ["patrolowiec", "patrolowce", "patrolowców"],
    "biernik": "patrolowiec"
}, {
    "nazwa": "korweta",
    "symbol": "W",
    "zakres": [4, 7],
    "sila_ognia": [3],
    "nazwy_statkow": ["Augustówka", "Balista", "Bazyliszek"],
    "liczba_mnoga": ["korweta", "korwety", "korwet"],
    "biernik": "korwetę"
}, {
    "nazwa": "fregata",
    "symbol": "F",
    "zakres": [7, 10],
    "sila_ognia": [2, 2],
    "nazwy_statkow": ["Bartia", "Bałtyk", "Berestia"],
    "liczba_mnoga": ["fregata", "fregaty", "fregat"],
    "biernik": "fregatę"
}, {
    "nazwa": "niszczyciel",
    "symbol": "N",
    "zakres": [10, 13],
    "sila_ognia": [3, 2],
    "nazwy_statkow": ["Anoda", "Bartek", "Białynia"],
    "liczba_mnoga": ["niszczyciel", "niszczyciele", "niszczycieli"],
    "biernik": "niszczyciel"
}, {
    "nazwa": "krążownik",
    "symbol": "K",
    "zakres": [13, 17],
    "sila_ognia": [3, 3],
    "nazwy_statkow": ["Atrox", "Audax", "Beatus"],
    "liczba_mnoga": ["krążownik", "krążowniki", "krążowników"],
    "biernik": "krążownik"
}, {
    "nazwa": "pancernik",
    "symbol": "P",
    "zakres": [17, 21],
    "sila_ognia": [3, 2, 2],
    "nazwy_statkow": ["Abdank", "Akszak", "Amadej"],
    "liczba_mnoga": ["pancernik", "pancerniki", "pancerników"],
    "biernik": "pancernik"
}]
LICZEBNIKI = ["II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]


def stworz_plik_o_blednym_formacie(sciezka):
    """Stworz w podanym miejscu plik o blędnym formacie."""
    with open(sciezka, "w") as zly_plik:
        zly_plik.write(BLEDNY_FORMAT)


def setUpModule():
    stworz_plik_o_blednym_formacie(SCIEZKA)


def tearDownModule():
    os.remove(SCIEZKA)


class TestyWlasne(unittest.TestCase):
    """Testy funkcji tego modułu."""

    def testuj_wlasne__tworzenie_pliku_danych_o_blednym_formacie(self):
        """
        Czy funkcja 'stworz_plik_o_blednym_formacie' tworzy odpowiedni plik?
        """
        with open(SCIEZKA) as zly_plik:
            zawartosc = zly_plik.read()
        self.assertEqual(zawartosc, BLEDNY_FORMAT)


class TestyLoadera(unittest.TestCase):
    """Testy klasy 'statki.pamiec.Loader'."""

    def testuj_loader__ladowanie_nieistniejacego_pliku(self):
        """
        Czy próba załadowania nieistniejącego pliku zwraca odpowiedni błąd?
        """
        Loader.SCIEZKA = "testy/data.json"
        with self.assertRaises(FileNotFoundError):
            Loader.zaladuj_dane()

    def testuj_loader__ladowanie_pliku_o_blednym_formacie(self):
        """
        Czy próba załadowania pliku o błędnym formacie zwraca odpowiedni błąd?
        """
        Loader.SCIEZKA = SCIEZKA
        with self.assertRaises(ValueError):
            Loader.zaladuj_dane()


class TestyParsera(unittest.TestCase):
    """Testy klasy 'statki.pamiec.Parser'."""

    def setUp(self):
        self.prawidlowe_rangi = [Ranga(
            dane["nazwa"],
            dane["symbol"],
            range(dane["zakres"][0], dane["zakres"][1]),
            dane["sila_ognia"],
            dane["nazwy_statkow"],
            LICZEBNIKI[:],
            dane["liczba_mnoga"],
            dane["biernik"],
        ) for dane in DANE_RANG]

    def tearDown(self):
        # Parser.DANE = None
        pass

    def testuj_parser__rangi(self):
        """
        Czy prawidłowo podane dane są parsowane w prawidłowe rangi?
        """

        Parser.DANE = {
            "rangi": DANE_RANG,
            "liczebniki": LICZEBNIKI
        }

        sparsowane_rangi = Parser.podaj_rangi()

        for sparsowana_ranga, prawidlowa_ranga in zip(list(sparsowane_rangi),
                                                      self.prawidlowe_rangi):
            with self.subTest(sparsowana_ranga=sparsowana_ranga):
                self.assertEqual(sparsowana_ranga, prawidlowa_ranga)
