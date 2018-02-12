#!/usr/bin/env python3

"""
Graficzny interfejs użytkownika
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import math

from plansza import Plansza, Pole, Statek
from mechanika import Gracz
from komunikaty import Komunikator


# ****************************************** SEKCJA PLANSZ **************************************************


class PoleGUI(ttk.Button):
    """Graficzna reprezentacja pola planszy. Nie dopuszcza powiększania na ekranie."""

    GLIFY = {
        "pudło": "•",
        "trafione": "�"
    }
    KOLORY = {
        "woda": "powder blue",
        "woda-active": "light cyan",
        "pudło": "DeepSkyBlue3",
        "pudło-active": "deep sky blue",
        "trafione": "light coral",
        "trafione-active": "light pink",
        "zatopione": "ivory4",
        "zatopione-active": "ivory3",
        "wybrane": "khaki2",
        "wybrane-active": "lemon chiffon",
        "wybrane&trafione": "OrangeRed2",
        "wybrane&trafione-active": "chocolate1",
        "atak-active": "DarkSeaGreen1"
    }
    STYLE = {
        "woda": "Woda.TButton",
        "pudło": "Pudło.TButton",
        "trafione": "Trafione.TButton",
        "zatopione": "Zatopione.TButton",
        "wybrane": "Wybrane.TButton",
        "wybrane&trafione": "Wybrane&Trafione.TButton",
        "atak": "Atak.TButton",
        "bazowe": "TButton"
    }

    def __init__(self, rodzic, pole, *args, **kwargs):
        super().__init__(rodzic, *args, **kwargs)
        self.pole = pole


class Sekcja(ttk.Frame):
    """
    Sekcja okna głównego z obramowaniem, wytłuszczoną etykietą i odstępem zewnętrznym (na zewnątrz obramowania) i wewnętrznym (od wewnątrz obramowania). Odstęp przyjmuje wartości akceptowane przez opcje `padding` Tkintera.
    """

    def __init__(self, rodzic, odstep_zewn, odstep_wewn, tytul):
        super().__init__(rodzic, padding=odstep_zewn)
        self.tytul = tk.StringVar(value=tytul)
        self.ustaw_sie(odstep_wewn, tytul)

    def ustaw_sie(self, odstep_wewn, tytul):
        """Ustawia interfejs pod widżety."""
        etykieta = ttk.Label(textvariable=self.tytul, style="Bold.TLabel")
        self.etyramka = ttk.LabelFrame(self, labelwidget=etykieta, padding=odstep_wewn)
        self.etyramka.grid()


class PlanszaGUI(Sekcja):
    """Graficzna reprezentacja planszy - szczegółowa implementacja w klasach potomnych. Nie dopuszcza powiększania."""

    def __init__(self, rodzic, odstep_zewn, odstep_wewn, tytul, **kwargs):
        super().__init__(rodzic, odstep_zewn, odstep_wewn, tytul)
        self.gracz = kwargs["gracz"]
        # self.tytul = tytul
        self.pola_gui = [[0 for kolumna in range(self.gracz.plansza.kolumny)] for rzad in range(self.gracz.plansza.rzedy)]  # matryca (lista rzędów (list)) obiektów klasy PoleGUI (tu inicjalizowanych jako "0")
        self.ustaw_style()
        self.buduj_etykiety()
        self.buduj_pola()

    def ustaw_style(self):
        """Definiuje style dla pól."""
        self.styl = ttk.Style()
        # woda
        self.styl.configure(
            PoleGUI.STYLE["woda"],
            relief="sunken",
            background=PoleGUI.KOLORY["woda"]
        )
        self.styl.map(
            PoleGUI.STYLE["woda"],
            relief=[("active", "sunken"), ("disabled", "sunken")],
            background=[("active", PoleGUI.KOLORY["woda-active"]), ("disabled", "gray")]
        )
        # pudło
        self.styl.configure(
            PoleGUI.STYLE["pudło"],
            relief="sunken",
            background=PoleGUI.KOLORY["pudło"]
        )
        self.styl.map(
            PoleGUI.STYLE["pudło"],
            relief=[("active", "sunken"), ("disabled", "sunken")],
            background=[("active", PoleGUI.KOLORY["pudło-active"]), ("disabled", "gray")]
        )
        # trafione
        self.styl.configure(
            PoleGUI.STYLE["trafione"],
            background=PoleGUI.KOLORY["trafione"]
        )
        self.styl.map(
            PoleGUI.STYLE["trafione"],
            background=[("active", PoleGUI.KOLORY["trafione-active"]), ("disabled", "gray")]
        )
        # zatopione
        self.styl.configure(
            PoleGUI.STYLE["zatopione"],
            relief="sunken",
            foreground="white",
            background=PoleGUI.KOLORY["zatopione"]
        )
        self.styl.map(
            PoleGUI.STYLE["zatopione"],
            relief=[("active", "sunken"), ("disabled", "sunken")],
            foreground=[("active", "white"), ("disabled", "white")],
            background=[("active", PoleGUI.KOLORY["zatopione-active"]), ("disabled", "gray")]
        )

    def buduj_etykiety(self):
        """Buduje etykiety kolumn i rzędów."""
        for kolumna in range(self.gracz.plansza.kolumny):
            ttk.Label(
                self.etyramka,
                text=Plansza.ALFABET[kolumna + 1],
                anchor=tk.CENTER
            ).grid(
                row=0,
                column=kolumna + 1,
                sticky=tk.W + tk.E,
                pady=(0, 3)
            )
        for rzad in range(self.gracz.plansza.rzedy):
            ttk.Label(
                self.etyramka,
                text=str(rzad + 1)
            ).grid(
                column=0,
                row=rzad + 1,
                sticky=tk.E,
                padx=(0, 6)
            )

    def buduj_pola(self):
        """Buduje pola planszy"""
        for i in range(self.gracz.plansza.kolumny):
            for j in range(self.gracz.plansza.rzedy):
                kolumna, rzad = i + 1, j + 1
                pole_gui = PoleGUI(
                    self.etyramka,
                    self.gracz.plansza.podaj_pole(kolumna, rzad),
                    text="",
                    width=2
                )
                pole_gui.grid(
                    column=kolumna,
                    row=rzad,
                    sticky=tk.W
                )
                self.pola_gui[j][i] = pole_gui

    def podaj_pole_gui(self, kolumna, rzad):
        """Podaje pole planszy."""
        return self.pola_gui[rzad - 1][kolumna - 1]

    def oznacz_pudlo(self, pole_gui):
        """Oznacza podane pole jako pudło."""
        pole_gui.pole.znacznik = Pole.ZNACZNIKI["pudło"]
        pole_gui.configure(style=PoleGUI.STYLE["pudło"], text=PoleGUI.GLIFY["pudło"])

    def oznacz_trafione(self, pole_gui, symbol=None):
        """Oznacza podane pole jako trafione."""
        pole_gui.pole.znacznik = Pole.ZNACZNIKI["trafione"]
        if symbol:
            pole_gui.configure(style=PoleGUI.STYLE["trafione"], text=symbol)
        else:
            pole_gui.configure(style=PoleGUI.STYLE["trafione"])


    def zatop_statek(self, statek, symbole=False):
        """Oznacza pola wskazanego statku jako zatopione."""
        for pole in statek.pola:
            pole.znacznik = Pole.ZNACZNIKI["zatopione"]
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            pole_gui.configure(style=PoleGUI.STYLE["zatopione"])
            if symbole:
                pole_gui.configure(text=statek.SYMBOLE[statek.RANGA_BAZOWA])

        self.gracz.plansza.zatopione.append(statek)
        self.gracz.plansza.niezatopione.remove(statek)


class PlanszaGracza(PlanszaGUI):
    """Graficzna reprezentacja planszy gracza."""

    def __init__(self, rodzic, odstep_zewn, odstep_wewn, tytul="Gracz", **kwargs):
        super().__init__(rodzic, odstep_zewn, odstep_wewn, tytul, **kwargs)
        self.kontrola_ataku = None  # Kontrola Ataku przekazuje tutaj odnośnik do siebie na koniec swojej inicjalizacji
        self.drzewo_floty = None  # Kontrola Floty jw.
        self.pozycja_pola = None  # Kontrola Floty jw.
        self.ustaw_style_gracza()
        self.powiaz_callbacki()
        self.odkryj_wszystkie_pola()

        # testy
        # statek = self.gracz.plansza.statki[0]
        # self.oznacz_trafione(self.podaj_pole_gui(*statek.polozenie.podaj_wspolrzedne()))
        # statek = self.gracz.plansza.statki[3]
        # self.zatop_statek(statek)

    def ustaw_style_gracza(self):
        """Definiuje style dla pól."""
        # wybrane
        self.styl.configure(
            PoleGUI.STYLE["wybrane"],
            background=PoleGUI.KOLORY["wybrane"]
        )
        self.styl.map(
            PoleGUI.STYLE["wybrane"],
            background=[("active", PoleGUI.KOLORY["wybrane-active"]), ("disabled", "gray")]
        )
        # wybrane&trafione
        self.styl.configure(
            PoleGUI.STYLE["wybrane&trafione"],
            background=PoleGUI.KOLORY["wybrane&trafione"]
        )
        self.styl.map(
            PoleGUI.STYLE["wybrane&trafione"],
            background=[("active", PoleGUI.KOLORY["wybrane&trafione-active"]), ("disabled", "gray")]
        )

    def powiaz_callbacki(self):
        """Wiąże callbacki."""
        # wszystkie pola
        for i in range(self.gracz.plansza.kolumny):
            for j in range(self.gracz.plansza.rzedy):
                kolumna, rzad = i + 1, j + 1
                # lambda bez własnych argumentów (w formie: lambda: self.na_klikniecie(kolumna, rzad) nie zadziała prawidłowo w tym przypadku - zmienne przekazywane do każdej funkcji (anonimowej czy nie - bez różnicy) są zawsze ewaluowane dopiero w momencie wywołania tej funkcji, tak więc w tym przypadku w danej iteracji pętli zostają przekazane zmienne "i" i "j" (nazwy) a nie ich wartości - wartości zostaną ewaluowane dopiero w momencie wywołania callbacka (czyli naciśnięcia przycisku) i będzie to wartość z ostatniej iteracji dla wszystkich przycisków, więcej tutaj: https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture/23557126))
                pole_gui = self.podaj_pole_gui(kolumna, rzad)
                pole_gui.configure(command=lambda x=kolumna, y=rzad: self.na_klikniecie(x, y))  # lambda konieczna, bo nie da się tego obsłużyć tak jak niżej z bind() - w przypadku przypisywania callbacków opcją 'command' nie ma przekazywania obiektu zdarzenia, z którego można by pobrać współrzędne pola
                pole_gui.bind("<Enter>", self.na_wejscie)
                pole_gui.bind("<Leave>", self.na_wyjscie)
        # okno główne
        self.winfo_toplevel().bind("[", self.na_nawias_kw_lewy)
        self.winfo_toplevel().bind("]", self.na_nawias_kw_prawy)

    # CALLBACK wszystkich pól
    def na_klikniecie(self, kolumna, rzad):
        """
        Wybiera kliknięty statek, kasując wybór poprzedniego. Zatopione statki nie są wybierane. Ten sam mechanizm jest uruchamiany po wyborze statku w sekcjach kontroli ataku i floty.
        """
        statek = self.gracz.plansza.podaj_statek(self.podaj_pole_gui(kolumna, rzad).pole)
        self.zmien_statek(statek)

        print("Kliknięcie w polu: ({}{})".format(Plansza.ALFABET[kolumna], rzad))  # test

    # CALLBACK wszystkich pól
    def na_wejscie(self, event=None):
        """
        Wyświetla pozycję pola w sekcji kontroli floty.
        """
        self.pozycja_pola.set(event.widget.pole)

    # CALLBACK wszystkich pól
    def na_wyjscie(self, event=None):
        """
        Kasuje wyświetlaną pozycję pola w sekcji kontroli floty.
        """
        self.pozycja_pola.set("")

    # CALLBACK okna głównego
    def na_nawias_kw_lewy(self, event=None):
        """
        Przewija wybrany statek do tyłu.
        """
        if len(self.gracz.tura.statki) > 1:  # jeśli jest co przewijać
            indeks = self.gracz.tura.statki.index(self.gracz.tura.runda.statek)
            if indeks > 0:  # jeśli nie jesteśmy na początku kolejki
                statek = self.gracz.tura.statki[indeks - 1]
            else:
                statek = self.gracz.tura.statki[len(self.gracz.tura.statki) - 1]
            self.zmien_statek(statek)

    # CALLBACK okna głównego
    def na_nawias_kw_prawy(self, event=None):
        """
        Przewija wybrany statek do przodu.
        """
        if len(self.gracz.tura.statki) > 1:  # jeśli jest co przewijać
            indeks = self.gracz.tura.statki.index(self.gracz.tura.runda.statek)
            if indeks < len(self.gracz.tura.statki) - 1:  # jeśli nie jesteśmy na końcu kolejki
                statek = self.gracz.tura.statki[indeks + 1]
            else:
                statek = self.gracz.tura.statki[0]
            self.zmien_statek(statek)

    def zmien_statek(self, statek):
        """Zmienia wybrany statek"""
        if statek and not statek.czy_zatopiony():
            self.kasuj_wybor_statku(self.gracz.tura.runda.statek)
            self.wybierz_statek(statek)

    def wybierz_statek(self, statek):
        """Wybiera statek na planszy"""
        for pole in statek.pola:
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            if pole_gui.pole.znacznik == Pole.ZNACZNIKI["trafione"]:
                pole_gui.configure(style=PoleGUI.STYLE["wybrane&trafione"])
            else:
                pole_gui.configure(style=PoleGUI.STYLE["wybrane"])
        self.gracz.tura.runda.statek = statek
        # kontrola widżetów w innych sekcjach
        self.kontrola_ataku.combo_statku.set(statek)
        self.kontrola_ataku.zmien_salwy(statek)
        if len(self.drzewo_floty.selection()) > 0:
            self.drzewo_floty.selection_remove(self.drzewo_floty.selection()[0])
        iid = str(self.gracz.plansza.niezatopione.index(statek))
        self.drzewo_floty.selection_add(iid)
        if self.drzewo_floty.bbox(iid, column="statek") == "":
            self.drzewo_floty.see(iid)

    def kasuj_wybor_statku(self, statek):
        """Kasuje wybór statku na planszy"""
        for pole in statek.pola:
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            if pole_gui.pole.znacznik == Pole.ZNACZNIKI["trafione"]:
                pole_gui.configure(style=PoleGUI.STYLE["trafione"])
            else:
                pole_gui.configure(style=PoleGUI.STYLE["bazowe"])


    def odkryj_wszystkie_pola(self):
        """Odkrywa wszystkie pola planszy."""
        for rzad in self.pola_gui:
            for pole_gui in rzad:
                statek = self.gracz.plansza.podaj_statek(pole_gui.pole)
                if pole_gui.pole.znacznik in (Pole.ZNACZNIKI["puste"], Pole.ZNACZNIKI["obwiednia"]):
                    pole_gui.configure(style=PoleGUI.STYLE["woda"])
                else:
                    pole_gui.configure(text=statek.SYMBOLE[statek.RANGA_BAZOWA])


class PlanszaPrzeciwnika(PlanszaGUI):
    """Graficzna reprezentacja planszy przeciwnika."""

    def __init__(self, rodzic, odstep_zewn, odstep_wewn, tytul="Przeciwnik", **kwargs):
        super().__init__(rodzic, odstep_zewn, odstep_wewn, tytul, **kwargs)
        self.combo_orientacji = None  # widżet przekazywany przez Kontrolę Ataku pod koniec jej inicjalizacji
        self.pozycje_salwy = None  # jw.
        self.komunikator = None  # przekazywany przez rodzica
        self.drugi_gracz = None  # jw.
        self.ustaw_style_przeciwnika()
        self.powiaz_callbacki()
        self.zmien_podswietlanie_nieodkrytych(PoleGUI.STYLE["atak"])

    def ustaw_style_przeciwnika(self):
        """Definiuje style dla pól."""
        # atak
        self.styl.map(
            PoleGUI.STYLE["atak"],
            background=[("active", PoleGUI.KOLORY["atak-active"])]
        )

    def zmien_podswietlanie_nieodkrytych(self, styl_pola_gui):
        """Zmienia podświetlanie nieodkrytych pól wg podanego stylu."""
        for rzad in self.pola_gui:
            for pole_gui in rzad:
                if pole_gui.pole.znacznik in [
                    Pole.ZNACZNIKI["puste"],
                    Pole.ZNACZNIKI["obwiednia"],
                    Pole.ZNACZNIKI["statek"]
                ]:
                    pole_gui.configure(style=styl_pola_gui)

    def powiaz_callbacki(self):
        """Wiąże callbacki we wszystkich polach."""
        for i in range(self.gracz.plansza.kolumny):
            for j in range(self.gracz.plansza.rzedy):
                kolumna, rzad = i + 1, j + 1
                pole_gui = self.podaj_pole_gui(kolumna, rzad)
                pole_gui.configure(command=lambda x=kolumna, y=rzad: self.na_klikniecie(x, y))
                pole_gui.bind("<Enter>", self.na_wejscie)
                pole_gui.bind("<Leave>", self.na_wyjscie)
                # obracanie podświetlaniem
                pole_gui.bind("<ButtonRelease-3>", self.na_wejscie)
                pole_gui.bind("<ButtonPress-3>", self.na_wyjscie)

    # CALLBACK wszystkich pól
    def na_klikniecie(self, kolumna, rzad):
        """
        W zależności od wybranej orientacji w Kontroli Ataku odkrywa na planszy odpowiednie pola (lub pole), dodaje salwy w rundzie i wyświetla komunikaty o salwie i zatopieniu.
        """
        ilosc_zatopionych = len(self.gracz.plansza.zatopione)
        # 1 pole
        self.odkryj_pole(kolumna, rzad)
        if self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[0]:
            self.drugi_gracz.tura.runda.dodaj_oddana_salwe(self.gracz.plansza, (kolumna, rzad))
        # 2 pola w prawo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[1]:
            self.odkryj_pole(kolumna + 1, rzad)
            self.drugi_gracz.tura.runda.dodaj_oddana_salwe(
                self.gracz.plansza,
                (kolumna, rzad),
                (kolumna + 1, rzad)
            )
        # 2 pola w dół
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[2]:
            self.odkryj_pole(kolumna, rzad + 1)
            self.drugi_gracz.tura.runda.dodaj_oddana_salwe(
                self.gracz.plansza,
                (kolumna, rzad),
                (kolumna, rzad + 1)
            )
        # 2 pola w lewo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[3]:
            self.odkryj_pole(kolumna - 1, rzad)
            self.drugi_gracz.tura.runda.dodaj_oddana_salwe(
                self.gracz.plansza,
                (kolumna, rzad),
                (kolumna - 1, rzad)
            )
        # 2 pola w górę
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[4]:
            self.odkryj_pole(kolumna, rzad - 1)
            self.drugi_gracz.tura.runda.dodaj_oddana_salwe(
                self.gracz.plansza,
                (kolumna, rzad),
                (kolumna, rzad - 1)
            )
        # 3 pola poziomo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[5]:
            self.odkryj_pole(kolumna - 1, rzad)
            self.odkryj_pole(kolumna + 1, rzad)
            self.drugi_gracz.tura.runda.dodaj_oddana_salwe(
                self.gracz.plansza,
                (kolumna, rzad),
                (kolumna - 1, rzad),
                (kolumna + 1, rzad)
            )
        # 3 pola pionowo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[6]:
            self.odkryj_pole(kolumna, rzad - 1)
            self.odkryj_pole(kolumna, rzad + 1)
            self.drugi_gracz.tura.runda.dodaj_oddana_salwe(
                self.gracz.plansza,
                (kolumna, rzad),
                (kolumna, rzad - 1),
                (kolumna, rzad + 1)
            )
        # 3 pola L
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[7]:
            self.odkryj_pole(kolumna, rzad - 1)
            self.odkryj_pole(kolumna + 1, rzad)
            self.drugi_gracz.tura.runda.dodaj_oddana_salwe(
                self.gracz.plansza,
                (kolumna, rzad),
                (kolumna, rzad - 1),
                (kolumna + 1, rzad)
            )
        # 3 pola Г
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[8]:
            self.odkryj_pole(kolumna, rzad + 1)
            self.odkryj_pole(kolumna + 1, rzad)
            self.drugi_gracz.tura.runda.dodaj_oddana_salwe(
                self.gracz.plansza,
                (kolumna, rzad),
                (kolumna, rzad + 1),
                (kolumna + 1, rzad)
            )
        # 3 pola Ꞁ
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[9]:
            self.odkryj_pole(kolumna - 1, rzad)
            self.odkryj_pole(kolumna, rzad + 1)
            self.drugi_gracz.tura.runda.dodaj_oddana_salwe(
                self.gracz.plansza,
                (kolumna, rzad),
                (kolumna - 1, rzad),
                (kolumna, rzad + 1)
            )
        # 3 pola ⅃
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[10]:
            self.odkryj_pole(kolumna - 1, rzad)
            self.odkryj_pole(kolumna, rzad - 1)
            self.drugi_gracz.tura.runda.dodaj_oddana_salwe(
                self.gracz.plansza,
                (kolumna, rzad),
                (kolumna - 1, rzad),
                (kolumna, rzad - 1)
            )
        # komunikaty
        self.komunikator.o_salwie(self.drugi_gracz.tura.runda.salwy_oddane[-1], self.drugi_gracz.tura.runda.statek)
        if len(self.gracz.plansza.zatopione) > ilosc_zatopionych:  # jeśli było zatopienie
            ofiara = self.gracz.plansza.zatopione[-1]
            napastnik = self.drugi_gracz.tura.runda.statek
            self.komunikator.o_zatopieniu(ofiara, napastnik)
        print("Kliknięcie w polu: ({}{})".format(Plansza.ALFABET[kolumna], rzad))  # test

    # CALLBACK wszystkich pól
    def na_wejscie(self, event):
        """
        W zależności od wybranej orientacji w Kontroli Ataku podświetla lub nie dodatkowe, sąsiednie pola w odpowiedniej konfiguracji.
        """
        kolumna, rzad = event.widget.pole.podaj_wspolrzedne()
        self.pozycje_salwy.pierwsza.set(event.widget.pole)
        # 2 pola w prawo
        if self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[1]:
            self.zmien_stan_pola(kolumna + 1, rzad, "active", "druga")
        # 2 pola w dół
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[2]:
            self.zmien_stan_pola(kolumna, rzad + 1, "active", "druga")
        # 2 pola w lewo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[3]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active", "druga")
        # 2 pola w górę
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[4]:
            self.zmien_stan_pola(kolumna, rzad - 1, "active", "druga")
        # 3 pola poziomo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[5]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active", "druga")
            self.zmien_stan_pola(kolumna + 1, rzad, "active", "trzecia")
        # 3 pola pionowo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[6]:
            self.zmien_stan_pola(kolumna, rzad - 1, "active", "druga")
            self.zmien_stan_pola(kolumna, rzad + 1, "active", "trzecia")
        # 3 pola L
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[7]:
            self.zmien_stan_pola(kolumna, rzad - 1, "active", "druga")
            self.zmien_stan_pola(kolumna + 1, rzad, "active", "trzecia")
        # 3 pola Г
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[8]:
            self.zmien_stan_pola(kolumna, rzad + 1, "active", "druga")
            self.zmien_stan_pola(kolumna + 1, rzad, "active", "trzecia")
        # 3 pola Ꞁ
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[9]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active", "druga")
            self.zmien_stan_pola(kolumna, rzad + 1, "active", "trzecia")
        # 3 pola ⅃
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[10]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active", "druga")
            self.zmien_stan_pola(kolumna, rzad - 1, "active", "trzecia")

    # CALLBACK wszystkich pól
    def na_wyjscie(self, event):
        """
        W zależności od wybranej orientacji w Kontroli Ataku kasuje podświetlenie dodatkowych, sąsiednich pól (lub pola) wywołane wcześniejszym uruchomieniem callbacka `na_wejscie()`.
        """
        kolumna, rzad = event.widget.pole.podaj_wspolrzedne()
        self.pozycje_salwy.pierwsza.set("")
        # 2 pola w prawo
        if self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[1]:
            self.zmien_stan_pola(kolumna + 1, rzad, "!active", "druga")
        # 2 pola w dół
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[2]:
            self.zmien_stan_pola(kolumna, rzad + 1, "!active", "druga")
        # 2 pola w lewo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[3]:
            self.zmien_stan_pola(kolumna - 1, rzad, "!active", "druga")
        # 2 pola w górę
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[4]:
            self.zmien_stan_pola(kolumna, rzad - 1, "!active", "druga")
        # 3 pola poziomo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[5]:
            self.zmien_stan_pola(kolumna - 1, rzad, "!active", "druga")
            self.zmien_stan_pola(kolumna + 1, rzad, "!active", "trzecia")
        # 3 pola pionowo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[6]:
            self.zmien_stan_pola(kolumna, rzad - 1, "!active", "druga")
            self.zmien_stan_pola(kolumna, rzad + 1, "!active", "trzecia")
        # 3 pola L
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[7]:
            self.zmien_stan_pola(kolumna, rzad - 1, "!active", "druga")
            self.zmien_stan_pola(kolumna + 1, rzad, "!active", "trzecia")
        # 3 pola Г
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[8]:
            self.zmien_stan_pola(kolumna, rzad + 1, "!active", "druga")
            self.zmien_stan_pola(kolumna + 1, rzad, "!active", "trzecia")
        # 3 pola Ꞁ
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[9]:
            self.zmien_stan_pola(kolumna - 1, rzad, "!active", "druga")
            self.zmien_stan_pola(kolumna, rzad + 1, "!active", "trzecia")
        # 3 pola ⅃
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[10]:
            self.zmien_stan_pola(kolumna - 1, rzad, "!active", "druga")
            self.zmien_stan_pola(kolumna, rzad - 1, "!active", "trzecia")

    def zmien_stan_pola(self, kolumna, rzad, stan, pozycja):
        """
        Zmienia stan pola wg podanych współrzędnych. Aktualizuje treść pozycji pól w sekcji kontroli ataku."""
        if self.gracz.plansza.czy_pole_w_planszy(kolumna, rzad):
            pole_gui = self.podaj_pole_gui(kolumna, rzad)
            pole_gui.state([stan])
            # pozycje pól
            if stan == "active":
                if pozycja == "druga":
                    self.pozycje_salwy.druga.set(pole_gui.pole)
                elif pozycja == "trzecia":
                    self.pozycje_salwy.trzecia.set(pole_gui.pole)
            elif stan == "!active":
                if pozycja == "druga":
                    self.pozycje_salwy.druga.set("")
                elif pozycja == "trzecia":
                    self.pozycje_salwy.trzecia.set("")

    def odkryj_pole(self, kolumna, rzad):
        """Odkrywa na planszy pole wg podanych współrzędnych. Zaznacza pudło lub trafienie. Jeśli trzeba, zatapia trafiony statek (i odkrywa pola jego obwiedni)."""
        if self.gracz.plansza.czy_pole_w_planszy(kolumna, rzad):
            pole_gui = self.podaj_pole_gui(kolumna, rzad)
            if pole_gui.pole.znacznik in (Pole.ZNACZNIKI["puste"], Pole.ZNACZNIKI["obwiednia"]):
                self.oznacz_pudlo(pole_gui)
            elif pole_gui.pole.znacznik == Pole.ZNACZNIKI["statek"]:
                self.oznacz_trafione(pole_gui, PoleGUI.GLIFY["trafione"])
                statek = self.gracz.plansza.podaj_statek(pole_gui.pole)
                if statek.czy_zatopiony():
                    self.zatop_statek(statek, symbole=True)
                    self.odkryj_obwiednie(statek)

    def odkryj_obwiednie(self, statek):
        """Odkrywa na planszy obwiednie zatopionego statku."""
        for pole in statek.obwiednia:
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            # configure("style") zwraca krotkę, której ostatnim elementem jest nazwa stylu
            if pole_gui.configure("style")[-1] not in (PoleGUI.STYLE["woda"], PoleGUI.STYLE["pudło"]):
                pole_gui.configure(style=PoleGUI.STYLE["woda"])
        # test
        print(statek.o_zatopieniu())


# ***************************************** SEKCJA KONTROLI *************************************************


class KontrolaAtaku(Sekcja):
    """
    Sekcja kontroli ataku znajdująca się w prawym górnym rogu głównego interfejsu gry. Dopuszcza powiększanie w poziomie.
    """

    ORIENTACJE = ["•", "•• prawo", "╏ dół", "•• lewo", "╏ góra", "•••", "┇", "L", "Г", "Ꞁ", "⅃"]

    def __init__(self, rodzic, odstep_zewn, odstep_wewn, tytul="Atak", **kwargs):
        super().__init__(rodzic, odstep_zewn, odstep_wewn, tytul)
        self.plansza_g = kwargs["plansza_gracza"]
        self.plansza_p = kwargs["plansza_przeciwnika"]
        self.ustaw_style()
        self.ustaw_etyramke()
        self.buduj_etykiety()
        self.buduj_comboboksy()
        self.ustaw_combo_readonly()
        self.pozycje_salwy = PozycjeSalwy(self.etyramka)
        self.przekaz_odnosniki()
        self.powiaz_callbacki()

    def ustaw_style(self):
        """Ustawia style dla widżetów"""
        self.styl = ttk.Style()
        self.styl.configure("KA.TCombobox")
        self.styl.map(
            "KA.TCombobox",
            fieldbackground=[("readonly", "white")]
        )
        self.styl.configure(
            "PozycjaPolaKA.TLabel",
            anchor=tk.CENTER,
            font=GraGUI.CZCIONKI["mała"],
            width=4
        )

    def ustaw_etyramke(self):
        """Ustawia etyramkę pod widżety."""
        self.etyramka.grid(sticky="we")
        self.etyramka.columnconfigure(0, weight=1)  # zgłasza wyżej powiększanie w poziomie

    def buduj_etykiety(self):
        """Buduje etykiety."""
        ttk.Label(
            self.etyramka,
            text="Wybierz statek:",
            style="Mała.TLabel"
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky=tk.W
        )
        ttk.Label(
            self.etyramka,
            text="Wybierz salwę:",
            style="Mała.TLabel"
        ).grid(
            row=2,
            column=0,
            sticky=tk.W,
            pady=(5, 0)
        )
        ttk.Label(
            self.etyramka,
            text="Wybierz orientację:",
            style="Mała.TLabel"
        ).grid(
            row=2,
            column=1,
            sticky=tk.W,
            pady=(5, 0)
        )

    def buduj_comboboksy(self):
        """Buduje comboboksy."""
        # wybór statku
        self.combo_statku = ComboZeZmianaCzcionki(
            self.etyramka,
            styl="KA.TCombobox",
            font=GraGUI.CZCIONKI["mała"],
            values=self.plansza_g.gracz.tura.statki,
            width=35
        )
        self.combo_statku.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=tk.W
        )
        self.combo_statku.configure(font=GraGUI.CZCIONKI["mała"])  # to zmienia tylko czcionkę pola tekstowego (Entry), które jest częścią comboboksa

        # wybór salwy
        self.combo_salwy = ComboZeZmianaCzcionki(
            self.etyramka,
            styl="KA.TCombobox",
            font=GraGUI.CZCIONKI["mała"],
            width=6
        )
        self.combo_salwy.grid(
            row=3,
            column=0,
            sticky=tk.W,
            pady=(0, 10)
        )
        self.combo_salwy.configure(font=GraGUI.CZCIONKI["mała"])

        # wybór orientacji
        self.combo_orientacji = ComboZeZmianaCzcionki(
            self.etyramka,
            styl="KA.TCombobox",
            font=GraGUI.CZCIONKI["mała"],
            width=7
        )
        self.combo_orientacji.grid(
            row=3,
            column=1,
            sticky=tk.W,
            pady=(0, 10)
        )
        self.combo_orientacji.configure(font=GraGUI.CZCIONKI["mała"])

    def ustaw_combo_readonly(self):
        """Ustawia stan comboboksów jako `readonly`"""
        self.combo_statku.state(["readonly"])
        self.combo_salwy.state(["readonly"])
        self.combo_orientacji.state(["readonly"])

    def przekaz_odnosniki(self):
        """Przekazuje własne odnośniki dla event handlerów w planszach"""
        self.plansza_g.kontrola_ataku = self
        self.plansza_p.combo_orientacji = self.combo_orientacji
        self.plansza_p.pozycje_salwy = self.pozycje_salwy

    def powiaz_callbacki(self):
        """Wiąże callbacki"""
        self.combo_statku.bind("<<ComboboxSelected>>", self.na_wybor_statku)
        self.combo_salwy.bind("<<ComboboxSelected>>", self.na_wybor_salwy)
        self.combo_orientacji.bind("<<ComboboxSelected>>", self.na_wybor_orientacji)
        self.winfo_toplevel().bind("<Button-3>", self.na_prawy_przycisk_myszy)

    # CALLBACK combo_statku
    def na_wybor_statku(self, event=None):
        """Zmienia statek na planszy i aktualizuje combo_salwy."""
        event.widget.selection_clear()  # czyści tło pola tekstowego comboboksa
        indeks = event.widget.current()
        wybrany_statek = self.plansza_g.gracz.tura.statki[indeks]
        self.plansza_g.zmien_statek(wybrany_statek)  # plansza aktualizuje obiekt rundy
        self.zmien_salwy(wybrany_statek)

    # CALLBACK combo_salwy
    def na_wybor_salwy(self, event=None):
        """Aktualizuje combo_orientacji."""
        event.widget.selection_clear()
        self.zmien_orientacje(event.widget.get())

    # CALLBACK combo_orientacji
    def na_wybor_orientacji(self, event=None):
        """Czyści pole tekstowe combo_orientacji"""
        event.widget.selection_clear()

    def zmien_salwy(self, statek):
        """Ustawia salwy wybranego statku."""
        self.combo_salwy["values"] = ["{} pole".format(salwa) if salwa == 1 else "{} pola".format(salwa) for salwa in statek.salwy]
        self.combo_salwy.set(self.combo_salwy["values"][0])
        self.zmien_orientacje(self.combo_salwy["values"][0])

    def zmien_orientacje(self, salwa_tekst):
        """Ustawia orientacje wybranej salwy."""
        salwa = int(salwa_tekst[0])
        if salwa == 1:
            self.combo_orientacji["values"] = [self.ORIENTACJE[0]]
            self.wylacz_pozycje_salwy("druga")
            self.wylacz_pozycje_salwy("trzecia")
        elif salwa == 2:
            self.combo_orientacji["values"] = self.ORIENTACJE[1:5]
            self.wlacz_pozycje_salwy("druga")
            self.wylacz_pozycje_salwy("trzecia")
        elif salwa == 3:
            self.combo_orientacji["values"] = self.ORIENTACJE[5:]
            self.wlacz_pozycje_salwy("druga")
            self.wlacz_pozycje_salwy("trzecia")
        self.combo_orientacji.set(self.combo_orientacji["values"][0])

    def wylacz_pozycje_salwy(self, pozycja):
        """Wyłącza podaną pozycję salwy"""
        if pozycja == "druga":
            self.pozycje_salwy.numer_drugiej.grid_remove()
            self.pozycje_salwy.etykieta_drugiej.grid_remove()
        elif pozycja == "trzecia":
            self.pozycje_salwy.numer_trzeciej.grid_remove()
            self.pozycje_salwy.etykieta_trzeciej.grid_remove()

    def wlacz_pozycje_salwy(self, pozycja):
        """Włącza podaną pozycję salwy"""
        if pozycja == "druga":
            self.pozycje_salwy.numer_drugiej.grid()
            self.pozycje_salwy.etykieta_drugiej.grid()
        elif pozycja == "trzecia":
            self.pozycje_salwy.numer_trzeciej.grid()
            self.pozycje_salwy.etykieta_trzeciej.grid()

    # CALLBACK okna głównego
    def na_prawy_przycisk_myszy(self, event=None):
        """Rotuje wybraną orientacją salw."""
        indeks = self.combo_orientacji.current()
        if indeks == len(self.combo_orientacji["values"]) - 1:
            indeks = 0
        else:
            indeks += 1
        self.combo_orientacji.set(self.combo_orientacji["values"][indeks])


class ComboZeZmianaCzcionki(ttk.Combobox):
    """
    Combobox z możliwością zmiany czcionki w liście rozwijanej. Wzięte stąd: https://stackoverflow.com/questions/43086378/how-to-modify-ttk-combobox-fonts/ .Standardowy combobox nie daje takiej możliwości.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<Map>", self._obsluz_czcionke_listy_rozwijanej)

    def _obsluz_czcionke_listy_rozwijanej(self, *args):
        lista_rozwijana = self.tk.eval("ttk::combobox::PopdownWindow {}".format(self))
        self.tk.call("{}.f.l".format(lista_rozwijana), 'configure', '-font', self['font'])


class PozycjeSalwy(ttk.Frame):
    """
    Podsekcja kontroli ataku pokazująca aktualne pozycje pól wybranej salwy.
    """

    def __init__(self, rodzic):
        super().__init__(rodzic)
        self.pierwsza = tk.StringVar()
        self.druga = tk.StringVar()
        self.trzecia = tk.StringVar()
        self.sprawdz_tlo_sytemowe()
        self.ustaw_sie()
        self.buduj_etykiety()

    def ustaw_sie(self):
        """Ustawia interfejs pod widżety."""
        self.grid(row=4, column=0, columnspan=2, sticky="we", pady=(0, 10))

    def buduj_etykiety(self):
        """Buduje etykiety."""
        self.numer_pierwszej = ttk.Label(self, style="Mała.TLabel", text="#1:")
        self.numer_pierwszej.grid(
            row=0,
            column=0,
            sticky=tk.W
        )
        self.numer_drugiej = ttk.Label(self, style="Mała.TLabel", text="#2:")
        self.numer_drugiej.grid(
            row=0,
            column=2,
            sticky=tk.W,
            padx=(25, 0)
        )
        self.numer_trzeciej = ttk.Label(self, style="Mała.TLabel", text="#3:")
        self.numer_trzeciej.grid(
            row=0,
            column=4,
            sticky=tk.W,
            padx=(25, 0)
        )
        self.etykieta_pierwszej = ttk.Label(
            self,
            style="PozycjaPolaKA.TLabel",
            text="",
            textvariable=self.pierwsza
        )
        self.etykieta_pierwszej.grid(row=0, column=1, sticky=tk.W)
        self.etykieta_drugiej = ttk.Label(
            self,
            style="PozycjaPolaKA.TLabel",
            text="",
            textvariable=self.druga
        )
        self.etykieta_drugiej.grid(row=0, column=3, sticky=tk.W)
        self.etykieta_trzeciej = ttk.Label(
            self,
            style="PozycjaPolaKA.TLabel",
            text="",
            textvariable=self.trzecia
        )
        self.etykieta_trzeciej.grid(row=0, column=5, sticky=tk.W)
        self.pierwsza.trace("w", lambda n, i, m, poz=self.pierwsza, et=self.etykieta_pierwszej: self.na_zmiane(poz, et))
        self.druga.trace("w", lambda n, i, m, poz=self.druga, et=self.etykieta_drugiej: self.na_zmiane(poz, et))
        self.trzecia.trace("w", lambda n, i, m, poz=self.trzecia, et=self.etykieta_trzeciej: self.na_zmiane(poz, et))

    def sprawdz_tlo_sytemowe(self):
        """Sprawdza kolor tla systemowego i zapisuje w stałej"""
        self.TLO_SYSTEMOWE = self.winfo_toplevel().cget("bg")

    # CALLBACK każdej pozycji pola
    def na_zmiane(self, pozycja, etykieta):
        """Zmienia tło etykiety pozycji pola."""
        if pozycja.get() == "":
            etykieta.configure(background=self.TLO_SYSTEMOWE)
        else:
            etykieta.configure(background=GraGUI.KOLORY["pozycja-pola"])


class KontrolaFloty(Sekcja):
    """
    Sekcja kontroli floty (całej gracza i zatopionej przeciwnika) znajdująca się w środku po prawej stronie głównego interfejsu gry. Dopuszcza powiększanie w poziomie i w pionie.
    """

    def __init__(self, rodzic, odstep_zewn, odstep_wewn, tytul="Flota", **kwargs):
        super().__init__(rodzic, odstep_zewn, odstep_wewn, tytul)
        self.plansza_g = kwargs["plansza_gracza"]
        self.plansza_p = kwargs["plansza_przeciwnika"]
        self.sprawdz_tlo_sytemowe()
        self.ustaw_style()
        self.ustaw_etyramke()
        self.buduj_drzewa()
        self.buduj_przyciski()
        self.buduj_pozycje_pola()
        self.przekaz_odnosniki()

    def ustaw_style(self):
        """Ustawia style dla widżetów"""
        self.styl = ttk.Style()
        self.styl.configure(
            "PozycjaPolaKF.TLabel",
            anchor=tk.CENTER,
            width=4
        )

    def ustaw_etyramke(self):
        """Ustawia etyramkę pod widżety."""
        self.etyramka.grid(sticky="nsew")
        # zgłasza wyżej powiększanie w poziomie i w pionie
        self.etyramka.rowconfigure(0, weight=1)
        self.etyramka.columnconfigure(0, weight=1)

    def buduj_drzewa(self):
        """Buduje drzewa floty (gracza i przeciwnika) umieszczone w notesie."""
        notes = ttk.Notebook(self.etyramka)
        # drzewa nie mogą być bezpośrednio umieszczane w notesie - potrzebne ramki pośrednie
        ramka_drzewa_g = ttk.Frame(notes)
        ramka_drzewa_p = ttk.Frame(notes)
        self.drzewo_g = DrzewoFlotyGracza(ramka_drzewa_g, self.plansza_g)
        self.drzewo_p = DrzewoFlotyPrzeciwnika(ramka_drzewa_p, self.plansza_p)
        ramka_drzewa_g.grid(sticky="nsew")
        # zgłasza wyżej powiększanie w poziomie i w pionie
        ramka_drzewa_g.rowconfigure(0, weight=1)
        ramka_drzewa_g.columnconfigure(0, weight=1)
        ramka_drzewa_p.grid(sticky="nsew")
        # zgłasza wyżej powiększanie w poziomie i w pionie
        ramka_drzewa_p.rowconfigure(0, weight=1)
        ramka_drzewa_p.columnconfigure(0, weight=1)
        notes.add(ramka_drzewa_g, text="Gracz")
        notes.add(ramka_drzewa_p, text="Przeciwnik")
        notes.grid(row=0, column=0, columnspan=3, sticky="nsew")
        # zgłasza wyżej powiększanie w poziomie i w pionie
        notes.rowconfigure(0, weight=1)
        notes.columnconfigure(0, weight=1)

    def buduj_przyciski(self):
        """Buduje przyciski przewijania statków."""
        # przycisk do tyłu
        ikona_do_tylu = ImageTk.PhotoImage(Image.open("zasoby/ikona_statku/statek-w-lewo_32x32.png"))
        przycisk_do_tylu = ttk.Button(
            self.etyramka,
            # text="Poprzedni",
            # compound=tk.LEFT,
            image=ikona_do_tylu,
            command=self.plansza_g.na_nawias_kw_lewy
        )
        przycisk_do_tylu.image = ikona_do_tylu  # konieczne ze względu na bug Tkintera (https://stackoverflow.com/questions/22200003/tkinter-button-not-showing-image)
        przycisk_do_tylu.grid(row=1, column=0, sticky=tk.W, pady=(13, 0), padx=35)
        # przycisk do przodu
        ikona_do_przodu = ImageTk.PhotoImage(Image.open("zasoby/ikona_statku/statek-w-prawo_32x32.png"))
        przycisk_do_przodu = ttk.Button(
            self.etyramka,
            # text="Kolejny",
            # compound=tk.LEFT,
            image=ikona_do_przodu,
            command=self.plansza_g.na_nawias_kw_prawy
        )
        przycisk_do_przodu.image = ikona_do_przodu
        przycisk_do_przodu.grid(row=1, column=2, sticky=tk.E, pady=(13, 0), padx=35)

    def buduj_pozycje_pola(self):
        """Buduje etykietę wyświetlającą pozycję pola planszy gracza wskazywanego aktualnie przez kursor."""
        self.pozycja_pola = tk.StringVar()
        self.etykieta_pozycji_pola = ttk.Label(
            self.etyramka,
            style="PozycjaPolaKF.TLabel",
            text="",
            textvariable=self.pozycja_pola
        )
        self.etykieta_pozycji_pola.grid(row=1, column=1, sticky="we", pady=(13, 0))
        self.pozycja_pola.trace("w", self.na_zmiane_pozycji_pola)

    def sprawdz_tlo_sytemowe(self):
        """Sprawdza kolor tla systemowego i zapisuje w stałej"""
        self.TLO_SYSTEMOWE = self.winfo_toplevel().cget("bg")

    # CALLBACK pozycji pola
    def na_zmiane_pozycji_pola(self, *args):
        """Zmienia tło etykiety pozycji pola."""
        if self.pozycja_pola.get() == "":
            self.etykieta_pozycji_pola.configure(background=self.TLO_SYSTEMOWE)
        else:
            self.etykieta_pozycji_pola.configure(background=GraGUI.KOLORY["pozycja-pola"])

    def przekaz_odnosniki(self):
        """Przekazuje własne odnośniki do event handlerów w planszach."""
        self.plansza_g.drzewo_floty = self.drzewo_g
        self.plansza_g.pozycja_pola = self.pozycja_pola


class DrzewoFloty(ttk.Treeview):
    """
    Drzewo wyświetlające statki floty (gracza/przeciwnika). Szczegółowa implementacja w klasach potomnych.
    """

    KOLORY = {
        "podświetlenie-rang": "LemonChiffon2",
        "podświetlenie-rang-zatopione": "plum3",  # TODO
        "podświetlenie-rang-przeciwnik": "DarkOliveGreen2"  # TODO
    }

    def __init__(self, rodzic, plansza_gui):
        super().__init__(rodzic)
        self.plansza_gui = plansza_gui
        self.wys_wiersza = 15

        self.ustaw_style()
        self.ustaw_sie()
        self.wstaw_suwaki(rodzic)
        self.powiaz_escape()

    def ustaw_style(self):
        """Ustawia style dla drzewa."""
        self.styl = ttk.Style()
        self.styl.configure(
            "KF.Treeview",
            font=GraGUI.CZCIONKI["mała"],
            rowheight=self.wys_wiersza
            # rowheight=13
        )
        self.styl.configure(
            "KF.Treeview.Heading",
            font=GraGUI.CZCIONKI["mała"]
        )

    def ustaw_sie(self):
        """Konfiguruje to drzewo."""

        self.configure(
            style="KF.Treeview",
            height=self.podaj_wysokosc(),
            # height=22,
            columns=("statek", "gdzie", "rozmiar", "ofiary"),
            displaycolumns="#all",
            selectmode="browse"
        )
        self.grid(sticky="nsew")

    def podaj_wysokosc(self):
        """
        Podaje wysokość (w wierszach) obliczaną na podstawie rozmiaru planszy.

        Punktem wyjścia do obliczeń były testy, z których wynika, że dla planszy w rozmiarze 26x26 idealna wysokość to 19 wierszy (przy wysokości wiersza równej 15 px - taka wysokość wiersza jest optymalna dla czytelności i wyglądu drzewa, ale dla prostego przeliczania względem planszy lepsza byłaby wysokość równa 13 px (ponieważ pole planszy ma 26 px)).
        """
        # TODO: testy pod Windowsem

        def skoryguj_wysokosc_pod_pasek_komunikatow(wysokosc, rzedy_planszy):
            # po decyzji o tym, że pasek komunikatów będzie umiejscowiony tylko pod planszami a nie pod całym oknem głównym, kolumna sekcji kontroli musi być odpowiednio wyższa, co oznacza konieczność korekty wysokości drzewa
            if rzedy_planszy >= 14:
                korekta = 6  # daje od 31 wierszy drzewa przy 30 wierszach planszy do 7 przy 14
            elif rzedy_planszy == 13:
                korekta = 5  # daje 6 wierszy drzewa
            elif rzedy_planszy == 12:
                korekta = 4  # daje 5 wierszy drzewa
            else:
                korekta = 3  # daje 4 wiersze
            return wysokosc + korekta

        bazowe_wiersze, bazowe_rzedy, wys_pola = 19, 26, 26
        rzedy_planszy = self.plansza_gui.gracz.plansza.rzedy
        delta_planszy = (rzedy_planszy - bazowe_rzedy) * wys_pola
        if delta_planszy < 0:
            wysokosc = bazowe_wiersze - math.ceil(abs(delta_planszy) / self.wys_wiersza)
            if wysokosc < 1:
                wysokosc = 1
            return skoryguj_wysokosc_pod_pasek_komunikatow(wysokosc, rzedy_planszy)
        else:
            wysokosc = bazowe_wiersze + math.floor(abs(delta_planszy) / self.wys_wiersza)
            return skoryguj_wysokosc_pod_pasek_komunikatow(wysokosc, rzedy_planszy)

    def wstaw_suwaki(self, rodzic):
        """Wstawia suwaki."""
        suwak_pionowy = ttk.Scrollbar(rodzic, orient=tk.VERTICAL, command=self.yview)
        suwak_pionowy.grid(column=1, row=0, sticky="ns")
        suwak_poziomy = ttk.Scrollbar(rodzic, orient=tk.HORIZONTAL, command=self.xview)
        suwak_poziomy.grid(column=0, row=1, sticky="we")
        self.configure(yscrollcommand=suwak_pionowy.set, xscrollcommand=suwak_poziomy.set)

    def ustaw_kolumny(self, naglowek_rozmiar):
        """Konfiguruje kolumny."""
        self.heading("statek", text="Statek")
        self.heading("gdzie", text="Poz")
        self.heading("rozmiar", text=naglowek_rozmiar)
        self.heading("ofiary", text=Statek.ORDER)
        self.column("#0", stretch=True, minwidth=70, width=49)
        self.column("statek", stretch=True, minwidth=97, width=49)
        self.column("gdzie", stretch=True, minwidth=35, width=49, anchor=tk.CENTER)
        self.column("rozmiar", stretch=True, minwidth=40, width=49, anchor=tk.E)
        self.column("ofiary", stretch=True, minwidth=12, width=49)

    def powiaz_escape(self):
        """Wiąże callback obsługujący naćiśnięcie ESCAPE."""
        self.bind("<Escape>", self.na_escape)

    # CALLBACK całego drzewa
    def na_escape(self, event=None):
        """Kasuje selekcję."""
        element_id = self.focus()
        if element_id != "":  # jeśli jakiś element był w ogóle wybrany
            self.selection_remove(element_id)


class DrzewoFlotyGracza(DrzewoFloty):
    """
    Pokazuje statki gracza. Kolumny: `Kategoria` (bez nagłówka), `Statek`, `Poz` (pozycja), `NT/R` (pola nietrafione/rozmiar), `★` (ilość gwiazdek = ilość ofiar danego statku).
    """

    def __init__(self, rodzic, plansza_gui):
        super().__init__(rodzic, plansza_gui)

        self.ustaw_kolumny("NT/R")
        self.dodaj_statki(self.plansza_gui.gracz.plansza.niezatopione, "niezatopione")
        self.ustaw_wyglad()
        self.powiaz_podwojne_klikniecie()

    def dodaj_statki(self, statki, kategoria):
        """
        Dodaje podane (niezatopione/zatopione) statki do drzewa. Wartość parametru `kategoria` to albo 'niezatopione' albo 'zatopione'.
        """
        # kategoria
        self.insert("", "0", kategoria,
                    text=kategoria + " (" + str(len(statki)) + ")",
                    open=True,
                    tags="kategoria"
                    )
        # rangi
        ilosc_wg_rang = self.plansza_gui.gracz.plansza.podaj_ilosc_niezatopionych_wg_rang()
        for ranga in Statek.RANGI[::-1]:
            if ilosc_wg_rang[ranga] > 0:
                ranga_i_ilosc = Statek.SYMBOLE[ranga] + " (" + str(ilosc_wg_rang[ranga]) + ")"
                self.insert(kategoria, "end",
                            ranga,
                            text=ranga_i_ilosc,
                            open=True,
                            tags=(kategoria, "ranga")
                            )
        # statki
        for i in range(len(statki)):
            statek = statki[i]
            self.insert(
                statek.RANGA_BAZOWA, "end",
                str(i),  # index listy statków jako ID statku w drzewie - upraszcza późniejszą translację wybranego elementu drzewa z powrotem na statek na planszy. Zamiana na str() wynika z dziwnej obsługi zera (Tkinter zwraca później zamiast zera string 'I001' - prawdopodobnie traktuje podanie zera jako wartości dla ID jako nie podanie niczego i zamiast tego wpisuje wartość defaultową)
                values=(
                    '"' + statek.nazwa + '"',
                    str(statek.polozenie),
                    statek.podaj_nietrafione_na_rozmiar(),
                    "".join([statek.ORDER for ofiara in statek.ofiary])
                ),
                tags=(kategoria, "statek")
            )

    def ustaw_wyglad(self):
        """Konfiguruje wygląd zawartości drzewa."""
        self.tag_configure("kategoria", font=GraGUI.CZCIONKI["mała-pogrubiona"])
        self.tag_configure("ranga", background=self.KOLORY["podświetlenie-rang"])

    def powiaz_podwojne_klikniecie(self):
        """Wiąże callback obsługujący podóœjne kliknięcie."""
        self.tag_bind("statek", "<Double-Button-1>", self.na_podwojne_klikniecie)

    # CALLBACK elementów z tagiem `statek`
    def na_podwojne_klikniecie(self, event=None):
        """Wybiera kliknięty podwójnie statek na planszy gracza."""
        # TODO: w drzewie nie może dać się wybierać statków które już miały swoją rundę w tej turze!
        statek = self.plansza_gui.gracz.tura.statki[int(self.focus())]
        self.plansza_gui.zmien_statek(statek)


class DrzewoFlotyPrzeciwnika(DrzewoFloty):
    """
    Pokazuje zatopione statki przeciwnika. Kolumny: `Kategoria` (bez nagłówka), `Statek`, `Poz` (pozycja), `Roz` (rozmiar), `★` (ilość gwiazdek = ilość ofiar danego statku).
    """

    def __init__(self, rodzic, plansza_gui):
        super().__init__(rodzic, plansza_gui)

        self.ustaw_kolumny("Rozm")

    def dodaj_statek(self):
        """
        Dodaje zatopiony statek przeciwnika. Przy pierwszym dodaniu statku danej rangi tworzy odpowiedni folder rangi.
        """
        pass


class KontrolaGry(Sekcja):
    """
    Sekcja kontroli gry znajdująca się w prawym dolnym rogu głównego interfejsu gry. Dopuszcza powiększanie w poziomie.
    """

    KOLORY = {
        "stan-gry-g": "LemonChiffon4",
        "stan-gry-p": "LemonChiffon4"
    }
    SZER_STANU = 15  # szerokość stanu gry (etykiety) w znakach

    def __init__(self, rodzic, odstep_zewn, odstep_wewn, tytul, **kwargs):
        super().__init__(rodzic, odstep_zewn, odstep_wewn, tytul)
        self.plansza_g = kwargs["plansza_gracza"]
        self.plansza_p = kwargs["plansza_przeciwnika"]
        self.ustaw_style()
        self.ustaw_etyramke()
        self.ustaw_tytul()
        self.buduj_etykiety()
        self.buduj_przycisk()
        self.komunikator = None  # przekazywane przez rodzica

    def ustaw_etyramke(self):
        """Ustawia etyramkę pod widżety."""
        self.etyramka.grid(sticky="we")
        self.etyramka.columnconfigure(0, weight=1)  # zgłasza wyżej powiększanie w poziomie

    def ustaw_tytul(self):
        """Ustawia tytuł sekcji. Format tytułu: Tura #[liczba]/Runda #[liczba]"""
        self.tytul.set(self.plansza_g.gracz.podaj_info_o_rundzie().title())

    def ustaw_style(self):
        """Ustawia style dla sekcji."""
        self.styl = ttk.Style()
        self.styl.configure(
            "GraczKG.TLabel",
            font=GraGUI.CZCIONKI["duża-pogrubiona"],
            # background=GraGUI.KOLORY["pozycja-pola"],
            foreground=self.KOLORY["stan-gry-g"]
        )
        self.styl.configure(
            "PrzeciwnikKG.TLabel",
            font=GraGUI.CZCIONKI["duża-pogrubiona"],
            # background=GraGUI.KOLORY["pozycja-pola"],
            foreground=self.KOLORY["stan-gry-p"]
        )
        self.styl.configure(
            "KG.TButton",
            font=GraGUI.CZCIONKI["pogrubiona"]
        )

    def buduj_etykiety(self):
        """Buduje etykiety stanu gry dla gracza i przeciwnika."""
        # gracz
        etykieta_g = ttk.Label(
            self.etyramka,
            style="Mała.TLabel",
            text=self.plansza_g.tytul.get() + ":"
        ).grid(
            row=0,
            column=0,
            sticky=tk.W,
            padx=(28, 13),
            pady=(0, 5)
        )
        tekst_g = self.podaj_tekst_stanu(self.plansza_g.gracz)
        self.stan_g = ttk.Label(
            self.etyramka,
            style="GraczKG.TLabel",
            text=tekst_g,
            anchor=tk.E,
            width=self.SZER_STANU
        )
        self.stan_g.grid(
            row=0,
            column=1,
            sticky=tk.E,
            padx=(0, 23),
            pady=(0, 5)
        )
        # przeciwnik
        etykieta_p = ttk.Label(
            self.etyramka,
            style="Mała.TLabel",
            text=self.plansza_p.tytul.get() + ":"
        ).grid(
            row=1,
            column=0,
            sticky=tk.W,
            padx=(28, 13),
            pady=(5, 5)
        )
        tekst_p = self.podaj_tekst_stanu(self.plansza_p.gracz)
        self.stan_p = ttk.Label(
            self.etyramka,
            style="PrzeciwnikKG.TLabel",
            text=tekst_p,
            anchor=tk.E,
            width=self.SZER_STANU
        )
        self.stan_p.grid(
            row=1,
            column=1,
            sticky=tk.E,
            padx=(0, 23),
            pady=(5, 5)
        )

    def podaj_tekst_stanu(self, gracz):
        """Podaje tekst stanu gry dla danego gracza."""
        tekst = str(gracz.plansza.podaj_ilosc_nietrafionych_pol()) + "/"
        tekst += str(gracz.plansza.ilosc_pol_statkow) + " ("
        tekst += gracz.plansza.podaj_procent_nietrafionych_pol() + ")"
        return tekst

    def buduj_przycisk(self):
        """Buduje przycisk KONIEC RUNDY."""
        self.koniec_rundy = ttk.Button(
            self.etyramka,
            text="KONIEC RUNDY",
            style="KG.TButton",
            command=self.na_koniec_rundy
        )
        self.koniec_rundy.grid(
            row=2,
            column=1,
            sticky=tk.E,
            padx=(0, 23),
            pady=10
        )

    # CALLBACK przycisku KONIEC RUNDY
    def na_koniec_rundy(self):
        """Kończy rundę."""
        # TODO: ustawienie pozostałych sekcji na początek rundy
        self.plansza_g.kasuj_wybor_statku(self.plansza_g.gracz.tura.runda.statek)
        self.plansza_g.gracz.tura.dodaj_runde()
        self.plansza_p.gracz.tura.dodaj_runde()
        self.plansza_g.wybierz_statek(self.plansza_g.gracz.tura.runda.statek)
        self.ustaw_tytul()
        self.komunikator.o_rundzie(self.plansza_g.gracz)


# *************************************** SEKCJA KOMUNIKATÓW ************************************************


class PasekKomunikatow(ttk.Frame):
    """
    Pasek wyświetlający komunikaty o grze w polu tekstowym na dole głównego interfejsu gry. Dopuszcza powiększanie w pionie.
    """

    def __init__(self, rodzic, odstep, szer_plansz, wys_plansz):
        super().__init__(rodzic, padding=odstep)
        self.szer_plansz, self.wys_plansz = szer_plansz, wys_plansz  # # ilość kolumn, ilość rzędów

        self.sprawdz_tlo_sytemowe()
        self.buduj_pole_tekstowe()
        self.wstaw_suwak()

    def podaj_wysokosc(self):
        """
        Podaje wysokość. Niezbędna wysokość uzależniona jest od wysokości plansz (oraz drzewa w sekcji kontroli floty) i została ustalona po testach.
        """
        wysokosci = {
            8: 17,
            9: 15,
            10: 13,
            11: 11,
            12: 10,
            13: 9,
            14: 8,
            15: 6,
            16: 5,
            17: 5,
            18: 5,
            19: 4,
            20: 5,
            21: 5,
            22: 5,
            23: 4,
            24: 5,
            25: 5,
            26: 5,
            27: 4,
            28: 5,
            29: 5,
            30: 4
        }
        return wysokosci[self.wys_plansz]

    def podaj_szerokosc(self):
        """Podaje szerokość."""
        # z testów wynikło, że dla bazowej szerokości planszy równej 8 kolumn prawidłowa szerokość pola tekstowego to 77 znaków i że z każdą dodatkową kolumną planszy pole powinno rosnąć o 7.5 znaku w szerz
        korekta = round(7.5 * (self.szer_plansz - 8))
        return 77 + korekta

    def buduj_pole_tekstowe(self):
        """Buduje pole tekstowe."""
        self.tekst = ReadonlyText(
            self,
            width=self.podaj_szerokosc(),
            height=self.podaj_wysokosc(),
            font=GraGUI.CZCIONKI["mała"],
            wrap=tk.WORD,
            bg=self.TLO_SYSTEMOWE,
            state=tk.DISABLED
        )
        self.tekst.grid(column=0, row=0, sticky="ns")

    def sprawdz_tlo_sytemowe(self):
        """Sprawdza kolor tla systemowego i zapisuje w stałej"""
        self.TLO_SYSTEMOWE = self.winfo_toplevel().cget("bg")

    def wstaw_suwak(self):
        """Wstawia pionowy suwak."""
        suwak = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tekst.yview)
        suwak.grid(column=1, row=0, sticky="ns")
        self.tekst.configure(yscrollcommand=suwak.set)


class ReadonlyText(tk.Text):
    """
    Pole tekstowe Tkintera zmodyfikowane o metody, które opakowują podstawe metody edycji tak, by nie trzeba było za każdym razem przed edycją przestawiać widżeta w stan `normal` i po edycji w stan `disabled` (co jest konieczne, ponieważ tk.Text nie ma defaultowo trybu readonly, a tylko `normal` i `disabled`, podczas którego nie można nic zmieniać w widżecie, również programistycznie.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<1>", lambda event: self.focus_set())  # to powiązanie przywraca możliwość selekcji tekstu (np. dla skopiowanie) po zablokowaniu (wzięte stąd: https://stackoverflow.com/questions/10817917/how-to-disable-input-to-a-text-widget-but-allow-programatic-input)

    def ro_insert(self, *args, **kwargs):
        """Readonly insert."""
        self.configure(state=tk.NORMAL)
        self.insert(*args, **kwargs)
        self.configure(state=tk.DISABLED)

    def ro_delete(self, *args, **kwargs):
        """Readonly delete."""
        self.configure(state=tk.NORMAL)
        self.delete(*args, **kwargs)
        self.configure(state=tk.DISABLED)


# ******************************************** OKNO GŁÓWNE **************************************************


class GraGUI(ttk.Frame):
    """Główny interfejs gry"""

    CZCIONKI = {
        "mała": ("TkDefaultFont", 8),
        "mała-pogrubiona": ("TkDefaultFont", 8, "bold"),
        "duża-pogrubiona": ("TkDefaultFont", 10, "bold"),
        "pogrubiona": ("TkDefaultFont", 9, "bold")
        # "mała-mono": ("TkFixedFont", 8)
    }
    KOLORY = {
        "pozycja-pola": "LemonChiffon2"
    }

    def __init__(self, rodzic, kolumny, rzedy):
        super().__init__(rodzic)
        self.grid()
        self.ustaw_style()
        gracz = Gracz(Plansza(kolumny, rzedy))
        przeciwnik = Gracz(Plansza(kolumny, rzedy))
        self.buduj_plansze(gracz, przeciwnik)
        self.buduj_sekcje_kontroli()
        self.buduj_pasek_komunikatow()
        self.ustaw_siatke()
        self.wybierz_statek_startowy()
        self.przekaz_komunikator()
        self.wyswietl_komunikaty()


    def ustaw_style(self):
        """Ustawia style dla okna głównego."""
        self.styl = ttk.Style()
        self.styl.configure(
            "Bold.TLabel",
            font=self.CZCIONKI["pogrubiona"]
        )
        self.styl.configure(
            "Mała.TLabel",
            font=GraGUI.CZCIONKI["mała"]
        )

    def buduj_plansze(self, gracz, przeciwnik):
        """Buduje plansze gracza i przeciwnika"""
        self.plansza_g = PlanszaGracza(self, 10, 10, gracz=gracz)
        self.plansza_p = PlanszaPrzeciwnika(self, 10, 10, gracz=przeciwnik)
        self.plansza_p.drugi_gracz = self.plansza_g.gracz

    def buduj_sekcje_kontroli(self):
        """Buduje sekcje kontroli: ataku, floty i gry po prawej stronie okna głównego."""
        self.kontrola_ataku = KontrolaAtaku(
            self,
            (0, 10, 10, 10),  # odstęp zewnętrzny (lewo, góra, prawo, dół)
            (5, 10, 5, 5),  # odstęp wewnętrzny
            plansza_gracza=self.plansza_g,
            plansza_przeciwnika=self.plansza_p
        )
        self.kontrola_floty = KontrolaFloty(
            self,
            (0, 0, 10, 10),
            (5, 7, 5, 13),
            plansza_gracza=self.plansza_g,
            plansza_przeciwnika=self.plansza_p
        )
        self.kontrola_gry = KontrolaGry(
            self,
            (0, 0, 10, 10),
            (5, 10, 5, 5),
            "",
            plansza_gracza=self.plansza_g,
            plansza_przeciwnika=self.plansza_p
        )

    def buduj_pasek_komunikatow(self):
        """Buduje pasek komunikatów na dole okna głównego"""
        self.pasek_komunikatow = PasekKomunikatow(
            self,
            (10, 0, 10, 11),
            self.plansza_g.gracz.plansza.kolumny,
            self.plansza_g.gracz.plansza.rzedy
        )

    def ustaw_siatke(self):
        """
        Konfiguruje layout managera. Dopuszcza powiększanie trzeciej kolumny (w poziomie) i czwartego rzędu (w pionie). Zmienia ustawienia dwóch ostatnich rzędów w zależności od wielkości planszy.
        """
        self.plansza_g.grid(column=0, row=0, rowspan=3, sticky=tk.N)
        self.plansza_p.grid(column=1, row=0, rowspan=3, sticky=tk.N)
        self.kontrola_ataku.grid(column=2, row=0, sticky="nwe")
        self.kontrola_floty.grid(column=2, row=1, sticky="nsew")
        self.kontrola_gry.grid(column=2, row=2, rowspan=2, sticky="nwe")
        self.pasek_komunikatow.grid(column=0, row=3, columnspan=2, sticky="ns")
        # dla plansz mniejszych niż 12 rzędów pasek komunikatów musi zajmować dwa rzędy siatki okna głównego a sekcja kontroli gry jeden (dla większych jest na odwrót)
        if self.plansza_g.gracz.plansza.rzedy < 12:
            self.plansza_g.grid(rowspan=2)
            self.plansza_g.grid(rowspan=2)
            self.kontrola_floty.grid(rowspan=2)
            self.kontrola_gry.grid(row=3, rowspan=1)
            self.pasek_komunikatow.grid(row=2, rowspan=2)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

    def wybierz_statek_startowy(self):
        """Wybiera największy statek na start gry."""
        self.plansza_g.wybierz_statek(self.plansza_g.gracz.plansza.statki[0])
        self.kontrola_floty.drzewo_g.see("niezatopione")

    def przekaz_komunikator(self):
        """Tworzy, ustawia i przekazuje widżetom komunikator."""
        self.komunikator = Komunikator(self.pasek_komunikatow.tekst, self.CZCIONKI, PoleGUI.KOLORY)
        self.plansza_p.komunikator = self.komunikator
        self.kontrola_gry.komunikator = self.komunikator

    def wyswietl_komunikaty(self):
        """Wyświetla komunikaty w polu tekstowym paska komunikatów."""
        self.komunikator.o_rozpoczeciu_gry(self.plansza_g.gracz.plansza)
        self.komunikator.o_rundzie(self.plansza_g.gracz)


def main():
    """Uruchamia grę."""
    okno_glowne = tk.Tk()
    okno_glowne.title("Statki")

    GraGUI(okno_glowne, 15, 15)  # dopuszczalny rozmiar planszy: 8-26 kolumn x 8-30 rzędów

    okno_glowne.resizable(False, False)
    okno_glowne.mainloop()


if __name__ == "__main__":
    main()
