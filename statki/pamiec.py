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
        return (cls.DANE["minmax"][0], cls.DANE["minmax"][1])

    @classmethod
    def podaj_parametry_wypelniania(cls):
        """Podaje sparsowane parametry wypełniania planszy statkami."""
        return (cls.DANE["wypelnianie"][0], cls.DANE["wypelnianie"][1], cls.DANE["wypelnianie"][2])
