#!/usr/bin/env python3

"""
Plansza gry wraz z jej podstawowymi elementami.
"""

import codecs
from random import randint, choice, gauss


class Parser:
    """Parsuje nazwy statków z 'dane/nazwy.sti'."""

    @staticmethod
    def sparsuj_nazwy(rangi):
        """Parsuje z pliku tekstowego 'dane/nazwy.sti' listę nazw dla każdej rangi statku (całość jako słownik)"""
        nazwy = {}

        def parsuj_wg_rangi(linie, ranga):  # funkcja pomocnicza dla bloku poniżej
            lista_nazw = []
            for linia in linie:
                if ranga in linia:
                    linia = linia.rstrip('\n')
                    lista_nazw.append(linia.split(':::')[0])
            return lista_nazw

        linie = []
        with codecs.open('dane/nazwy.sti', encoding='utf-8') as plik:
            for linia in plik:
                linie.append(linia)

        for ranga in rangi:
            lista_nazw = parsuj_wg_rangi(linie, ranga)
            print("\nRanga: {}. Dodano nazw: [{}]".format(ranga, len(lista_nazw)))  # test
            nazwy[ranga] = lista_nazw

        def czy_nazwy_OK():  # czy do wszystkich rang statków przypisano jakieś nazwy?
            czy_OK = True
            for ranga in nazwy:
                if len(nazwy[ranga]) == 0:
                    czy_OK = False
            return czy_OK

        assert czy_nazwy_OK(), "Nieudane parsowanie nazw statków. Brak pliku 'dane/nazwy.sti' lub plik nie zawiera danych w prawidłowym formacie"

        return nazwy

    @staticmethod
    def sklonuj_nazwy(nazwy_wg_rangi):
        """Klonuje słownik nazw wg rangi, wykonując kopię każdej składowej listy."""
        nazwy = {}
        for klucz in nazwy_wg_rangi:
            nazwy[klucz] = nazwy_wg_rangi[klucz][:]
        return nazwy
