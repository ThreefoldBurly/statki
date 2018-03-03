"""

    statki.pamiec
    ~~~~~~~~~~~~~

    Zapis i odczyt danych z pamięci zewnętrznej.

"""

import codecs


class Parser:
    """Parsuje nazwy statków z 'dane/nazwy.txt'."""

    SCIEZKA_NAZW = "dane/nazwy.txt"

    @classmethod
    def podaj_nazwy_statkow(cls, nazwa_rangi):
        """Podaje sparsowaną listę nazw statków dla danej rangi."""
        nazwy = []
        try:
            with codecs.open(cls.SCIEZKA_NAZW, encoding='utf-8') as plik:
                for linia in [linia.rstrip("\n") for linia in plik if nazwa_rangi in linia]:
                    nazwy.append(linia.split(':::')[0])
        except FileNotFoundError:
            print("Nieudane parsowanie nazw statków. Brak pliku '{}'".format(cls.SCIEZKA_NAZW))
            raise

        assert len(nazwy) > 0, "Nieudane parsowanie nazw statków. Plik '{}' nie zawiera danych w prawidłowym formacie".format(cls.SCIEZKA_NAZW)

        print("\nRanga: {}. Dodano nazw: [{}]".format(nazwa_rangi, len(nazwy)))  # test

        return nazwy
