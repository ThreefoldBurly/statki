"""

    statki.pamiec
    ~~~~~~~~~~~~~

    Zapis i odczyt danych z pamięci zewnętrznej.

"""

import json

from statki.ranga import Ranga, Rangi


class Loader:
    """Ładuj dane zapisane w plikach."""
    SCIEZKA = "dane/dane.json"

    @classmethod
    def zaladuj_dane(cls):
        """Ładuj dane z pliku JSON."""
        try:
            with open(cls.SCIEZKA, encoding='utf-8') as plik:
                dane = json.load(plik)
        except FileNotFoundError:
            print("Nieudane parsowanie danych dla rang. Brak pliku '{}'".format(cls.SCIEZKA))
            raise
        except ValueError:
            print("Nieudane parsowanie danych dla rang.",
                  "Plik '{}' w nieprawidłowym formacie".format(cls.SCIEZKA))
            raise

        return dane


class Parser:
    """Parsuj dane zapisane w plikach."""
    # TODO: testy prawidłowości parsowanych danych
    DANE = Loader.zaladuj_dane()
    DANE_PLANSZY = DANE["plansza"]

    @classmethod
    def podaj_rangi(cls):
        """Podaj sparsowane obiekty klasy 'statki.ranga.Ranga'."""
        dane_rang = cls.DANE["rangi"]  # słownik
        liczebniki = cls.DANE["liczebniki"]

        lista_rang = []
        for ranga_dane in dane_rang:
            lista_rang.append(Ranga(
                ranga_dane["nazwa"],
                ranga_dane["symbol"],
                range(ranga_dane["zakres"][0], ranga_dane["zakres"][1]),
                ranga_dane["sila_ognia"],
                ranga_dane["nazwy_statkow"],
                liczebniki[:],
                ranga_dane["liczba_mnoga"],
                ranga_dane["biernik"]
            ))
            print("\nRanga: {}. Sparsowano nazw: [{}]".format(
                ranga_dane["nazwa"],
                len(ranga_dane["nazwy_statkow"])
            ))  # test

        return Rangi._make(lista_rang)

    @classmethod
    def podaj_minmax_kolumny(cls):
        """Podaj sparsowane minimalną i maksymalną liczbę kolumn planszy."""
        min_kolumny = cls.DANE_PLANSZY["kolumny"][0]  # 8
        max_kolumny = cls.DANE_PLANSZY["kolumny"][1]  # 26
        return min_kolumny, max_kolumny

    @classmethod
    def podaj_minmax_rzedy(cls):
        """Podaj sparsowane minimalną i maksymalną liczbę rzędów planszy."""
        min_rzedy = cls.DANE_PLANSZY["rzedy"][0]  # 8
        max_rzedy = cls.DANE_PLANSZY["rzedy"][1]  # 30
        return min_rzedy, max_rzedy

    @classmethod
    def podaj_minmax_rozmiar_statku(cls):
        """Podaj sparsowane minimalny i maksymalny rozmiar statku."""
        min_rozmiar = cls.DANE_PLANSZY["rozmiar_statku"][0]  # 1
        max_rozmiar = cls.DANE_PLANSZY["rozmiar_statku"][1]  # 20
        return min_rozmiar, max_rozmiar

    @classmethod
    def podaj_parametry_wypelniania(cls):
        """Podaj sparsowane parametry wypełniania planszy statkami."""
        zapelnienie = cls.DANE_PLANSZY["wypelnianie"][0]  # od 5 do 45
        odch_st = cls.DANE_PLANSZY["wypelnianie"][1]  # od 8.0 do 12.0
        prz_mediany = cls.DANE_PLANSZY["wypelnianie"][2]  # od -20 do 5
        return zapelnienie, odch_st, prz_mediany
