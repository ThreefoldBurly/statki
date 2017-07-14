#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Moduł współdzielony, z którego pozostałe importują stałe i funkcje.
"""

import codecs
from random import gauss


ZNACZNIK_PUSTY = "0"
ZNACZNIK_PUDLO = "x"
ZNACZNIK_TRAFIONY = "T"
ZNACZNIK_ZATOPIONY = "Z"
ZNACZNIK_STATEK = "&"
ZNACZNIK_OBWIEDNIA = "."
KIERUNKI = ["prawo", "lewo", "gora", "dol"]


def sparsujRangiStatkow():
    """
    Parsuje z pliku tekstowego 'rangi-statkow.sti słownik rozmiarów i rang statków'
    """
    rangi_statkow = []
    with codecs.open('rangi-statkow.sti', encoding='utf-8') as plik:
        for linia in plik:
            if u"#" in linia:
                continue
            linia = linia.strip(u' \n')
            spars_linia = linia.split(u':::')
            rozmiar_statku = int(spars_linia[0])
            ranga_statku = spars_linia[1]
            rangi_statkow.append([rozmiar_statku, ranga_statku])

    rangi_statkow = dict(rangi_statkow)

    assert len(rangi_statkow) > 0, u"Nieudane parsowanie rang statków. Brak pliku 'rangi-statkow.sti' lub plik nie zawiera danych w prawidłowym formacie"

    return rangi_statkow


RANGI_STATKOW = sparsujRangiStatkow()  # słownik


def podajIntZRozkladuGaussa(mediana, odch_st, minimum, maximum, prz_mediany=0):
    """
    Podaje losowy int wg rozkładu Gaussa we wskazanym przedziale oraz ze wskazanym przesunięciem mediany. Liczby spoza zadanego przedziału zwracane przez random.gauss() są odbijane proporcjonalnie do wewnątrz przedziału. PRZYKŁAD: dla przedziału <1, 20>, jeśli random.gauss() zwraca -2, to zwróconą liczbą będzie 3, jeśli -5, to 6 jeśli random.gauss() zwraca 22, to zwróconą liczbą, będzie 19, jeśli 27, to 14.
    """
    i = int(round(gauss(mediana + prz_mediany, odch_st)))
    if i < minimum:
        i = minimum - i
        if i > maximum:  # odbicie do wewnątrz przedziału jest jednokrotne (jeśli odbite minimum-, miałoby wyjść poza zadany przedział, jest przycinane do maximum bez odbicia)
            i = maximum
    if i > maximum:
        i = maximum - (i - maximum) + 1
        if i < minimum:  # odbicie do wewnątrz przedziału jest jednokrotne (jeśli odbite maximum+, miałoby wyjść poza zadany przedział, jest przycinane do minimum bez odbicia)
            i = minimum
    return i
