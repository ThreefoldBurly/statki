"""

    testy.test_plansza
    ~~~~~~~~~~~~~~~~~~

    Testy jednostkowe modułu 'statki.plansza'.

"""

import unittest

from statki.plansza import Plansza, Pole, Salwa, Statek

# TODO: testy funkcji tego modułu


def podaj_pusta_plansze(kolumny, rzedy):
    """Podaj pustą planszę."""
    plansza = Plansza(kolumny, rzedy)
    for rzad in plansza.pola:
        for pole in rzad:
            pole.znacznik = Pole.ZNACZNIKI.pusty
    plansza.statki, plansza.niezatopione, plansza.zatopione = [], [], []
    plansza.ilosc_pol_statkow = 0
    return plansza


def stworz_statek(plansza, *wspolrzedne):
    """Stwórz na podanej planszy statek z pól o podanych współrzędnych."""
    if len(wspolrzedne) not in range(plansza.MIN_ROZMIAR_STATKU, plansza.MAX_ROZMIAR_STATKU + 1):
        raise ValueError("Błąd tworzenia statku. Podano złą ilość współrzędnych pól.")

    pola_statku = [plansza.podaj_pole(kolumna, rzad) for kolumna, rzad in wspolrzedne]
    for pole in pola_statku:
        if pole is None:
            raise ValueError("Błąd tworzenia statku. Podano współrzędne pól spoza planszy.")
        pole.znacznik = Pole.ZNACZNIKI.statek

    return Statek.fabryka(pola_statku)


def stworz_salwe(plansza, zrodlo, *wspolrzedne):
    """Stwórz na podanej planszy salwę z pól o podanych współrzędnych."""
    if len(wspolrzedne) not in range(Salwa.MIN_ROZMIAR, Salwa.MAX_ROZMIAR + 1):
        raise ValueError("Błąd tworzenia salwy. Podano złą ilość współrzędnych pól.")
    pola_salwy = [plansza.podaj_pole(kolumna, rzad) for kolumna, rzad in wspolrzedne]
    plansza.odkryj_pola([pole for pole in pola_salwy if pole is not None])
    return Salwa(zrodlo, pola_salwy)


class TestyPlanszy(unittest.TestCase):
    """Testy klasy 'statki.plansza.Plansza'."""

    def setUp(self):
        """Przygotuj pustą planszę do testów."""
        self.plansza = podaj_pusta_plansze(26, 30)

    def testuj_plansze__nieprawidlowe_wymiary(self):
        """
        Czy wymiary planszy są prawidłowo sprawdzane?"
        """
        nieprawidlowe_wymiary = [(7, 7), (4, 13), (3, 35), (12, 34), (27, 31)]
        for kolumny, rzedy in nieprawidlowe_wymiary:
            with self.subTest(wymiary="{}x{}".format(kolumny, rzedy)):
                with self.assertRaises(ValueError):
                    self.plansza.sprawdz_wymiary(kolumny, rzedy)

    def testuj_plansze__pola_prawidlowego_statku(self):
        """
        Czy pola prawidłowego statku są prawidłowo sprawdzane (czy każde kolejne pole statku jest ortogonalnym sąsiadem któregoś z poprzednich)? Test 4 różnych statków.
        """
        pancernik_prawidlowy = stworz_statek(
            self.plansza,
            (1, 5), (2, 5), (3, 5), (4, 5), (4, 4), (4, 3), (5, 3), (5, 4), (6, 4), (6, 5),
            (6, 6), (5, 6), (5, 5), (5, 7), (4, 7), (3, 7), (2, 7), (2, 6), (1, 6), (1, 7)
        )
        niszczyciel_prawidlowy = stworz_statek(
            self.plansza,
            (10, 13), (11, 13), (12, 13), (12, 14), (12, 15), (11, 15), (10, 15), (10, 14),
            (11, 14), (9, 14), (9, 15)
        )
        patrolowiec_prawidlowy_dwapola = stworz_statek(self.plansza, (5, 12), (5, 13))
        patrolowiec_prawidlowy_trzypola = stworz_statek(self.plansza, (8, 10), (9, 10), (9, 9))
        kuter = stworz_statek(self.plansza, (2, 11))

        for statek in [pancernik_prawidlowy, niszczyciel_prawidlowy,
                       patrolowiec_prawidlowy_dwapola, patrolowiec_prawidlowy_trzypola, kuter]:
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
        pancernik_nieprawidlowy_koniec = stworz_statek(
            self.plansza,
            (1, 5), (2, 5), (3, 5), (4, 5), (4, 4), (4, 3), (5, 3), (5, 4), (6, 4), (6, 5),
            (6, 6), (5, 6), (5, 5), (5, 7), (4, 7), (3, 7), (2, 7), (2, 6), (1, 6),
            (1, 8)  # nieprawidłowe pole
        )
        pancernik_nieprawidlowy_srodek = stworz_statek(
            self.plansza,
            (16, 5), (17, 5), (18, 5), (19, 5), (19, 4), (19, 3), (20, 3), (20, 4), (21, 4),
            (21, 5), (21, 6), (20, 6), (20, 5), (19, 7),  # nieprawidłowe pole
            (18, 7), (17, 7), (17, 6), (16, 6), (16, 7), (16, 8)
        )
        pancernik_nieprawidlowy_poczatek = stworz_statek(
            self.plansza,
            (16, 13),  # nieprawidłowe pole
            (17, 14), (18, 14), (19, 14), (19, 13), (19, 12), (18, 12), (18, 11), (18, 10),
            (19, 10), (20, 10), (20, 11), (19, 11), (20, 12), (21, 12), (21, 13), (21, 14),
            (20, 14), (20, 13), (20, 15)
        )
        patrolowiec_nieprawidlowy_dwapola = stworz_statek(self.plansza, (5, 12), (4, 13))
        patrolowiec_nieprawidlowy_trzypola = stworz_statek(
            self.plansza,
            (8, 10), (9, 10), (11, 8)  # nieprawidłowe pole
        )
        korweta_nieprawidlowa_powtorzenie = stworz_statek(
            self.plansza,
            (10, 5), (11, 5), (11, 5), (11, 4), (12, 4)
        )
        niszczyciel_nieprawidlowy = stworz_statek(
            self.plansza,
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

    def testuj_pole__domyslny_znacznik(self):
        """
        Czy pole inicjalizowane bez podania znacznika otrzymuje jego właściwą wartość domyślną?
        """
        self.assertEqual(self.pole.znacznik, Pole.ZNACZNIKI.pusty)

    def testuj_pole__konwersja_do_str_w_nawiasach(self):
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
        self.salwa = stworz_salwe(
            self.plansza_gracza,
            self.plansza_przeciwnika.statki[0].polozenie,
            (8, 10), (9, 10), (9, 9)
        )

    def testuj_salwe__ekwiwalencja(self):
        """
        Czy dwie salwy mające to samo źródło i składające się z równych sobie pól są równe?
        """
        druga = stworz_salwe(
            self.plansza_gracza,
            self.plansza_przeciwnika.statki[0].polozenie,
            (8, 10), (9, 10), (9, 9)
        )
        self.assertEqual(self.salwa, druga)

    def testuj_salwe__roznica(self):
        """
        Czy dwie salwy mające różne źródła i składające się z różnych pól są różne?
        """
        druga_inne_zrodlo = stworz_salwe(
            self.plansza_gracza,
            self.plansza_przeciwnika.statki[1].polozenie,
            (8, 10), (9, 10), (9, 9)
        )
        druga_inne_wspolrzedne = stworz_salwe(
            self.plansza_gracza,
            self.plansza_przeciwnika.statki[0].polozenie,
            (2, 3), (3, 3), (3, 4)
        )
        druga_inne_wspolrzedne_niewypal = stworz_salwe(
            self.plansza_gracza,
            self.plansza_przeciwnika.statki[0].polozenie,
            (1, 1), (1, 2), (0, 2)
        )
        for druga in [druga_inne_zrodlo, druga_inne_wspolrzedne, druga_inne_wspolrzedne_niewypal]:
            with self.subTest(salwa=str(druga)):
                self.assertNotEqual(self.salwa, druga)

    def testuj_salwe__konwersja_do_str_jedno_pole(self):
        """
        Czy salwa jest zamieniana na stringa w odpowiednim formacie? Test salwy składającej się z 1 pola.
        """
        salwa = stworz_salwe(
            self.plansza_gracza,
            self.plansza_przeciwnika.statki[0].polozenie,
            (8, 10)
        )
        self.assertEqual(str(salwa), "(H10)")

    def testuj_salwe__konwersja_do_str_dwa_pola(self):
        """
        Czy salwa jest zamieniana na stringa w odpowiednim formacie? Test salwy składającej się z 2 póla.
        """
        salwa = stworz_salwe(
            self.plansza_gracza,
            self.plansza_przeciwnika.statki[0].polozenie,
            (8, 10), (9, 10)
        )
        self.assertEqual(str(salwa), "(H10) i (I10)")

    def testuj_salwe__konwersja_do_str_trzy_pola(self):
        """
        Czy salwa jest zamieniana na stringa w odpowiednim formacie? Test salwy składającej się z 3 pól.
        """
        self.assertEqual(str(self.salwa), "(H10), (I9) i (I10)" or "(I9), (H10) i (I10)")

    def testuj_salwe__rozmiar(self):
        """
        Czy próba stworzenia salwy o nieprawidłowym rozmiarze zwraca odpowiedni błąd?
        """
        with self.assertRaises(ValueError):
            stworz_salwe(
                self.plansza_gracza,
                self.plansza_przeciwnika.statki[0].polozenie,
                (8, 10), (9, 10), (9, 9), (10, 10), (9, 11)
            )

    def testuj_salwe__nieprawidlowe_pola(self):
        """
        Czy próba stworzenia salwy z pól o nieprawidłowym położeniu zwraca odpowiedni błąd?
        """
        zestaw_wspolrzednych = [
            ((8, 10), (9, 9)),
            ((8, 9), (9, 10)),
            ((8, 10), (10, 8)),
            ((8, 10), (9, 9), (10, 8)),
            ((8, 8), (9, 9), (10, 10)),
            ((8, 10), (9, 9), (10, 8)),
            ((9, 9), (9, 10), (9, 12))
        ]
        for wspolrzedne in zestaw_wspolrzednych:
            with self.subTest(wspolrzedne=wspolrzedne):
                with self.assertRaises(ValueError):
                    stworz_salwe(
                        self.plansza_gracza,
                        self.plansza_przeciwnika.statki[0].polozenie,
                        *wspolrzedne
                    )


class TestyStatku(unittest.TestCase):
    """Testy klasy 'statki.plansza.Statek'."""
    pass


# def main():
#     """Uruchom testy."""
#     unittest.main()
