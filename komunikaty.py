#!/usr/bin/env python3

"""
Komunikaty tekstowe w grze.
"""

import tkinter as tk

from plansza import Statek


class Komunikator:
    """Obsługuje pole tekstowe paska stanu (TODO: oraz tooltipy)."""

    ODMIANY = {
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
    GWIAZDKA = "✱"
    KOLORY = {
        "szare": "dim gray"
    }

    def __init__(self, tekst, czcionki, kolory_pola):
        self.tekst = tekst
        self.CZCIONKI = czcionki
        self.KOLORY.update(kolory_pola)
        self.ustaw_tagi()

    @staticmethod
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

    def ustaw_tagi(self):
        """Ustawia tagi pola tekstowego zapewniające odpowiednie formatowanie komunikatów."""
        self.tekst.tag_configure("wyszarzone", foreground=self.KOLORY["szare"])
        self.tekst.tag_configure("wyśrodkowane", justify=tk.CENTER)
        self.tekst.tag_configure("pogrubione", font=self.CZCIONKI["mała-pogrubiona"])
        self.tekst.tag_configure("trafione", background=self.KOLORY["trafione"])

    def o_rozpoczeciu_gry(self, plansza_gracza):
        """Wyświetla komunikat o rozpoczęciu gry."""
        kolumny, rzedy = plansza_gracza.kolumny, plansza_gracza.rzedy
        rozmiar = plansza_gracza.rozmiar
        ilosc_statkow = len(plansza_gracza.statki)
        ilosc_pol_statkow = plansza_gracza.podaj_ilosc_nietrafionych_pol()
        wg_rang = plansza_gracza.podaj_ilosc_niezatopionych_wg_rang()  # słownik

        self.tekst.ro_insert("1.0", "Gra na planszy o rozmiarze: ")
        self.tekst.ro_insert("end", str(kolumny), "pogrubione")
        self.tekst.ro_insert("end", " " + self.ODMIANY["kolumna"][self.do_indeksu(kolumny)] + " x ")
        self.tekst.ro_insert("end", str(rzedy), "pogrubione")
        komunikat = " " + self.ODMIANY["rząd"][self.do_indeksu(rzedy)]
        komunikat += " (" + str(rozmiar) + " " + self.ODMIANY["pole"][self.do_indeksu(rozmiar)] + "). "
        komunikat += "Umieszczono "
        self.tekst.ro_insert("end", komunikat)
        self.tekst.ro_insert("end", str(ilosc_statkow), "pogrubione")
        komunikat = " " + self.ODMIANY["statek"][self.do_indeksu(ilosc_statkow)]
        komunikat += " zajmujących " + str(ilosc_pol_statkow) + " "
        komunikat += self.ODMIANY["pole"][self.do_indeksu(ilosc_pol_statkow)] + ". W tym: "
        self.tekst.ro_insert("end", komunikat)
        for ranga in Statek.RANGI:
            self.tekst.ro_insert("end", str(wg_rang[ranga]), "pogrubione")
            komunikat = " " + self.ODMIANY[ranga][self.do_indeksu(wg_rang[ranga])]
            komunikat += " (" + Statek.SYMBOLE[ranga] + "), "
            self.tekst.ro_insert("end", komunikat)
        self.tekst.ro_delete("end-3c", "end")
        self.tekst.ro_insert("end", ". Zaczynamy!")

    def o_rundzie(self, gracz):
        """Wyświetla komunikat o nowej rundzie."""
        bazowa_dl_separatora = 120
        korekta = round((gracz.plansza.kolumny - 8) * 13)
        dl_separatora = bazowa_dl_separatora + korekta
        komunikat = gracz.podaj_info_o_rundzie().title()
        komunikat = "  ".join(["  ", self.GWIAZDKA, komunikat, self.GWIAZDKA, "   "])
        komunikat = komunikat.center(dl_separatora, "-")

        self.tekst.ro_insert("end", "\n\n")
        self.tekst.ro_insert("end", komunikat, ("wyszarzone", "wyśrodkowane"))
        self.tekst.ro_insert("end", "\n")
