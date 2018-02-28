"""Główny interfejs gry."""

import tkinter as tk
from tkinter import ttk

from plansza import Plansza
from mechanika import Gra
from komunikaty import Komunikator
from .plansza import PlanszaGracza, PlanszaPrzeciwnika
from .kontrola import KontrolaAtaku, KontrolaFloty, KontrolaGry
from .komunikaty import PasekKomunikatow
from . import stale


class Interfejs(ttk.Frame):
    """Główny interfejs gry."""

    def __init__(self, rodzic, kolumny, rzedy):
        super().__init__(rodzic)
        self.grid()
        self.ustaw_style()
        gracz = Gra(Plansza(kolumny, rzedy))
        przeciwnik = Gra(Plansza(kolumny, rzedy))
        self.buduj_plansze(gracz, przeciwnik)
        self.buduj_sekcje_kontroli()
        self.buduj_pasek_komunikatow()
        self.ustaw_siatke()
        self.przekaz_odnosniki()
        self.wybierz_statek_startowy()
        self.przekaz_komunikator()
        self.wyswietl_komunikaty()

    def ustaw_style(self):
        """Ustawia style dla okna głównego."""
        self.styl = ttk.Style()
        self.styl.configure(
            "Bold.TLabel",
            font=stale.CZCIONKI["pogrubiona"]
        )
        self.styl.configure(
            "Mała.TLabel",
            font=stale.CZCIONKI["mała"]
        )

    def buduj_plansze(self, gracz, przeciwnik):
        """Buduje plansze gracza i przeciwnika"""
        self.plansza_gracza = PlanszaGracza(self, 10, 10, gra=gracz)
        self.plansza_przeciwnika = PlanszaPrzeciwnika(self, 10, 10, gra=przeciwnik)

    def buduj_sekcje_kontroli(self):
        """Buduje sekcje kontroli: ataku, floty i gry po prawej stronie okna głównego."""
        self.kontrola_ataku = KontrolaAtaku(
            self,
            (0, 10, 10, 10),  # odstęp zewnętrzny (lewo, góra, prawo, dół)
            (5, 10, 5, 5),  # odstęp wewnętrzny
            plansza_gracza=self.plansza_gracza,
            plansza_przeciwnika=self.plansza_przeciwnika
        )
        self.kontrola_floty = KontrolaFloty(
            self,
            (0, 0, 10, 10),
            (5, 7, 5, 13),
            plansza_gracza=self.plansza_gracza,
            plansza_przeciwnika=self.plansza_przeciwnika
        )
        self.kontrola_gry = KontrolaGry(
            self,
            (0, 0, 10, 10),
            (5, 10, 5, 5),
            "",
            plansza_gracza=self.plansza_gracza,
            plansza_przeciwnika=self.plansza_przeciwnika
        )

    def buduj_pasek_komunikatow(self):
        """Buduje pasek komunikatów na dole okna głównego"""
        self.pasek_komunikatow = PasekKomunikatow(
            self,
            (10, 0, 10, 11),
            self.plansza_gracza.gra.plansza.kolumny,
            self.plansza_gracza.gra.plansza.rzedy
        )

    def ustaw_siatke(self):
        """
        Konfiguruje layout managera. Dopuszcza powiększanie trzeciej kolumny (w poziomie) i czwartego rzędu (w pionie). Zmienia ustawienia dwóch ostatnich rzędów w zależności od wielkości planszy.
        """
        self.plansza_gracza.grid(column=0, row=0, rowspan=3, sticky=tk.N)
        self.plansza_przeciwnika.grid(column=1, row=0, rowspan=3, sticky=tk.N)
        self.kontrola_ataku.grid(column=2, row=0, sticky="nwe")
        self.kontrola_floty.grid(column=2, row=1, sticky="nsew")
        self.kontrola_gry.grid(column=2, row=2, rowspan=2, sticky="nwe")
        self.pasek_komunikatow.grid(column=0, row=3, columnspan=2, sticky="ns")
        # dla plansz mniejszych niż 12 rzędów pasek komunikatów musi zajmować dwa rzędy siatki okna głównego a sekcja kontroli gry jeden (dla większych jest na odwrót)
        if self.plansza_gracza.gra.plansza.rzedy < 12:
            self.plansza_gracza.grid(rowspan=2)
            self.plansza_gracza.grid(rowspan=2)
            self.kontrola_floty.grid(rowspan=2)
            self.kontrola_gry.grid(row=3, rowspan=1)
            self.pasek_komunikatow.grid(row=2, rowspan=2)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

    def przekaz_odnosniki(self):
        """Przekazuje odnośniki pomiędzy sekcjami."""
        # PG
        self.plansza_przeciwnika.pg = self.plansza_gracza
        # KA
        self.plansza_gracza.ka = self.kontrola_ataku
        self.plansza_przeciwnika.ka = self.kontrola_ataku
        self.kontrola_gry.ka = self.kontrola_ataku
        # KF
        self.plansza_gracza.kf = self.kontrola_floty
        self.plansza_przeciwnika.kf = self.kontrola_floty
        self.kontrola_gry.kf = self.kontrola_floty
        # KG
        self.plansza_przeciwnika.kg = self.kontrola_gry

    def wybierz_statek_startowy(self):
        """Wybiera największy statek na rozpoczęcie gry."""
        self.plansza_gracza.wybierz_statek(self.plansza_gracza.gra.plansza.statki[0])
        self.kontrola_floty.drzewo_g.see("niezatopione")

    def przekaz_komunikator(self):
        """Tworzy, ustawia i przekazuje widżetom komunikator."""
        self.komunikator = Komunikator(self.pasek_komunikatow.tekst)
        self.plansza_przeciwnika.komunikator = self.komunikator
        self.kontrola_gry.komunikator = self.komunikator

    def wyswietl_komunikaty(self):
        """Wyświetla komunikaty w polu tekstowym paska komunikatów."""
        self.komunikator.o_rozpoczeciu_gry(self.plansza_gracza.gra.plansza)
        self.komunikator.o_rundzie(self.plansza_gracza.gra)
