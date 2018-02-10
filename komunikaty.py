#!/usr/bin/env python3

"""
Komunikaty tekstowe w grze.
"""

from plansza import Statek

SLOWNIK_ODMIAN = {
    "kolumna": ["kolumna", "kolumny", "kolumn"],
    "rząd": ["rząd", "rzędy", "rzędów"],
    "pole": ["pole", "pola", "pól"],
    "statek": ["statek", "statki", "statków"],
    "kuter": ["kuter", "kutry", "kutrów"],
    "patrolowiec": ["patrolowiec", "patrolowce", "patrolowców"],
    "korweta": ["korweta", "korwety", "korwet"],
    "fregata": ["fregata", "fregaty", "fregat"],
    "niszczyciel": ["niszczyciel", "niszczyciele", "niszczycieli"],
    "krążownik": ["krążownik", "krążowniki", "krążowników"],
    "pancernik": ["pancernik", "pancerniki", "pancerników"]
}


def do_indeksu(liczba):
    """Zamienia liczbę na indeks wartości w słowniku odmian."""
    if liczba == 1:
        return 0
    elif liczba in range(2, 5):
        return 1
    elif liczba in range(5, 22):
        return 2
    elif int(str(liczba)[-1]) in range(2, 5):
        return 1
    else:
        return 2


class Komunikator:
    """Obsługuje pole tekstowe paska stanu (TODO: oraz tooltipy)."""

    def __init__(self, pasek_stanu, plansza_gracza, plansza_przeciwnika):
        self.pasek_stanu = pasek_stanu
        self.plansza_g = plansza_gracza
        self.plansza_p = plansza_przeciwnika

    def o_rozpoczeciu_gry(self):
        """Wyświetla komunikat o rozpoczęciu gry."""
        kolumny, rzedy = self.plansza_g.gracz.plansza.kolumny, self.plansza_g.gracz.plansza.rzedy
        rozmiar = self.plansza_g.gracz.plansza.rozmiar
        ilosc_statkow = len(self.plansza_g.gracz.plansza.statki)
        ilosc_pol_statkow = self.plansza_g.gracz.plansza.podaj_ilosc_nietrafionych_pol()
        wg_rang = self.plansza_g.gracz.plansza.podaj_ilosc_niezatopionych_wg_rang()  # słownik

        komunikat = "Gra na planszy o rozmiarze: " + str(kolumny)
        komunikat += " " + SLOWNIK_ODMIAN["kolumna"][do_indeksu(kolumny)]
        komunikat += " x " + str(rzedy) + " "
        komunikat += SLOWNIK_ODMIAN["rząd"][do_indeksu(rzedy)]
        komunikat += " (" + str(rozmiar) + " " + SLOWNIK_ODMIAN["pole"][do_indeksu(rozmiar)] + "). "
        komunikat += "Umieszczono " + str(ilosc_statkow) + " "
        komunikat += SLOWNIK_ODMIAN["statek"][do_indeksu(ilosc_statkow)]
        komunikat += " zajmujących " + str(ilosc_pol_statkow) + " "
        komunikat += SLOWNIK_ODMIAN["pole"][do_indeksu(ilosc_pol_statkow)] + ". W tym: "
        for ranga in Statek.RANGI:
            komunikat += str(wg_rang[ranga]) + " " + SLOWNIK_ODMIAN[ranga][do_indeksu(wg_rang[ranga])] + ", "
        komunikat = komunikat[:-2]
        komunikat += ". Zaczynamy!"

        self.pasek_stanu.tekst.readonly_insert("1.0", komunikat)
