"""

    statki.pamiec
    ~~~~~~~~~~~~~

    Zapis i odczyt danych z pamięci zewnętrznej.

"""

import codecs
import json


from statki.ranga import Ranga, Rangi


class Parser:
    """Parsuje dane z 'dane/dane.json'."""

    SCIEZKA_DANE = "dane/dane.json"

    @classmethod
    def podaj_rangi(cls):
        """Podaje sparsowaną listę obiektów klasy 'statki.ranga.Ranga.'"""

        lista_rang = []
        try:
            with codecs.open(cls.SCIEZKA_DANE, encoding='utf-8') as plik:
                dane = json.load(plik)
                dane_dla_rang = dane["rangi"]  # słownik
                liczebniki = dane["liczebniki"]
        except FileNotFoundError:
            print("Nieudane parsowanie danych dla rang. Brak pliku '{}'".format(cls.SCIEZKA_DANE))
            raise
        except ValueError:
            print("Nieudane parsowanie danych dla rang. Plik '{}' w nieprawidłowym formacie".format(cls.SCIEZKA_DANE))
            raise

        for ranga_dane in dane_dla_rang:
            lista_rang.append(Ranga(
                ranga_dane["nazwa"],
                ranga_dane["symbol"],
                range(ranga_dane["zakres"][0], ranga_dane["zakres"][1]),
                ranga_dane["sila_ognia"],
                ranga_dane["nazwy_statkow"],
                liczebniki,
                ranga_dane["liczba_mnoga"],
                ranga_dane["biernik"]
            ))
            print("\nRanga: {}. Sparsowano nazw: [{}]".format(ranga_dane["nazwa"], len(ranga_dane["nazwy_statkow"])))  # test

        return Rangi._make(lista_rang)
