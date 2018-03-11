"""

    statki.pamiec
    ~~~~~~~~~~~~~

    Zapis i odczyt danych z pamięci zewnętrznej.

"""

import codecs
import json


from statki.ranga import Ranga, Rangi


class Loader:
    """Ładuje dane zapisane w plikach."""
    SCIEZKA = "dane/dane.json"

    @classmethod
    def zaladuj_dane(cls):
        """Ładuje dane z pliku JSON."""
        try:
            with codecs.open(cls.SCIEZKA, encoding='utf-8') as plik:
                dane = json.load(plik)
        except FileNotFoundError:
            print("Nieudane parsowanie danych dla rang. Brak pliku '{}'".format(cls.SCIEZKA))
            raise
        except ValueError:
            print("Nieudane parsowanie danych dla rang. Plik '{}' w nieprawidłowym formacie".format(cls.SCIEZKA))
            raise

        return dane


class Parser:
    """Parsuje dane zapisane w plikach."""
    DANE = Loader.zaladuj_dane()

    @classmethod
    def podaj_rangi(cls):
        """Podaje sparsowane obiekty klasy 'statki.ranga.Ranga'."""
        dane_dla_rang = cls.DANE["rangi"]  # słownik
        liczebniki = cls.DANE["liczebniki"]

        lista_rang = []
        for ranga_dane in dane_dla_rang:
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
            print("\nRanga: {}. Sparsowano nazw: [{}]".format(ranga_dane["nazwa"], len(ranga_dane["nazwy_statkow"])))  # test

        return Rangi._make(lista_rang)

    @classmethod
    def podaj_minmax_rozmiar_statku(cls):
        """Podaje sparsowane minimalny i maksymalny rozmiar statku."""
        min_rozmiar, max_rozmiar = cls.DANE["minmax"][0], cls.DANE["minmax"][1]
        if min_rozmiar != 1:
            raise ValueError(
                "Błąd parsowania parametrów rozmiaru statków.",
                "Dopuszczalny minimalny rozmiar statku: 1. Otrzymany: {}".format(min_rozmiar)
            )
        if max_rozmiar != 20:
            raise ValueError(
                "Błąd parsowania parametrów rozmiaru statków.",
                "Dopuszczalny maksymalny rozmiar statku: 20. Otrzymany: {}".format(max_rozmiar)
            )
        return (min_rozmiar, max_rozmiar)

    @classmethod
    def podaj_parametry_wypelniania(cls):
        """Podaje sparsowane parametry wypełniania planszy statkami."""
        zapelnienie = cls.DANE["wypelnianie"][0]
        odch_st = cls.DANE["wypelnianie"][1]
        prz_mediany = cls.DANE["wypelnianie"][2]

        if zapelnienie not in range(5, 46):
            raise ValueError(
                "Błąd parsowania parametrów wypełniania planszy statkami.",
                "Dopuszczalne zapełnienie: (5-45). Otrzymane: {}".format(zapelnienie)
            )
        if not (8.0 <= odch_st <= 12.0):
            raise ValueError(
                "Błąd parsowania parametrów wypełniania planszy statkami.",
                "Dopuszczalne odchylenie standardowe: (8.0-12.0). Otrzymane: {}".format(odch_st)
            )
        if prz_mediany not in range(-20, 6):
            raise ValueError(
                "Błąd parsowania parametrów wypełniania planszy statkami.",
                "Dopuszczalne przesunięcie mediany: (-20-5). Otrzymane: {}".format(prz_mediany)
            )
        return (zapelnienie, odch_st, prz_mediany)
