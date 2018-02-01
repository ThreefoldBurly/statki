#!/usr/bin/env python3

"""
Graficzny interfejs użytkownika
"""

import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

from plansza import Plansza, Pole
from mechanika import Gracz


class PoleGUI(ttk.Button):
    """Graficzna reprezentacja pola planszy."""

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
        "nieodkryte-active": "DarkSeaGreen1"
    }
    STYLE = {
        "woda": "Woda.TButton",
        "pudło": "Pudło.TButton",
        "trafione": "Trafione.TButton",
        "zatopione": "Zatopione.TButton",
        "wybrane": "Wybrane.TButton",
        "wybrane&trafione": "Wybrane&Trafione.TButton"
    }

    def __init__(self, rodzic, pole, *args, **kwargs):
        super().__init__(rodzic, *args, **kwargs)
        self.pole = pole


class PlanszaGUI(ttk.Frame):
    """Graficzna reprezentacja planszy - szczegółowa implementacja w klasach potomnych."""

    def __init__(self, rodzic, gracz, tytul):
        super().__init__(rodzic, padding=10)
        self.gracz = gracz
        self.tytul = tytul
        self.pola_gui = [[0 for kolumna in range(self.gracz.plansza.kolumny)] for rzad in range(self.gracz.plansza.rzedy)]  # matryca (lista rzędów (list)) obiektów klasy PoleGUI (tu inicjalizowanych jako "0")

        self.ustaw_style()
        self.ustaw_sie()
        self.buduj_etykiety()
        self.buduj_pola()

    def ustaw_sie(self):
        """Ustawia interfejs pod widżety."""
        self.grid(rowspan=3)
        self.etyramka = ttk.LabelFrame(self, text=self.tytul, padding=10)
        self.etyramka.grid()

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

    def zatop_statek(self, statek, symbole=False):
        """Oznacza pola wskazanego statku jako zatopione."""
        for pole in statek.pola:
            pole.znacznik = Pole.ZNACZNIKI["zatopione"]
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            pole_gui.configure(style=PoleGUI.STYLE["zatopione"])
            if symbole:
                pole_gui.configure(text=statek.SYMBOL)

        self.gracz.plansza.zatopione.append(statek)
        self.gracz.plansza.niezatopione.remove(statek)


class PlanszaGracza(PlanszaGUI):
    """Graficzna reprezentacja planszy gracza."""

    def __init__(self, rodzic, plansza, tytul="Gracz"):
        super().__init__(rodzic, plansza, tytul)
        self.kontrola_ataku = None  # Kontrola Ataku przekazuje tutaj odnośnik do siebie na koniec swojej inicjalizacji
        self.ustaw_style_gracza()
        self.rejestruj_callback()
        self.odkryj_wszystkie_pola()

        # testy
        # self.oznacz_pudlo(self.podaj_pole_gui(5, 5))
        statek = self.gracz.plansza.statki[2]
        self.oznacz_trafione(self.podaj_pole_gui(*statek.polozenie.podaj_wspolrzedne()))
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

    def rejestruj_callback(self):
        """Rejestruje callback na_klikniecie() we wszystkich polach."""
        for i in range(self.gracz.plansza.kolumny):
            for j in range(self.gracz.plansza.rzedy):
                kolumna, rzad = i + 1, j + 1
                # lambda bez własnych argumentów (w formie: lambda: self.na_klikniecie(kolumna, rzad) nie zadziała prawidłowo w tym przypadku - zmienne przekazywane do każdej funkcji (anonimowej czy nie - bez różnicy) są zawsze ewaluowane dopiero w momencie wywołania tej funkcji, tak więc w tym przypadku w danej iteracji pętli zostają przekazane zmienne "i" i "j" (nazwy) a nie ich wartości - wartości zostaną ewaluowane dopiero w momencie wywołania callbacka (czyli naciśnięcia przycisku) i będzie to wartość z ostatniej iteracji dla wszystkich przycisków, więcej tutaj: https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture/23557126))
                pole_gui = self.podaj_pole_gui(kolumna, rzad)
                pole_gui.configure(command=lambda x=kolumna, y=rzad: self.na_klikniecie(x, y))  # lambda konieczna, bo nie da się tego obsłużyć tak jak niżej z bind() - w przypadku przypisywania callbacków opcją 'command' nie ma przekazywania obiektu zdarzenia, z którego można by pobrać współrzędne pola

    def na_klikniecie(self, kolumna, rzad):
        """
        Callback każdego pola uruchamiany po naciśnięciu. Wybiera kliknięty statek, kasując wybór poprzedniego. Zatopione statki nie są wybierane. Ten sam mechanizm jest uruchamiany po wyborze statku w sekcji Kontroli Ataku.
        """
        statek = self.gracz.plansza.podaj_statek(self.podaj_pole_gui(kolumna, rzad).pole)
        self.zmien_statek(statek)

        print("Kliknięcie w polu: ({}{})".format(Plansza.ALFABET[kolumna], rzad))  # test

    def zmien_statek(self, statek):
        """Zmienia wybrany statek"""
        if statek and not statek.czy_zatopiony():
            stary_statek = self.gracz.tura.runda.statek
            if stary_statek:
                self.kasuj_wybor_statku(stary_statek)
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
        self.kontrola_ataku.combo_statku.set(statek)
        self.kontrola_ataku.ustaw_salwy(statek)

    def kasuj_wybor_statku(self, statek):
        """Kasuje wybór statku na planszy"""
        for pole in statek.pola:
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            if pole_gui.pole.znacznik == Pole.ZNACZNIKI["trafione"]:
                pole_gui.configure(style=PoleGUI.STYLE["trafione"])
            else:
                pole_gui.configure(style="TButton")

    def oznacz_trafione(self, pole_gui):
        """Oznacza podane pole jako trafione."""
        pole_gui.pole.znacznik = Pole.ZNACZNIKI["trafione"]
        pole_gui.configure(style=PoleGUI.STYLE["trafione"])

    def odkryj_wszystkie_pola(self):
        """Odkrywa wszystkie pola planszy."""
        for rzad in self.pola_gui:
            for pole_gui in rzad:
                statek = self.gracz.plansza.podaj_statek(pole_gui.pole)
                if pole_gui.pole.znacznik in (Pole.ZNACZNIKI["puste"], Pole.ZNACZNIKI["obwiednia"]):
                    pole_gui.configure(style=PoleGUI.STYLE["woda"])
                else:
                    pole_gui.configure(text=statek.SYMBOL)


class PlanszaPrzeciwnika(PlanszaGUI):
    """Graficzna reprezentacja planszy przeciwnika."""

    def __init__(self, rodzic, plansza, tytul="Przeciwnik"):
        super().__init__(rodzic, plansza, tytul)
        self.orientacja_ataku = None  # zmieniane przez event (pierwszy wybór statku)

        self.ustaw_style_przeciwnika()
        self.rejestruj_callbacki()
        # test
        # self.orientacja_ataku = KontrolaAtaku.ORIENTACJE[0]

    def ustaw_style_przeciwnika(self):
        """Definiuje style dla pól."""
        # nieodkryte
        self.styl.map(
            "Nieodkryte.TButton",
            background=[("active", PoleGUI.KOLORY["nieodkryte-active"])]
        )

    def zmien_podswietlanie_nieodkrytych(self):
        """Zmienia podświetlanie nieodkrytych pól na odpowiedni kolor."""
        for rzad in self.pola_gui:
            for pole_gui in rzad:
                pole_gui.configure(styl="Nieodkryte.TButton")

    def rejestruj_callbacki(self):
        """Rejestruje callbacki na_klikniecie(), na_wejscie() i na_wyjscie() we wszystkich polach."""
        for i in range(self.gracz.plansza.kolumny):
            for j in range(self.gracz.plansza.rzedy):
                kolumna, rzad = i + 1, j + 1
                pole_gui = self.podaj_pole_gui(kolumna, rzad)
                pole_gui.configure(command=lambda x=kolumna, y=rzad: self.na_klikniecie(x, y))
                pole_gui.bind("<Enter>", self.na_wejscie)
                pole_gui.bind("<Leave>", self.na_wyjscie)

    def na_klikniecie(self, kolumna, rzad):
        """
        Callback każdego pola uruchamiany po naciśnięciu. W zależności od 9-stanowej flagi 'orientacja_ataku' odkrywa na planszy odpowiednie pola (lub pole).
        """
        if self.orientacja_ataku:
            self.odkryj_pole(kolumna, rzad)
            if self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[1]:
                self.odkryj_pole(kolumna + 1, rzad)

            elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[2]:
                self.odkryj_pole(kolumna, rzad + 1)

            elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[3]:
                self.odkryj_pole(kolumna - 1, rzad)
                self.odkryj_pole(kolumna + 1, rzad)

            elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[4]:
                self.odkryj_pole(kolumna, rzad - 1)
                self.odkryj_pole(kolumna, rzad + 1)

            elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[5]:
                self.odkryj_pole(kolumna, rzad - 1)
                self.odkryj_pole(kolumna + 1, rzad)

            elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[6]:
                self.odkryj_pole(kolumna, rzad + 1)
                self.odkryj_pole(kolumna + 1, rzad)

            elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[7]:
                self.odkryj_pole(kolumna - 1, rzad)
                self.odkryj_pole(kolumna, rzad + 1)

            elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[8]:
                self.odkryj_pole(kolumna - 1, rzad)
                self.odkryj_pole(kolumna, rzad - 1)

        print("Kliknięcie w polu: ({}{})".format(Plansza.ALFABET[kolumna], rzad))  # test

    def odkryj_pole(self, kolumna, rzad):
        """Odkrywa na planszy pole wg podanych współrzędnych. Zaznacza pudło lub trafienie. Zatapia trafiony statek (i odkrywa pola jego obwiedni), jeśli trzeba."""
        if self.gracz.plansza.czy_pole_w_planszy(kolumna, rzad):
            pole_gui = self.podaj_pole_gui(kolumna, rzad)
            if pole_gui.pole.znacznik in (Pole.ZNACZNIKI["puste"], Pole.ZNACZNIKI["obwiednia"]):
                self.oznacz_pudlo(pole_gui)
            elif pole_gui.pole.znacznik == Pole.ZNACZNIKI["statek"]:
                pole_gui.pole.znacznik = Pole.ZNACZNIKI["trafione"]
                pole_gui.configure(style=PoleGUI.STYLE["trafione"], text=PoleGUI.GLIFY["trafione"])
                statek = self.gracz.plansza.podaj_statek(pole_gui.pole)
                if statek.czy_zatopiony():
                    self.zatop_statek(statek, symbole=True)
                    self.odkryj_obwiednie(statek)

    def odkryj_obwiednie(self, statek):
        """Odkrywa na planszy obwiednie zatopionego statku."""
        for pole in statek.obwiednia:
            # configure("style") zwraca krotkę, której ostatnim elementem jest nazwa stylu
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            if pole_gui.configure("style")[-1] not in (PoleGUI.STYLE["woda"], PoleGUI.STYLE["pudło"]):
                pole_gui.configure(style=PoleGUI.STYLE["woda"])
        # test
        print(statek.o_zatopieniu())

    def na_wejscie(self, event):
        """
        Callback każdego pola uruchamiany po wejściu kursora w obręb pola. W zależności od 9-stanowej flagi 'orientacja_ataku' podświetla lub nie dodatkowe, sąsiednie pola w odpowiedniej konfiguracji.
        """
        kolumna, rzad = event.widget.pole.podaj_wspolrzedne()
        if self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[1]:
            self.zmien_stan_pola(kolumna + 1, rzad, "active")

        elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[2]:
            self.zmien_stan_pola(kolumna, rzad + 1, "active")

        elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[3]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active")
            self.zmien_stan_pola(kolumna + 1, rzad, "active")

        elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[4]:
            self.zmien_stan_pola(kolumna, rzad - 1, "active")
            self.zmien_stan_pola(kolumna, rzad + 1, "active")

        elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[5]:
            self.zmien_stan_pola(kolumna, rzad - 1, "active")
            self.zmien_stan_pola(kolumna + 1, rzad, "active")

        elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[6]:
            self.zmien_stan_pola(kolumna, rzad + 1, "active")
            self.zmien_stan_pola(kolumna + 1, rzad, "active")

        elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[7]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active")
            self.zmien_stan_pola(kolumna, rzad + 1, "active")

        elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[8]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active")
            self.zmien_stan_pola(kolumna, rzad - 1, "active")

    def na_wyjscie(self, event):
        """
        Callback każdego pola uruchamiany po wyjściu kursora z obrębu pola. W zależności od 9-stanowej flagi 'orientacja_ataku' kasuje podświetlenie dodatkowych, sąsiednich pól (lub pola) wywołane wcześniej odpaleniem callbacka na_wejscie().
        """
        kolumna, rzad = event.widget.pole.podaj_wspolrzedne()
        if self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[1]:
            self.zmien_stan_pola(kolumna + 1, rzad, "!active")

        elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[2]:
            self.zmien_stan_pola(kolumna, rzad + 1, "!active")

        elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[3]:
            self.zmien_stan_pola(kolumna - 1, rzad, "!active")
            self.zmien_stan_pola(kolumna + 1, rzad, "!active")

        elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[4]:
            self.zmien_stan_pola(kolumna, rzad - 1, "!active")
            self.zmien_stan_pola(kolumna, rzad + 1, "!active")

        elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[5]:
            self.zmien_stan_pola(kolumna, rzad - 1, "!active")
            self.zmien_stan_pola(kolumna + 1, rzad, "!active")

        elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[6]:
            self.zmien_stan_pola(kolumna, rzad + 1, "!active")
            self.zmien_stan_pola(kolumna + 1, rzad, "!active")

        elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[7]:
            self.zmien_stan_pola(kolumna - 1, rzad, "!active")
            self.zmien_stan_pola(kolumna, rzad + 1, "!active")

        elif self.orientacja_ataku == KontrolaAtaku.ORIENTACJE[8]:
            self.zmien_stan_pola(kolumna - 1, rzad, "!active")
            self.zmien_stan_pola(kolumna, rzad - 1, "!active")

    def zmien_stan_pola(self, kolumna, rzad, stan):
        """Zmienia stan pola wg podanych współrzędnych."""
        if self.gracz.plansza.czy_pole_w_planszy(kolumna, rzad):
            self.podaj_pole_gui(kolumna, rzad).state([stan])


class KontrolaAtaku(ttk.Frame):
    """
    Graficzna reprezentacja sekcji kontroli ataku znajdującej się w prawym górnym rogu głównego interfejsu gry.
    """

    ORIENTACJE = ["•", "••", "||", "•••", "|||", "L", "Г", "˥", "⅃"]

    def __init__(self, rodzic, plansza_gracza, plansza_przeciwnika):
        super().__init__(rodzic, padding=(0, 0, 10, 0))
        self.plansza_g = plansza_gracza
        self.plansza_p = plansza_przeciwnika

        self.ustaw_style()
        self.ustaw_sie()
        self.buduj_etykiety()
        self.buduj_comboboksy()

        self.plansza_g.kontrola_ataku = self  # przekazanie do planszy dla jej event handlerów

    def ustaw_style(self):
        """Ustawia style dla widżetów"""
        self.styl = ttk.Style()
        # etykiety
        self.styl.configure(
            "KA.TLabel",
            font=("TkDefaultFont", 8)
        )
        # comboboksy
        self.styl.configure(
            "KA.TCombobox",
            font=("TkDefaultFont", 8)
        )
        self.styl.map(
            "KA.TCombobox",
            fieldbackground=[("readonly", "white")]
        )

    def ustaw_sie(self):
        """Ustawia interfejs pod widżety."""
        self.grid()
        self.etyramka = ttk.Labelframe(self, text="Atak", padding=5)
        self.etyramka.grid()

    def buduj_etykiety(self):
        """Buduje etykiety."""
        ttk.Label(
            self.etyramka,
            text="Wybierz statek:",
            style="KA.TLabel"
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky=tk.W
        )
        ttk.Label(
            self.etyramka,
            text="Wybierz salwę:",
            style="KA.TLabel"
        ).grid(
            row=2,
            column=0,
            sticky=tk.W,
            pady=(5, 0)
        )
        ttk.Label(
            self.etyramka,
            text="Wybierz orientację:",
            style="KA.TLabel"
        ).grid(
            row=2,
            column=1,
            sticky=tk.W,
            pady=(5, 0)
        )

    def buduj_comboboksy(self):
        """Buduje comboboksy."""
        # wybór statku
        self.combo_statku = ttk.Combobox(
            self.etyramka,
            styl="KA.TCombobox",
            values=self.plansza_g.gracz.tura.statki,
            width=30
        )
        self.combo_statku.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=tk.W
        )
        self.combo_statku.configure(font=("TkDefaultFont", 8))  # to zmienia tylko czcionkę pola tekstowego (Entry), które jest częścią comboboksa
        self.combo_statku.state(["readonly"])
        self.combo_statku.bind("<<ComboboxSelected>>", self.na_wybor_statku)

        # wybór salwy
        self.combo_salwy = ttk.Combobox(
            self.etyramka,
            styl="KA.TCombobox",
            width=6
        )
        self.combo_salwy.grid(
            row=3,
            column=0,
            sticky=tk.W,
            pady=(0, 10)
        )
        self.combo_salwy.configure(font=("TkDefaultFont", 8))
        self.combo_salwy.state(["readonly"])
        self.combo_salwy.bind("<<ComboboxSelected>>", self.na_wybor_salwy)

        # wybór orientacji
        self.combo_orientacji = ttk.Combobox(
            self.etyramka,
            styl="KA.TCombobox",
            width=4
        )
        self.combo_orientacji.grid(
            row=3,
            column=1,
            sticky=tk.W,
            pady=(0, 10)
        )
        self.combo_orientacji.configure(font=("TkDefaultFont", 8))
        self.combo_orientacji.state(["readonly"])
        self.combo_orientacji.bind("<<ComboboxSelected>>", self.na_wybor_orientacji)

    def na_wybor_statku(self, event=None):
        """Callback comboboksa wyboru statku uruchamiany po zmianie selekcji."""
        event.widget.selection_clear()  # czyści tło pola tekstowego comboboksa
        indeks = event.widget.current()
        wybrany_statek = self.plansza_g.gracz.tura.statki[indeks]
        self.plansza_g.zmien_statek(wybrany_statek)  # plansza aktualizuje obiekt rundy
        self.ustaw_salwy(wybrany_statek)

    def na_wybor_salwy(self, event=None):
        """Callback comboboksa wyboru salwy uruchamiany po zmianie selekcji."""
        event.widget.selection_clear()
        self.ustaw_orientacje(event.widget.get())

    def na_wybor_orientacji(self, event=None):
        """Callback comboboksa wyboru salwy uruchamiany po zmianie selekcji."""
        event.widget.selection_clear()
        self.plansza_p.orientacja_ataku = event.widget.get()

    def ustaw_salwy(self, statek):
        """Ustawia salwy wybranego statku"""
        self.combo_salwy["values"] = ["{} pole".format(salwa) if salwa == 1 else "{} pola".format(salwa) for salwa in statek.salwy]
        self.combo_salwy.set(self.combo_salwy["values"][0])
        self.ustaw_orientacje(self.combo_salwy["values"][0])

    def ustaw_orientacje(self, salwa_tekst):
        """Ustawia orientacje wybranej salwy"""
        if not self.plansza_g.gracz.tura.runda.salwy:  # inicjalizacja listy salw w rundzie
            self.plansza_g.gracz.tura.runda.salwy = self.plansza_g.gracz.tura.runda.statek
        salwa = int(salwa_tekst[0])
        if salwa == 1:
            self.combo_orientacji["values"] = [self.ORIENTACJE[0]]
        elif salwa == 2:
            self.combo_orientacji["values"] = self.ORIENTACJE[1:3]
        elif salwa == 3:
            self.combo_orientacji["values"] = self.ORIENTACJE[3:]
        self.combo_orientacji.set(self.combo_orientacji["values"][0])
        # plansza przeciwnika
        if not self.plansza_p.orientacja_ataku:
            self.plansza_p.zmien_podswietlanie_nieodkrytych()
        self.plansza_p.orientacja_ataku = self.combo_orientacji["values"][0]


class KontrolaFloty(ttk.Frame):
    """
    Graficzna reprezentacja sekcji kontroli floty znajdującej się w środku po prawej stronie głównego interfejsu gry.
    """

    def __init__(self, rodzic, plansza_gracza, plansza_przeciwnika):
        super().__init__(rodzic, padding=(0, 0, 10, 0))
        self.plansza_g = plansza_gracza
        self.plansza_p = plansza_przeciwnika
        # GUI
        self.grid()
        etyramka = ttk.Labelframe(self, text="Flota", padding=5)
        etyramka.grid()
        pass  # TODO


class KontrolaGry(ttk.Frame):
    """
    Graficzna reprezentacja sekcji kontroli gry znajdującej się w prawym dolnym rogu głównego interfejsu gry.
    """

    def __init__(self, rodzic, plansza_gracza, plansza_przeciwnika):
        super().__init__(rodzic, padding=(0, 0, 10, 0))
        self.plansza_g = plansza_gracza
        self.plansza_p = plansza_przeciwnika
        # GUI
        self.tytul = None  # string w formacie `Tura #[liczba]/Runda #[liczba]`
        self.grid()
        etyramka = ttk.Labelframe(self, text=self.tytul, padding=5)
        etyramka.grid()
        pass  # TODO


class PasekStanu(ttk.Frame):
    """
    Graficzna reprezentacja paska stanu wyświetlającego komunikaty o grze na dole głównego interfejsu gry.
    """

    def __init__(self, rodzic, plansza_gracza, plansza_przeciwnika):
        super().__init__(rodzic, padding=10)
        self.plansza_g = plansza_gracza
        self.plansza_p = plansza_przeciwnika
        # GUI
        self.grid(columnspan=3)
        pass  # TODO


class GraGUI(ttk.Frame):
    """Graficzna reprezentacja głównego interfejsu gry"""

    def __init__(self, rodzic, kolumny, rzedy):
        super().__init__(rodzic)
        self.grid()

        gracz = Gracz(Plansza(kolumny, rzedy))
        przeciwnik = Gracz(Plansza(kolumny, rzedy))

        plansza_gracza = PlanszaGracza(self, gracz)
        plansza_gracza.grid(column=0, row=0)
        plansza_przeciwnika = PlanszaPrzeciwnika(self, przeciwnik)
        plansza_przeciwnika.grid(column=1, row=0)

        # kontrolna sekcja po prawej stronie
        kontrola_ataku = KontrolaAtaku(self, plansza_gracza, plansza_przeciwnika)
        kontrola_ataku.grid(column=3, row=0)
        kontrola_floty = KontrolaFloty(self, plansza_gracza, plansza_przeciwnika)
        kontrola_floty.grid(column=3, row=1)
        kontrola_gry = KontrolaGry(self, plansza_gracza, plansza_przeciwnika)
        kontrola_gry.grid(column=3, row=2)

        # sekcja komunikatów na dole okna
        pasek_stanu = PasekStanu(self, plansza_gracza, plansza_przeciwnika)
        pasek_stanu.grid(column=0, row=3)


def main():
    """Uruchamia skrypt."""
    root = tk.Tk()
    root.title("Statki")
    # zmiana rozmiaru fontu we wszystkich comboboksach aplikacji
    # brzydki hack stąd: https://stackoverflow.com/questions/43086378/how-to-modify-ttk-combobox-fonts
    # na poziomie pojedynczego widżeta się tego zrobić nie da
    # co ciekawe nawet delegowanie tego kodu do osobnej funkcji powoduje, że hack przestaje działać
    fnt = tkfont.Font(family="TkDefaultFont", size=8)
    root.option_add("*TCombobox*Listbox.font", fnt)

    GraGUI(root, 26, 30)

    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
