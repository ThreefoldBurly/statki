#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Moduł współdzielony, z którego pozostałe importują stałe i funkcje.
"""

import codecs
from random import gauss


ZNACZNIKI = {
    "pusty": "0",
    "pudlo": "x",
    "trafiony": "T",
    "zatopiony": "Z",
    "statek": "&",
    "obwiednia": "."
}
KIERUNKI = ["prawo", "lewo", "gora", "dol"]


def sparsuj_rangi_statkow():
    """
    Parsuje z pliku tekstowego 'rangi-statkow.sti słownik rozmiarów i rang statków oraz listę nazw rang
    """
    rangi_statkow = []
    with codecs.open('rangi-statkow.sti', encoding='utf-8') as plik:
        for linia in plik:
            if "#" in linia:
                continue
            linia = linia.strip(' \n')
            spars_linia = linia.split(':::')
            rozmiar_statku = int(spars_linia[0])
            ranga_statku = spars_linia[1]
            rangi_statkow.append([rozmiar_statku, ranga_statku])

    rangi_statkow = dict(rangi_statkow)

    assert len(rangi_statkow) > 0, "Nieudane parsowanie rang statków. Brak pliku 'rangi-statkow.sti' lub plik nie zawiera danych w prawidłowym formacie"

    nazwy_rang = []  # TODO: to trzeba zamienić na wyciągnięcie wartości ze słownika i zostawienie unikatowych funkcją set()
    akt_nazwa_rangi = ""
    for k, nazwa_rangi in rangi_statkow.items():
        if nazwa_rangi != akt_nazwa_rangi:
            nazwy_rang.append(nazwa_rangi)
        akt_nazwa_rangi = nazwa_rangi
    return (rangi_statkow, nazwy_rang)


RANGI_STATKOW, NAZWY_RANG = sparsuj_rangi_statkow()  # słownik w formacie {rozmiar: ranga}, lista [kuter, patrolowiec, korweta, fregata, niszczyciel, krążownik, pancernik] (niekoniecznie w tej kolejności!)


def sparsuj_nazwy_statkow():
    """Parsuje z pliku tekstowego 'nazwy-statkow.sti' listę nazw dla każdej rangi statku (całość jako słownik)"""
    nazwy_statkow = {}

    def parsuj_wg_rangi(linie, ranga):  # funkcja pomocnicza dla bloku poniżej
        lista_nazw = []
        for linia in linie:
            if ranga in linia:
                linia = linia.rstrip('\n')
                lista_nazw.append(linia.split(':::')[0])
        return lista_nazw

    linie = []
    with codecs.open('nazwy-statkow.sti', encoding='utf-8') as plik:
        for linia in plik:
            linie.append(linia)

    for ranga in NAZWY_RANG:
        lista_nazw = parsuj_wg_rangi(linie, ranga)
        print("\nRanga: {}. Dodano nazw: [{}]".format(ranga, len(lista_nazw)))  # test
        nazwy_statkow[ranga] = lista_nazw

    def czy_nazwy_OK():  # czy do wszystkich rang statków przypisano jakieś nazwy?
        czy_OK = True
        for ranga in nazwy_statkow:
            if len(nazwy_statkow[ranga]) == 0:
                czy_OK = False
        return czy_OK

    assert czy_nazwy_OK(), "Nieudane parsowanie nazw statków. Brak pliku 'nazwy-statkow.sti' lub plik nie zawiera danych w prawidłowym formacie"

    return nazwy_statkow


NAZWY_STATKOW = sparsuj_nazwy_statkow()  # słownik w formacie {ranga: [lista nazw]}


def sklonuj_nazwy_statkow():
    """
    Klonuje słownik NAZWY_STATKOW, wykonując kopię każdej składowej listy
    """
    nazwy = {}
    for klucz in NAZWY_STATKOW:
        nazwy[klucz] = NAZWY_STATKOW[klucz][:]
    return nazwy


def podaj_int_z_rozkladu_Gaussa(mediana, odch_st, minimum, maximum, prz_mediany=0):
    """
    Podaje losowy int wg rozkładu Gaussa we wskazanym przedziale oraz ze wskazanym przesunięciem mediany. Liczby spoza zadanego przedziału zwracane przez random.gauss() są odbijane proporcjonalnie do wewnątrz przedziału. PRZYKŁAD: dla przedziału <1, 20>, jeśli random.gauss() zwraca -2, to zwróconą liczbą będzie 3, jeśli -5, to 6 jeśli random.gauss() zwraca 22, to zwróconą liczbą, będzie 19, jeśli 27, to 14.
    """
    i = int(round(gauss(mediana + prz_mediany, odch_st)))
    if i < minimum:
        i = minimum - i
        if i > maximum:  # odbicie do wewnątrz przedziału jest jednokrotne (jeśli odbite minimum- miałoby wyjść poza zadany przedział, jest przycinane do maximum bez odbicia)
            i = maximum
    if i > maximum:
        i = maximum - (i - maximum) + 1
        if i < minimum:  # odbicie do wewnątrz przedziału jest jednokrotne (jeśli odbite maximum+ miałoby wyjść poza zadany przedział, jest przycinane do minimum bez odbicia)
            i = minimum
    return i
