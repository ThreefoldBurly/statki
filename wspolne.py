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
    """Podaje losowy int wg rozkładu Gaussa we wskazanym przedziale oraz ze wskazanym przesunięciem mediany"""
    i = int(round(gauss(mediana + prz_mediany, odch_st)))
    if i < minimum:
        i = minimum
    if i > maximum:
        i = maximum
    return i

# test
# slownik = sparsujRangiStatkow()
# for klucz in slownik:
#     print "%s [%d]" % (slownik[klucz], klucz)
