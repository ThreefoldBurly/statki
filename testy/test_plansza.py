"""

    testy.test_plansza
    ~~~~~~~~~~~~~~~~~~

    Testy jednostkowe modułu 'statki.plansza'.

"""

import unittest

from statki.plansza import Plansza, Pole


class TestyPlanszy(unittest.TestCase):
    """Testy klasy 'statki.plansza.Plansza'."""

    def setUp(self):
        """Przygotuj pustą planszę do testów."""
        self.plansza = Plansza(26, 30)
        for rzad in self.plansza.pola:
            for pole in rzad:
                pole.znacznik = Pole.ZNACZNIKI.pusty
        self.plansza.statki, self.plansza.niezatopione, self.plansza.zatopione = [], [], []
        self.plansza.ilosc_pol_statkow = 0

    def tearDown(self):
        """Usuń przygotowaną wcześniej planszę."""
        del self.plansza

    def testuj_plansze__pola_prawidlowego_statku(self):
        """
        Czy pola prawidłowego statku są prawidłowo sprawdzane (czy każde kolejne pole statku jest ortogonalnym sąsiadem któregoś z poprzednich)? Test 4 różnych statków.
        """
        pancernik_prawidlowy = self.plansza.stworz_statek(
            (1, 5), (2, 5), (3, 5), (4, 5), (4, 4), (4, 3), (5, 3), (5, 4), (6, 4), (6, 5),
            (6, 6), (5, 6), (5, 5), (5, 7), (4, 7), (3, 7), (2, 7), (2, 6), (1, 6), (1, 7)
        )
        niszczyciel_prawidlowy = self.plansza.stworz_statek(
            (10, 13), (11, 13), (12, 13), (12, 14), (12, 15), (11, 15), (10, 15), (10, 14),
            (11, 14), (9, 14), (9, 15)
        )
        patrolowiec_prawidlowy_dwapola = self.plansza.stworz_statek((5, 12), (5, 13))
        patrolowiec_prawidlowy_trzypola = self.plansza.stworz_statek((8, 10), (9, 10), (9, 9))
        kuter = self.plansza.stworz_statek((2, 11))

        for statek in [pancernik_prawidlowy, patrolowiec_prawidlowy_dwapola,
                       patrolowiec_prawidlowy_trzypola, kuter]:
            with self.subTest(statek=str(statek)):
                try:
                    self.plansza.sprawdz_pola_statku(statek)
                except ValueError:
                    self.fail("Metoda 'sprawdz_pola_statku()' zwróciła błąd, "
                              "którego nie powinna zwracać.")

    def testuj_plansze__pola_nieprawidlowego_statku(self):
        """
        Czy pola nieprawidłowego statku są prawidłowo sprawdzane (czy każde kolejne pole statku jest ortogonalnym sąsiadem któregoś z poprzednich)? Test 7 różnych statków.
        """
        pancernik_nieprawidlowy_koniec = self.plansza.stworz_statek(
            (1, 5), (2, 5), (3, 5), (4, 5), (4, 4), (4, 3), (5, 3), (5, 4), (6, 4), (6, 5),
            (6, 6), (5, 6), (5, 5), (5, 7), (4, 7), (3, 7), (2, 7), (2, 6), (1, 6),
            (1, 8)  # nieprawidłowe pole
        )
        pancernik_nieprawidlowy_srodek = self.plansza.stworz_statek(
            (16, 5), (17, 5), (18, 5), (19, 5), (19, 4), (19, 3), (20, 3), (20, 4), (21, 4),
            (21, 5), (21, 6), (20, 6), (20, 5), (19, 7),  # nieprawidłowe pole
            (18, 7), (17, 7), (17, 6), (16, 6), (16, 7), (16, 8)
        )
        pancernik_nieprawidlowy_poczatek = self.plansza.stworz_statek(
            (16, 13),  # nieprawidłowe pole
            (17, 14), (18, 14), (19, 14), (19, 13), (19, 12), (18, 12), (18, 11), (18, 10),
            (19, 10), (20, 10), (20, 11), (19, 11), (20, 12), (21, 12), (21, 13), (21, 14),
            (20, 14), (20, 13), (20, 15)
        )
        patrolowiec_nieprawidlowy_dwapola = self.plansza.stworz_statek((5, 12), (4, 13))
        patrolowiec_nieprawidlowy_trzypola = self.plansza.stworz_statek(
            (8, 10), (9, 10), (11, 8)  # nieprawidłowe pole
        )
        korweta_nieprawidlowa_powtorzenie = self.plansza.stworz_statek(
            (10, 5), (11, 5), (11, 5), (11, 4), (12, 4)
        )
        niszczyciel_nieprawidlowy = self.plansza.stworz_statek(
            (10, 13), (11, 13), (12, 13), (12, 14), (12, 15), (11, 15), (10, 15), (10, 14),
            (11, 14),
            (11, 17), (11, 18)  # nieprawidłowe pola
        )

        for statek in [pancernik_nieprawidlowy_koniec, pancernik_nieprawidlowy_srodek,
                       pancernik_nieprawidlowy_poczatek, patrolowiec_nieprawidlowy_dwapola,
                       patrolowiec_nieprawidlowy_trzypola, korweta_nieprawidlowa_powtorzenie,
                       niszczyciel_nieprawidlowy]:
            with self.subTest(statek=str(statek)):
                with self.assertRaises(ValueError):
                    self.plansza.sprawdz_pola_statku(statek)


class TestyPola(unittest.TestCase):
    """Testy klasy 'statki.plansza.Pole'."""

    def setUp(self):
        """Stwórz pole do testów."""
        self.pole = Pole(id(self), 10, 10)

    def tearDown(self):
        """Usuń stworzone wcześniej pole do testów."""
        del self.pole

    def testuj_pole__domyslny_znacznik(self):
        """
        Czy pole inicjalizowane bez podania znacznika otrzymuje jego właściwą wartość domyślną?
        """
        self.assertEqual(self.pole.znacznik, Pole.ZNACZNIKI.pusty)

    def testuj_pole__konwersja_do_stringu_w_nawiasach(self):
        """
        Czy pole jest zamieniane na stringa w odpowiednim formacie?
        """
        self.assertEqual(self.pole.str_w_nawiasach(), "(J10)")

    def testuj_pole__ekwiwalencja(self):
        """
        Czy dwa pola należące do tej samej planszy, mające te same współrzędne i te same znaczniki są równe?
        """
        drugie = Pole(id(self), 10, 10, Pole.ZNACZNIKI.pusty)
        self.assertEqual(self.pole, drugie)

    def testuj_pole__roznica(self):
        """
        Czy dwa pola należące do różnych plansz, mające różne współrzędne i różne znaczniki są różne?
        """
        drugie_inna_plansza = Pole(id(object()), 10, 10, Pole.ZNACZNIKI.pusty)
        drugie_inne_wspolrzedne = Pole(id(self), 13, 3, Pole.ZNACZNIKI.pusty)
        drugie_inny_znacznik = Pole(id(self), 10, 10, Pole.ZNACZNIKI.zatopiony)

        for drugie in [drugie_inna_plansza, drugie_inne_wspolrzedne,
                       drugie_inny_znacznik]:
            with self.subTest(pole=str(drugie)):
                self.assertNotEqual(self.pole, drugie)

    def testuj_pole__obsluga_wyjatkowosci_w_zbiorach(self):
        """
        Czy zbiór pól odsiewa duplikaty?
        """
        dziesiec_takich_samych_pol = [Pole(id(self), 10, 5, Pole.ZNACZNIKI.statek)
                                      for i in range(10)]
        self.assertEqual(1, len(set(dziesiec_takich_samych_pol)))


class TestySalwy(unittest.TestCase):
    """Testy klasy 'statki.plansza.Salwa'."""

    def setUp(self):
        """Stwórz salwę do testów."""
        self.plansza_gracza, self.plansza_przeciwnika = Plansza(26, 30), Plansza(26, 30)
        self.salwa = self.plansza_gracza.stworz_salwe(
            self.plansza_przeciwnika.statki[0].polozenie,
            (8, 10), (9, 10), (9, 9)
        )

    def tearDown(self):
        """Usuń stworzoną wcześniej salwę do testów."""
        del self.plansza_gracza
        del self.plansza_przeciwnika
        del self.salwa

    def testuj_salwe__ekwiwalencja(self):
        """
        Czy dwie salwy mające to samo źródło i składające się z równych sobie pól są równe?
        """
        druga = self.plansza_gracza.stworz_salwe(
            self.plansza_przeciwnika.statki[0].polozenie,
            (8, 10), (9, 10), (9, 9)
        )
        self.assertEqual(self.salwa, druga)

    def testuj_salwe__roznica(self):
        """
        Czy dwie salwy mające różne źródła i składające się z różnych pól są różne?
        """
        druga_inne_zrodlo = self.plansza_gracza.stworz_salwe(
            self.plansza_przeciwnika.statki[1].polozenie,
            (8, 10), (9, 10), (9, 9)
        )
        druga_inne_wspolrzedne = self.plansza_gracza.stworz_salwe(
            self.plansza_przeciwnika.statki[0].polozenie,
            (2, 3), (3, 3), (3, 4)
        )
        druga_inne_wspolrzedne_niewypal = self.plansza_gracza.stworz_salwe(
            self.plansza_przeciwnika.statki[0].polozenie,
            (1, 1), (1, 2), (0, 2)
        )
        for druga in [druga_inne_zrodlo, druga_inne_wspolrzedne, druga_inne_wspolrzedne_niewypal]:
            with self.subTest(salwa=str(druga)):
                self.assertNotEqual(self.salwa, druga)


class TestyStatku(unittest.TestCase):
    """Testy klasy 'statki.plansza.Statek'."""
    pass


# def main():
#     """Uruchom testy."""
#     unittest.main()
