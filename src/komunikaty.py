"""
Komunikaty tekstowe w grze.
"""

import tkinter as tk

from plansza import Pole, Statek


class Komunikator:
    """Obsługuje pole tekstowe paska stanu (TODO: oraz tooltipy)."""

    LICZBA_MNOGA = {
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
    BIERNIKI = {
        "korweta": "korwetę",
        "fregata": "fregatę"
    }
    GWIAZDKA = "✱"

    def __init__(self, pole_tekstowe):
        self.tekst = pole_tekstowe

    @staticmethod
    def do_indeksu(liczba):
        """Zamienia liczbę na indeks wartości w słowniku liczby mnogiej."""
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

    def o_rozpoczeciu_gry(self, plansza_gracza):
        """Wyświetla komunikat o rozpoczęciu gry."""
        kolumny, rzedy = plansza_gracza.kolumny, plansza_gracza.rzedy
        rozmiar = plansza_gracza.rozmiar
        ilosc_statkow = len(plansza_gracza.statki)
        ilosc_pol_statkow = plansza_gracza.podaj_ilosc_nietrafionych_pol()
        wg_rang = plansza_gracza.podaj_ilosc_niezatopionych_wg_rang()  # słownik

        self.tekst.ro_insert("1.0", "Gra na planszy o rozmiarze: ")
        self.tekst.ro_insert("end", str(kolumny), "pogrubione")
        self.tekst.ro_insert("end", " " + self.LICZBA_MNOGA["kolumna"][self.do_indeksu(kolumny)] + " x ")
        self.tekst.ro_insert("end", str(rzedy), "pogrubione")
        komunikat = " " + self.LICZBA_MNOGA["rząd"][self.do_indeksu(rzedy)]
        komunikat += " (" + str(rozmiar) + " " + self.LICZBA_MNOGA["pole"][self.do_indeksu(rozmiar)] + "). "
        komunikat += "Umieszczono "
        self.tekst.ro_insert("end", komunikat)
        self.tekst.ro_insert("end", str(ilosc_statkow), "pogrubione")
        komunikat = " " + self.LICZBA_MNOGA["statek"][self.do_indeksu(ilosc_statkow)]
        komunikat += " zajmujących " + str(ilosc_pol_statkow) + " "
        komunikat += self.LICZBA_MNOGA["pole"][self.do_indeksu(ilosc_pol_statkow)] + ". W tym: "
        self.tekst.ro_insert("end", komunikat)
        for ranga in Statek.RANGI:
            self.tekst.ro_insert("end", str(wg_rang[ranga]), "pogrubione")
            komunikat = " " + self.LICZBA_MNOGA[ranga][self.do_indeksu(wg_rang[ranga])]
            komunikat += " (" + Statek.SYMBOLE[ranga] + "), "
            self.tekst.ro_insert("end", komunikat)
        self.tekst.ro_delete("end-3c", "end")
        self.tekst.ro_insert("end", ". Zaczynamy!")

    def o_rundzie(self, gra):
        """Wyświetla komunikat o nowej rundzie."""
        bazowa_dl_separatora = 120
        korekta = round((gra.plansza.kolumny - 8) * 13)
        dl_separatora = bazowa_dl_separatora + korekta
        komunikat = gra.podaj_info_o_rundzie().title()
        komunikat = "  ".join(["  ", self.GWIAZDKA, komunikat, self.GWIAZDKA, "   "])
        komunikat = komunikat.center(dl_separatora, "-")

        self.tekst.ro_insert("end", "\n\n")
        self.tekst.ro_insert("end", komunikat, ("wyszarzone", "wyśrodkowane"))
        self.tekst.ro_insert("end", "\n")
        self.tekst.see("end")

    def o_salwie(self, salwa, statek):
        """Wyświetla komunikat o oddanej salwie."""
        self.tekst.ro_insert("end", "\n")
        self.o_statku(statek)
        komunikat = "oddała" if statek.RANGA_BAZOWA in Statek.RANGI[2:4] else "oddał"
        self.tekst.ro_insert("end", " " + komunikat + " salwę w ")
        komunikat = "polę: " if len(salwa.pola) == 1 else "pola: "
        self.tekst.ro_insert("end", komunikat)
        for i in range(len(salwa.pola)):
            if salwa.trafienia[i]:
                self.tekst.ro_insert("end", salwa.pola[i].w_nawiasach(), ("pogrubione", "trafione"))
            else:
                self.tekst.ro_insert("end", salwa.pola[i].w_nawiasach(), "pogrubione")
            if i == 0:
                if len(salwa.pola) == 2:
                    self.tekst.ro_insert("end", " i ")
                elif len(salwa.pola) == 3:
                    self.tekst.ro_insert("end", ", ")
            if i == 1 and len(salwa.pola) == 3:
                self.tekst.ro_insert("end", " i ")
        self.tekst.see("end")

    def o_statku(self, statek, przypadek="mianownik"):
        """Wyświetla komunikat o statku. W razie potrzeby dokonuje odmiany przez przypadki."""
        statek_info = str(statek).split('"')
        indeks_znaku = self.tekst.index("end-1c").split(".")[1]
        if indeks_znaku == "0":
            self.tekst.ro_insert("end", statek_info[0].title() + '"')
        else:
            if przypadek == "biernik":
                statek_ranga = statek_info[0][:-1]
                if statek_ranga in Statek.RANGI[2:4]:
                    statek_ranga = self.BIERNIKI[statek_ranga]
                    self.tekst.ro_insert("end", statek_ranga + ' "')
                else:
                    self.tekst.ro_insert("end", statek_info[0] + '"')
            else:
                self.tekst.ro_insert("end", statek_info[0] + '"')
        self.tekst.ro_insert("end", statek_info[1], "pogrubione")
        self.tekst.ro_insert("end", '"' + statek_info[2])

    def o_zatopieniu(self, ofiara, napastnik):
        """Wyświetla komunikat o zatopieniu ofiary przez napastnika."""
        self.tekst.ro_insert("end", "\n")
        self.tekst.ro_insert("end", "Statek przeciwnika, ")
        self.o_statku(ofiara)
        self.tekst.ro_insert("end", ", został zatopiony przez ")
        self.o_statku(napastnik, "biernik")
        self.tekst.see("end")
