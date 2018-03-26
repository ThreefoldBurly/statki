"""

    testy.test_plansza
    ~~~~~~~~~~~~~~~~~~

    Testy jednostkowe modułu 'statki.plansza'.

"""

import unittest

from statki.plansza import Plansza, Pole, Salwa, Statek


class TestyPlanszy(unittest.TestCase):
    """Testy klasy 'statki.plansza.Plansza'."""
    pass


class TestyPola(unittest.TestCase):
    """Testy klasy 'statki.plansza.Pole'."""

    def setUp(self):
        """Stwórz pole o współrzędnych (10, 10)."""
        self.pole = Pole(id(self), 10, 10)

    def testuj_domyslny_znacznik_pola(self):
        """
        Czy pole inicjalizowane bez podania znacznika otrzymuje jego właściwą wartość domyślną?
        """
        self.assertEqual(self.pole.znacznik, Pole.ZNACZNIKI.pusty)

    def testuj_zamiane_na_string_w_nawiasach(self):
        """Czy pole jest zamieniane na stringa w odpowiednim formacie?"""
        self.assertEqual(self.pole.str_w_nawiasach(), "(J10)")


class TestySalwy(unittest.TestCase):
    """Testy klasy 'statki.plansza.Salwa'."""
    pass


class TestyStatku(unittest.TestCase):
    """Testy klasy 'statki.plansza.Statek'."""
    pass


# def main():
#     """Uruchom testy."""
#     unittest.main()
