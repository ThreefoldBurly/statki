#!/usr/bin/env python3

"""
Graficzny interfejs użytkownika
"""

import tkinter as tk
from tkinter import ttk

from plansza import Plansza, Pole, Statek
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
        self.grid(rowspan=10)
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
                pole_gui.configure(text=statek.SYMBOLE[statek.RANGA])

        self.gracz.plansza.zatopione.append(statek)
        self.gracz.plansza.niezatopione.remove(statek)


class PlanszaGracza(PlanszaGUI):
    """Graficzna reprezentacja planszy gracza."""

    def __init__(self, rodzic, plansza, tytul="Gracz"):
        super().__init__(rodzic, plansza, tytul)
        self.kontrola_ataku = None  # Kontrola Ataku przekazuje tutaj odnośnik do siebie na koniec swojej inicjalizacji
        self.ustaw_style_gracza()
        self.powiaz_callback()
        self.odkryj_wszystkie_pola()

        # testy
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

    def powiaz_callback(self):
        """Wiąże na_klikniecie() we wszystkich polach."""
        for i in range(self.gracz.plansza.kolumny):
            for j in range(self.gracz.plansza.rzedy):
                kolumna, rzad = i + 1, j + 1
                # lambda bez własnych argumentów (w formie: lambda: self.na_klikniecie(kolumna, rzad) nie zadziała prawidłowo w tym przypadku - zmienne przekazywane do każdej funkcji (anonimowej czy nie - bez różnicy) są zawsze ewaluowane dopiero w momencie wywołania tej funkcji, tak więc w tym przypadku w danej iteracji pętli zostają przekazane zmienne "i" i "j" (nazwy) a nie ich wartości - wartości zostaną ewaluowane dopiero w momencie wywołania callbacka (czyli naciśnięcia przycisku) i będzie to wartość z ostatniej iteracji dla wszystkich przycisków, więcej tutaj: https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture/23557126))
                pole_gui = self.podaj_pole_gui(kolumna, rzad)
                pole_gui.configure(command=lambda x=kolumna, y=rzad: self.na_klikniecie(x, y))  # lambda konieczna, bo nie da się tego obsłużyć tak jak niżej z bind() - w przypadku przypisywania callbacków opcją 'command' nie ma przekazywania obiektu zdarzenia, z którego można by pobrać współrzędne pola

    # CALLBACK wszystkich pól
    def na_klikniecie(self, kolumna, rzad):
        """
        Wybiera kliknięty statek, kasując wybór poprzedniego. Zatopione statki nie są wybierane. Ten sam mechanizm jest uruchamiany po wyborze statku w sekcji Kontroli Ataku.
        """
        statek = self.gracz.plansza.podaj_statek(self.podaj_pole_gui(kolumna, rzad).pole)
        self.zmien_statek(statek)

        print("Kliknięcie w polu: ({}{})".format(Plansza.ALFABET[kolumna], rzad))  # test

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
        self.kontrola_ataku.combo_statku.set(statek)
        self.kontrola_ataku.zmien_salwy(statek)

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
                    pole_gui.configure(text=statek.SYMBOLE[statek.RANGA])


class PlanszaPrzeciwnika(PlanszaGUI):
    """Graficzna reprezentacja planszy przeciwnika."""

    def __init__(self, rodzic, plansza, tytul="Przeciwnik"):
        super().__init__(rodzic, plansza, tytul)
        self.combo_orientacji = None  # widżet przekazywany przez Kontrolę Ataku pod koniec jej inicjalizacji
        self.ustaw_style_przeciwnika()
        self.powiaz_callbacki()
        self.zmien_podswietlanie_nieodkrytych()

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
        W zależności od wybranej orientacji w Kontroli Ataku odkrywa na planszy odpowiednie pola (lub pole).
        """
        self.odkryj_pole(kolumna, rzad)
        if self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[1]:
            self.odkryj_pole(kolumna + 1, rzad)

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[2]:
            self.odkryj_pole(kolumna, rzad + 1)

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[3]:
            self.odkryj_pole(kolumna - 1, rzad)
            self.odkryj_pole(kolumna + 1, rzad)

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[4]:
            self.odkryj_pole(kolumna, rzad - 1)
            self.odkryj_pole(kolumna, rzad + 1)

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[5]:
            self.odkryj_pole(kolumna, rzad - 1)
            self.odkryj_pole(kolumna + 1, rzad)

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[6]:
            self.odkryj_pole(kolumna, rzad + 1)
            self.odkryj_pole(kolumna + 1, rzad)

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[7]:
            self.odkryj_pole(kolumna - 1, rzad)
            self.odkryj_pole(kolumna, rzad + 1)

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[8]:
            self.odkryj_pole(kolumna - 1, rzad)
            self.odkryj_pole(kolumna, rzad - 1)

        print("Kliknięcie w polu: ({}{})".format(Plansza.ALFABET[kolumna], rzad))  # test

    # CALLBACK wszustkich pól
    def na_wejscie(self, event):
        """
        W zależności od wybranej orientacji w Kontroli Ataku podświetla lub nie dodatkowe, sąsiednie pola w odpowiedniej konfiguracji.
        """
        kolumna, rzad = event.widget.pole.podaj_wspolrzedne()
        if self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[1]:
            self.zmien_stan_pola(kolumna + 1, rzad, "active")

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[2]:
            self.zmien_stan_pola(kolumna, rzad + 1, "active")

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[3]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active")
            self.zmien_stan_pola(kolumna + 1, rzad, "active")

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[4]:
            self.zmien_stan_pola(kolumna, rzad - 1, "active")
            self.zmien_stan_pola(kolumna, rzad + 1, "active")

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[5]:
            self.zmien_stan_pola(kolumna, rzad - 1, "active")
            self.zmien_stan_pola(kolumna + 1, rzad, "active")

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[6]:
            self.zmien_stan_pola(kolumna, rzad + 1, "active")
            self.zmien_stan_pola(kolumna + 1, rzad, "active")

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[7]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active")
            self.zmien_stan_pola(kolumna, rzad + 1, "active")

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[8]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active")
            self.zmien_stan_pola(kolumna, rzad - 1, "active")

    # CALLBACK wszystkich pól
    def na_wyjscie(self, event):
        """
        W zależności od wybranej orientacji w Kontroli Ataku kasuje podświetlenie dodatkowych, sąsiednich pól (lub pola) wywołane wcześniejszym uruchomieniem callbacka `na_wejscie()`.
        """
        kolumna, rzad = event.widget.pole.podaj_wspolrzedne()
        if self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[1]:
            self.zmien_stan_pola(kolumna + 1, rzad, "!active")

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[2]:
            self.zmien_stan_pola(kolumna, rzad + 1, "!active")

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[3]:
            self.zmien_stan_pola(kolumna - 1, rzad, "!active")
            self.zmien_stan_pola(kolumna + 1, rzad, "!active")

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[4]:
            self.zmien_stan_pola(kolumna, rzad - 1, "!active")
            self.zmien_stan_pola(kolumna, rzad + 1, "!active")

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[5]:
            self.zmien_stan_pola(kolumna, rzad - 1, "!active")
            self.zmien_stan_pola(kolumna + 1, rzad, "!active")

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[6]:
            self.zmien_stan_pola(kolumna, rzad + 1, "!active")
            self.zmien_stan_pola(kolumna + 1, rzad, "!active")

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[7]:
            self.zmien_stan_pola(kolumna - 1, rzad, "!active")
            self.zmien_stan_pola(kolumna, rzad + 1, "!active")

        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[8]:
            self.zmien_stan_pola(kolumna - 1, rzad, "!active")
            self.zmien_stan_pola(kolumna, rzad - 1, "!active")

    def zmien_stan_pola(self, kolumna, rzad, stan):
        """Zmienia stan pola wg podanych współrzędnych."""
        if self.gracz.plansza.czy_pole_w_planszy(kolumna, rzad):
            self.podaj_pole_gui(kolumna, rzad).state([stan])

    def odkryj_pole(self, kolumna, rzad):
        """Odkrywa na planszy pole wg podanych współrzędnych. Zaznacza pudło lub trafienie. Jeśli trzeba, zatapia trafiony statek (i odkrywa pola jego obwiedni)."""
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
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            # configure("style") zwraca krotkę, której ostatnim elementem jest nazwa stylu
            if pole_gui.configure("style")[-1] not in (PoleGUI.STYLE["woda"], PoleGUI.STYLE["pudło"]):
                pole_gui.configure(style=PoleGUI.STYLE["woda"])
        # test
        print(statek.o_zatopieniu())


class KontrolaAtaku(ttk.Frame):
    """
    Sekcja kontroli ataku znajdująca się w prawym górnym rogu głównego interfejsu gry.
    """
    # TODO: rozważyć zaimplementowania 4 orientacji dla salwy 2-polowej (tak by można nią było obracać we wszystkich kierunkach dookoła centralnego pola, tak jak to jest w przypadku salyw 3-polowej)

    ORIENTACJE = ["•", "••", "╏", "•••", "┇", "L", "Г", "Ꞁ", "⅃"]

    def __init__(self, rodzic, plansza_gracza, plansza_przeciwnika):
        super().__init__(rodzic, padding=(0, 10, 10, 0))
        self.plansza_g = plansza_gracza
        self.plansza_p = plansza_przeciwnika
        self.ustaw_style()
        self.ustaw_sie()
        self.buduj_etykiety()
        self.buduj_comboboksy()
        self.ustaw_combo_readonly()
        self.przekaz_odnosniki()
        self.powiaz_callbacki()
        self.wybierz_statek_startowy()

    def ustaw_style(self):
        """Ustawia style dla widżetów"""
        self.styl = ttk.Style()
        # etykiety
        self.styl.configure(
            "KA.TLabel",
            font=GraGUI.CZCIONKA
        )
        # comboboksy
        self.styl.configure("KA.TCombobox")
        self.styl.map(
            "KA.TCombobox",
            fieldbackground=[("readonly", "white")]
        )

    def ustaw_sie(self):
        """Ustawia interfejs pod widżety."""
        self.etyramka = ttk.Labelframe(self, text="Atak", padding=(5, 15, 5, 5))
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
        self.combo_statku = ComboAtaku(
            self.etyramka,
            styl="KA.TCombobox",
            font=GraGUI.CZCIONKA,
            values=self.plansza_g.gracz.tura.statki,
            width=36
        )
        self.combo_statku.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=tk.W
        )
        self.combo_statku.configure(font=GraGUI.CZCIONKA)  # to zmienia tylko czcionkę pola tekstowego (Entry), które jest częścią comboboksa

        # wybór salwy
        self.combo_salwy = ComboAtaku(
            self.etyramka,
            styl="KA.TCombobox",
            font=GraGUI.CZCIONKA,
            width=6
        )
        self.combo_salwy.grid(
            row=3,
            column=0,
            sticky=tk.W,
            pady=(0, 10)
        )
        self.combo_salwy.configure(font=GraGUI.CZCIONKA)

        # wybór orientacji
        self.combo_orientacji = ComboAtaku(
            self.etyramka,
            styl="KA.TCombobox",
            font=GraGUI.CZCIONKA,
            width=4
        )
        self.combo_orientacji.grid(
            row=3,
            column=1,
            sticky=tk.W,
            pady=(0, 10)
        )
        self.combo_orientacji.configure(font=GraGUI.CZCIONKA)

    def ustaw_combo_readonly(self):
        """Ustawia stan comboboksów jako `readonly`"""
        self.combo_statku.state(["readonly"])
        self.combo_salwy.state(["readonly"])
        self.combo_orientacji.state(["readonly"])

    def przekaz_odnosniki(self):
        """Przekazuje własne odnośniki do event handlerów w planszach"""
        self.plansza_g.kontrola_ataku = self
        self.plansza_p.combo_orientacji = self.combo_orientacji

    def wybierz_statek_startowy(self):
        """Wybiera największy statek na start gry"""
        self.plansza_g.wybierz_statek(self.plansza_g.gracz.plansza.statki[0])

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
        elif salwa == 2:
            self.combo_orientacji["values"] = self.ORIENTACJE[1:3]
        elif salwa == 3:
            self.combo_orientacji["values"] = self.ORIENTACJE[3:]
        self.combo_orientacji.set(self.combo_orientacji["values"][0])

    # CALLBACK okna głównego
    def na_prawy_przycisk_myszy(self, event=None):
        """Rotuje wybraną orientacją salw."""
        indeks = self.combo_orientacji.current()
        if indeks == len(self.combo_orientacji["values"]) - 1:
            indeks = 0
        else:
            indeks += 1
        self.combo_orientacji.set(self.combo_orientacji["values"][indeks])


class ComboAtaku(ttk.Combobox):
    """
    Combobox z możliwością zmiany fontu w liście rozwijanej. Wzięte stąd: https://stackoverflow.com/questions/43086378/how-to-modify-ttk-combobox-fonts/ .Standardowy combobox nie daje takiej możliwości.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<Map>", self._obsluz_czcionke_listy_rozwijanej)

    def _obsluz_czcionke_listy_rozwijanej(self, *args):
        lista_rozwijana = self.tk.eval("ttk::combobox::PopdownWindow {}".format(self))
        self.tk.call("{}.f.l".format(lista_rozwijana), 'configure', '-font', self['font'])


class KontrolaFloty(ttk.Frame):
    """
    Sekcja kontroli floty (całej gracza i zatopionej przeciwnika) znajdująca się w środku po prawej stronie głównego interfejsu gry.
    """

    KOLORY = {
        "podświetlenie-rang": "LemonChiffon2"
    }

    def __init__(self, rodzic, plansza_gracza, plansza_przeciwnika):
        super().__init__(rodzic, padding=(0, 0, 10, 0))
        self.plansza_g = plansza_gracza
        self.plansza_p = plansza_przeciwnika
        self.ustaw_style()
        self.ustaw_sie()
        self.buduj_drzewo()
        self.powiaz_callbacki()

        # test
        print(self.plansza_g.gracz.plansza.podaj_ilosc_niezatopionych_wg_rang())
        print(self.plansza_g.gracz.plansza.podaj_ilosc_zatopionych_wg_rang())

    def ustaw_style(self):
        """Ustawia style dla drzewa"""
        self.styl = ttk.Style()
        self.styl.configure(
            "KF.Treeview",
            font=GraGUI.CZCIONKA,
            rowheight=15
        )
        self.styl.configure(
            "KF.Treeview.Heading",
            font=GraGUI.CZCIONKA
        )

    def ustaw_sie(self):
        """Ustawia interfejs pod widżety."""
        self.etyramka = ttk.Labelframe(self, text="Flota", padding=(5, 0, 5, 5))
        self.etyramka.grid()

    def buduj_drzewo(self):
        """Buduje widok drzewa floty."""
        self.drzewo = ttk.Treeview(
            self.etyramka,
            style="KF.Treeview",
            height=20,
            columns=("statek", "gdzie", "rozmiar", "ofiary"),
            displaycolumns="#all",
            selectmode="browse"
        )
        self.drzewo.grid(column=0, row=0, sticky="news")
        self.ustaw_kolumny()
        self.dodaj_statki(self.plansza_g.gracz.plansza.niezatopione, "niezatopione")
        self.ustaw_wyglad()

    def ustaw_kolumny(self):
        """Konfiguruje kolumny drzewa."""
        self.drzewo.heading("statek", text="Statek")
        self.drzewo.heading("gdzie", text="Poz")
        self.drzewo.heading("rozmiar", text="NT/R")
        self.drzewo.heading("ofiary", text=Statek.ORDER)
        self.drzewo.column("#0", stretch=False, width=65)
        self.drzewo.column("statek", stretch=True, width=110)
        self.drzewo.column("gdzie", stretch=False, width=35)
        self.drzewo.column("rozmiar", stretch=False, width=40, anchor=tk.E)
        self.drzewo.column("ofiary", stretch=False, width=12)

    def dodaj_statki(self, statki, kategoria):
        """
        Dodaje podane (niezatopione/zatopione) statki do drzewa. Wartość parametru `kategoria` to albo 'niezatopione' albo 'zatopione'
        """
        # kategoria
        self.drzewo.insert("", "0", kategoria,
                           text=kategoria + " (" + str(len(statki)) + ")",
                           open=True,
                           tags="kategoria"
                           )
        # rangi
        ilosc_wg_rang = self.plansza_g.gracz.plansza.podaj_ilosc_niezatopionych_wg_rang()
        for ranga in Statek.RANGI[::-1]:
            if ilosc_wg_rang[ranga] > 0:
                ranga_i_ilosc = Statek.SYMBOLE[ranga] + " (" + str(ilosc_wg_rang[ranga]) + ")"
                self.drzewo.insert(kategoria, "end",
                                   ranga,
                                   text=ranga_i_ilosc,
                                   open=True,
                                   tags="ranga"
                                   )
        # statki
        for i in range(len(statki)):
            statek = statki[i]
            self.drzewo.insert(
                statek.RANGA, "end",
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
        """Konfiguruje wygląd zawartości drzewa"""
        self.drzewo.tag_configure("kategoria", font=GraGUI.CZCIONKA_BOLD)
        self.drzewo.tag_configure("ranga", background=self.KOLORY["podświetlenie-rang"])

    def powiaz_callbacki(self):
        """Wiąże callbacki"""
        self.drzewo.bind("<Escape>", self.na_escape)
        self.drzewo.tag_bind("statek", "<Double-Button-1>", self.na_podwojne_klikniecie)

    # CALLBACK całego drzewa
    def na_escape(self, event=None):
        """Kasuje selekcję"""
        element_id = self.drzewo.focus()
        if element_id != "":  # jeśli jakiś element był w ogóle wybrany
            self.drzewo.selection_remove(element_id)

    # CALLBACK elementów z tagiem `statek`
    def na_podwojne_klikniecie(self, event=None):
        """Wybiera kliknięty podwójnie statek na planszy gracza"""
        statek = self.plansza_g.gracz.plansza.niezatopione[int(self.drzewo.focus())]
        self.plansza_g.zmien_statek(statek)


class KontrolaGry(ttk.Frame):
    """
    Sekcja kontroli gry znajdująca się w prawym dolnym rogu głównego interfejsu gry.
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
    Pasek stanu wyświetlający komunikaty o grze na dole głównego interfejsu gry.
    """

    def __init__(self, rodzic, plansza_gracza, plansza_przeciwnika):
        super().__init__(rodzic, padding=10)
        self.plansza_g = plansza_gracza
        self.plansza_p = plansza_przeciwnika
        # GUI
        self.grid(columnspan=3)
        pass  # TODO


class GraGUI(ttk.Frame):
    """Główny interfejs gry"""

    CZCIONKA = ("TkDefaultFont", 8)
    CZCIONKA_BOLD = ("TkDefaultFont", 8, "bold")

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
        kontrola_ataku.grid(column=2, row=0, rowspan=1, sticky=tk.N)
        kontrola_floty = KontrolaFloty(self, plansza_gracza, plansza_przeciwnika)
        kontrola_floty.grid(column=2, row=1, rowspan=5, sticky="news")
        kontrola_gry = KontrolaGry(self, plansza_gracza, plansza_przeciwnika)
        kontrola_gry.grid(column=2, row=2)

        # sekcja komunikatów na dole okna
        pasek_stanu = PasekStanu(self, plansza_gracza, plansza_przeciwnika)
        pasek_stanu.grid(column=0, row=3)


def main():
    """Uruchamia grę."""
    root = tk.Tk()
    root.title("Statki")

    GraGUI(root, 26, 30)

    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
