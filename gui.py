#!/usr/bin/env python3

"""
Graficzny interfejs użytkownika
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from plansza import Plansza, Pole, Statek
from mechanika import Gracz


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
    """Graficzna reprezentacja planszy - szczegółowa implementacja w klasach potomnych. Nie dopuszcza powiększania."""

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
        etykieta = ttk.Label(text=self.tytul, style="Bold.TLabel")
        self.etyramka = ttk.LabelFrame(self, labelwidget=etykieta, padding=10)
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
        self.drzewo_floty = None  # Kontrola Floty jw.
        self.ustaw_style_gracza()
        self.powiaz_callbacki()
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

    def powiaz_callbacki(self):
        """Wiąże callbacki."""
        # wszystkie pola
        for i in range(self.gracz.plansza.kolumny):
            for j in range(self.gracz.plansza.rzedy):
                kolumna, rzad = i + 1, j + 1
                # lambda bez własnych argumentów (w formie: lambda: self.na_klikniecie(kolumna, rzad) nie zadziała prawidłowo w tym przypadku - zmienne przekazywane do każdej funkcji (anonimowej czy nie - bez różnicy) są zawsze ewaluowane dopiero w momencie wywołania tej funkcji, tak więc w tym przypadku w danej iteracji pętli zostają przekazane zmienne "i" i "j" (nazwy) a nie ich wartości - wartości zostaną ewaluowane dopiero w momencie wywołania callbacka (czyli naciśnięcia przycisku) i będzie to wartość z ostatniej iteracji dla wszystkich przycisków, więcej tutaj: https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture/23557126))
                pole_gui = self.podaj_pole_gui(kolumna, rzad)
                pole_gui.configure(command=lambda x=kolumna, y=rzad: self.na_klikniecie(x, y))  # lambda konieczna, bo nie da się tego obsłużyć tak jak niżej z bind() - w przypadku przypisywania callbacków opcją 'command' nie ma przekazywania obiektu zdarzenia, z którego można by pobrać współrzędne pola
        # okno główne
        self.winfo_toplevel().bind("[", self.na_nawias_kw_lewy)
        self.winfo_toplevel().bind("]", self.na_nawias_kw_prawy)

    # CALLBACK wszystkich pól
    def na_klikniecie(self, kolumna, rzad):
        """
        Wybiera kliknięty statek, kasując wybór poprzedniego. Zatopione statki nie są wybierane. Ten sam mechanizm jest uruchamiany po wyborze statku w sekcji Kontroli Ataku.
        """
        statek = self.gracz.plansza.podaj_statek(self.podaj_pole_gui(kolumna, rzad).pole)
        self.zmien_statek(statek)

        print("Kliknięcie w polu: ({}{})".format(Plansza.ALFABET[kolumna], rzad))  # test

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
        # kontrola widżetów w innych sekcjach
        self.gracz.tura.runda.statek = statek
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
        # 1 pole
        self.odkryj_pole(kolumna, rzad)
        # 2 pola w prawo
        if self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[1]:
            self.odkryj_pole(kolumna + 1, rzad)
        # 2 pola w dół
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[2]:
            self.odkryj_pole(kolumna, rzad + 1)
        # 2 pola w lewo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[3]:
            self.odkryj_pole(kolumna - 1, rzad)
        # 2 pola w górę
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[4]:
            self.odkryj_pole(kolumna, rzad - 1)
        # 3 pola poziomo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[5]:
            self.odkryj_pole(kolumna - 1, rzad)
            self.odkryj_pole(kolumna + 1, rzad)
        # 3 pola pionowo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[6]:
            self.odkryj_pole(kolumna, rzad - 1)
            self.odkryj_pole(kolumna, rzad + 1)
        # 3 pola L
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[7]:
            self.odkryj_pole(kolumna, rzad - 1)
            self.odkryj_pole(kolumna + 1, rzad)
        # 3 pola Г
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[8]:
            self.odkryj_pole(kolumna, rzad + 1)
            self.odkryj_pole(kolumna + 1, rzad)
        # 3 pola Ꞁ
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[9]:
            self.odkryj_pole(kolumna - 1, rzad)
            self.odkryj_pole(kolumna, rzad + 1)
        # 3 pola ⅃
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[10]:
            self.odkryj_pole(kolumna - 1, rzad)
            self.odkryj_pole(kolumna, rzad - 1)

        print("Kliknięcie w polu: ({}{})".format(Plansza.ALFABET[kolumna], rzad))  # test

    # CALLBACK wszystkich pól
    def na_wejscie(self, event):
        """
        W zależności od wybranej orientacji w Kontroli Ataku podświetla lub nie dodatkowe, sąsiednie pola w odpowiedniej konfiguracji.
        """
        kolumna, rzad = event.widget.pole.podaj_wspolrzedne()
        # 2 pola w prawo
        if self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[1]:
            self.zmien_stan_pola(kolumna + 1, rzad, "active")
        # 2 pola w dół
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[2]:
            self.zmien_stan_pola(kolumna, rzad + 1, "active")
        # 2 pola w lewo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[3]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active")
        # 2 pola w górę
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[4]:
            self.zmien_stan_pola(kolumna, rzad - 1, "active")
        # 3 pola poziomo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[5]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active")
            self.zmien_stan_pola(kolumna + 1, rzad, "active")
        # 3 pola pionowo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[6]:
            self.zmien_stan_pola(kolumna, rzad - 1, "active")
            self.zmien_stan_pola(kolumna, rzad + 1, "active")
        # 3 pola L
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[7]:
            self.zmien_stan_pola(kolumna, rzad - 1, "active")
            self.zmien_stan_pola(kolumna + 1, rzad, "active")
        # 3 pola Г
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[8]:
            self.zmien_stan_pola(kolumna, rzad + 1, "active")
            self.zmien_stan_pola(kolumna + 1, rzad, "active")
        # 3 pola Ꞁ
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[9]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active")
            self.zmien_stan_pola(kolumna, rzad + 1, "active")
        # 3 pola ⅃
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[10]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active")
            self.zmien_stan_pola(kolumna, rzad - 1, "active")

    # CALLBACK wszystkich pól
    def na_wyjscie(self, event):
        """
        W zależności od wybranej orientacji w Kontroli Ataku kasuje podświetlenie dodatkowych, sąsiednich pól (lub pola) wywołane wcześniejszym uruchomieniem callbacka `na_wejscie()`.
        """
        kolumna, rzad = event.widget.pole.podaj_wspolrzedne()
        # 2 pola w prawo
        if self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[1]:
            self.zmien_stan_pola(kolumna + 1, rzad, "!active")
        # 2 pola w dół
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[2]:
            self.zmien_stan_pola(kolumna, rzad + 1, "!active")
        # 2 pola w lewo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[3]:
            self.zmien_stan_pola(kolumna - 1, rzad, "!active")
        # 2 pola w górę
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[4]:
            self.zmien_stan_pola(kolumna, rzad - 1, "!active")
        # 3 pola poziomo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[5]:
            self.zmien_stan_pola(kolumna - 1, rzad, "!active")
            self.zmien_stan_pola(kolumna + 1, rzad, "!active")
        # 3 pola pionowo
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[6]:
            self.zmien_stan_pola(kolumna, rzad - 1, "!active")
            self.zmien_stan_pola(kolumna, rzad + 1, "!active")
        # 3 pola L
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[7]:
            self.zmien_stan_pola(kolumna, rzad - 1, "!active")
            self.zmien_stan_pola(kolumna + 1, rzad, "!active")
        # 3 pola Г
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[8]:
            self.zmien_stan_pola(kolumna, rzad + 1, "!active")
            self.zmien_stan_pola(kolumna + 1, rzad, "!active")
        # 3 pola Ꞁ
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[9]:
            self.zmien_stan_pola(kolumna - 1, rzad, "!active")
            self.zmien_stan_pola(kolumna, rzad + 1, "!active")
        # 3 pola ⅃
        elif self.combo_orientacji.get() == KontrolaAtaku.ORIENTACJE[10]:
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


# ***************************************** SEKCJA KONTROLI *************************************************


class KontrolaAtaku(ttk.Frame):
    """
    Sekcja kontroli ataku znajdująca się w prawym górnym rogu głównego interfejsu gry. Dopuszcza powiększanie w poziomie.
    """

    ORIENTACJE = ["•", "•• prawo", "╏ dół", "•• lewo", "╏ góra", "•••", "┇", "L", "Г", "Ꞁ", "⅃"]

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

    def ustaw_style(self):
        """Ustawia style dla widżetów"""
        self.styl = ttk.Style()
        # etykiety
        self.styl.configure(
            "KA.TLabel",
            font=GraGUI.CZCIONKA_MALA
        )
        # comboboksy
        self.styl.configure("KA.TCombobox")
        self.styl.map(
            "KA.TCombobox",
            fieldbackground=[("readonly", "white")]
        )

    def ustaw_sie(self):
        """Ustawia interfejs pod widżety."""
        etykieta = ttk.Label(text="Atak", style="Bold.TLabel")
        self.etyramka = ttk.Labelframe(self, labelwidget=etykieta, padding=(5, 15, 5, 5))
        self.etyramka.grid(sticky="we")
        self.etyramka.columnconfigure(0, weight=1)  # zgłasza wyżej powiększanie w poziomie

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
        self.combo_statku = ComboZeZmianaCzcionki(
            self.etyramka,
            styl="KA.TCombobox",
            font=GraGUI.CZCIONKA_MALA,
            values=self.plansza_g.gracz.tura.statki,
            width=35
        )
        self.combo_statku.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=tk.W
        )
        self.combo_statku.configure(font=GraGUI.CZCIONKA_MALA)  # to zmienia tylko czcionkę pola tekstowego (Entry), które jest częścią comboboksa

        # wybór salwy
        self.combo_salwy = ComboZeZmianaCzcionki(
            self.etyramka,
            styl="KA.TCombobox",
            font=GraGUI.CZCIONKA_MALA,
            width=6
        )
        self.combo_salwy.grid(
            row=3,
            column=0,
            sticky=tk.W,
            pady=(0, 10)
        )
        self.combo_salwy.configure(font=GraGUI.CZCIONKA_MALA)

        # wybór orientacji
        self.combo_orientacji = ComboZeZmianaCzcionki(
            self.etyramka,
            styl="KA.TCombobox",
            font=GraGUI.CZCIONKA_MALA,
            width=7
        )
        self.combo_orientacji.grid(
            row=3,
            column=1,
            sticky=tk.W,
            pady=(0, 10)
        )
        self.combo_orientacji.configure(font=GraGUI.CZCIONKA_MALA)

    def ustaw_combo_readonly(self):
        """Ustawia stan comboboksów jako `readonly`"""
        self.combo_statku.state(["readonly"])
        self.combo_salwy.state(["readonly"])
        self.combo_orientacji.state(["readonly"])

    def przekaz_odnosniki(self):
        """Przekazuje własne odnośniki dla event handlerów w planszach"""
        self.plansza_g.kontrola_ataku = self
        self.plansza_p.combo_orientacji = self.combo_orientacji

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
            self.combo_orientacji["values"] = self.ORIENTACJE[1:5]
        elif salwa == 3:
            self.combo_orientacji["values"] = self.ORIENTACJE[5:]
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


class KontrolaFloty(ttk.Frame):
    """
    Sekcja kontroli floty (całej gracza i zatopionej przeciwnika) znajdująca się w środku po prawej stronie głównego interfejsu gry. Dopuszcza powiększanie w poziomie i w pionie.
    """

    def __init__(self, rodzic, plansza_gracza, plansza_przeciwnika):
        super().__init__(rodzic, padding=(0, 0, 10, 360))
        self.plansza_g = plansza_gracza
        self.plansza_p = plansza_przeciwnika
        self.ustaw_sie()
        self.buduj_drzewa()
        self.przekaz_odnosniki()

    def ustaw_sie(self):
        """Ustawia interfejs pod widżety."""
        etykieta = ttk.Label(text="Flota", style="Bold.TLabel")
        self.etyramka = ttk.Labelframe(self, labelwidget=etykieta, padding=(5, 7, 5, 13))
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
        notes.grid(row=0, column=0, columnspan=2, sticky="nsew")
        # zgłasza wyżej powiększanie w poziomie i w pionie
        notes.rowconfigure(0, weight=1)
        notes.columnconfigure(0, weight=1)

    def buduj_przyciski(self):
        """Buduje przyciski przewijania statków."""
        ikona_do_przodu = ImageTk.PhotoImage(Image.open("zasoby/ikona_statku/statek-w-prawo_48x48.png"))
        ikona_do_tylu = ImageTk.PhotoImage(Image.open("zasoby/ikona_statku/statek-w-lewo_48x48.png"))
        self.przycisk_do_przodu = ttk.Button(
            self.etyramka,
            text="Kolejny",
            image=ikona_do_przodu,
            command=self.plansza_g.na_nawias_kw_prawy
        )
        self.przycisk_do_tylu = ttk.Button(
            self.etyramka,
            text="Poprzedni",
            image=ikona_do_tylu,
            command=self.plansza_g.na_nawias_kw_lewy
        )

    def przekaz_odnosniki(self):
        """Przekazuje własne odnośniki do event handlerów w planszach."""
        self.plansza_g.drzewo_floty = self.drzewo_g


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
        self.plansza = plansza_gui

        self.ustaw_style()
        self.ustaw_sie()
        self.wstaw_suwaki(rodzic)
        self.powiaz_escape()

    def ustaw_style(self):
        """Ustawia style dla drzewa."""
        self.styl = ttk.Style()
        self.styl.configure(
            "KF.Treeview",
            font=GraGUI.CZCIONKA_MALA,
            rowheight=15
        )
        self.styl.configure(
            "KF.Treeview.Heading",
            font=GraGUI.CZCIONKA_MALA
        )

    def ustaw_sie(self):
        """Konfiguruje to drzewo."""
        self.configure(
            style="KF.Treeview",
            height=19,
            columns=("statek", "gdzie", "rozmiar", "ofiary"),
            displaycolumns="#all",
            selectmode="browse"
        )
        self.grid(sticky="nsew")

    def wstaw_suwaki(self, rodzic):
        """Wstawia w drzewo suwaki."""
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
        self.column("gdzie", stretch=True, minwidth=35, width=49)
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
        self.dodaj_statki(self.plansza.gracz.plansza.niezatopione, "niezatopione")
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
        ilosc_wg_rang = self.plansza.gracz.plansza.podaj_ilosc_niezatopionych_wg_rang()
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
        """Konfiguruje wygląd zawartości drzewa."""
        self.tag_configure("kategoria", font=GraGUI.CZCIONKA_MALA_BOLD)
        self.tag_configure("ranga", background=self.KOLORY["podświetlenie-rang"])

    def powiaz_podwojne_klikniecie(self):
        """Wiąże callback obsługujący podóœjne kliknięcie."""
        self.tag_bind("statek", "<Double-Button-1>", self.na_podwojne_klikniecie)

    # CALLBACK elementów z tagiem `statek`
    def na_podwojne_klikniecie(self, event=None):
        """Wybiera kliknięty podwójnie statek na planszy gracza."""
        # TODO: w drzewie nie może dać się wybierać statków które już miały swoją rundę w tej turze!
        statek = self.plansza.gracz.tura.statki[int(self.focus())]
        self.plansza.zmien_statek(statek)


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


class KontrolaGry(ttk.Frame):
    """
    Sekcja kontroli gry znajdująca się w prawym dolnym rogu głównego interfejsu gry. Dopuszcza powiększanie w poziomie.
    """

    def __init__(self, rodzic, plansza_gracza, plansza_przeciwnika):
        super().__init__(rodzic, padding=(0, 0, 10, 0))
        self.plansza_g = plansza_gracza
        self.plansza_p = plansza_przeciwnika
        # GUI
        self.tytul = None  # string w formacie `Tura #[liczba]/Runda #[liczba]`
        etyramka = ttk.Labelframe(self, text=self.tytul, padding=5)
        etyramka.grid(sticky="we")
        # zgłasza wyżej powiększanie w poziomie
        etyramka.columnconfigure(0, weight=1)
        pass  # TODO


# ****************************************** SEKCJA STANU ***************************************************


class PasekStanu(ttk.Frame):
    """
    Pasek stanu wyświetlający komunikaty o grze na dole głównego interfejsu gry. Dopuszcza powiększanie w poziomie i w pionie.
    """

    def __init__(self, rodzic, plansza_gracza, plansza_przeciwnika):
        super().__init__(rodzic, padding=10)
        self.plansza_g = plansza_gracza
        self.plansza_p = plansza_przeciwnika
        pass  # TODO


# ******************************************** OKNO GŁÓWNE **************************************************


class GraGUI(ttk.Frame):
    """Główny interfejs gry"""

    CZCIONKA_MALA = ("TkDefaultFont", 8)
    CZCIONKA_MALA_BOLD = ("TkDefaultFont", 8, "bold")
    CZCIONKA_BOLD = ("TkDefaultFont", 9, "bold")

    def __init__(self, rodzic, kolumny, rzedy):
        super().__init__(rodzic)
        self.grid()

        gracz = Gracz(Plansza(kolumny, rzedy))
        przeciwnik = Gracz(Plansza(kolumny, rzedy))

        self.ustaw_style()
        self.buduj_plansze(gracz, przeciwnik)
        self.buduj_sekcje_kontroli()
        self.buduj_pasek_stanu()
        self.ustaw_grid()

        self.wybierz_statek_startowy()

    def ustaw_style(self):
        """Ustawia style dla okna głównego."""
        self.styl = ttk.Style()
        self.styl.configure(
            "Bold.TLabel",
            font=self.CZCIONKA_BOLD
        )

    def buduj_plansze(self, gracz, przeciwnik):
        """Buduje plansze gracza i przeciwnika"""
        self.plansza_g = PlanszaGracza(self, gracz)
        self.plansza_g.grid(column=0, row=0, rowspan=3)
        self.plansza_p = PlanszaPrzeciwnika(self, przeciwnik)
        self.plansza_p.grid(column=1, row=0, rowspan=3)

    def buduj_sekcje_kontroli(self):
        """Buduje sekcje kontroli: ataku, floty i gry po prawej stronie okna głównego"""
        self.kontrola_ataku = KontrolaAtaku(self, self.plansza_g, self.plansza_p)
        self.kontrola_ataku.grid(column=2, row=0, sticky=tk.N)
        self.kontrola_floty = KontrolaFloty(self, self.plansza_g, self.plansza_p)
        self.kontrola_floty.grid(column=2, row=1, sticky="nsew")
        self.kontrola_gry = KontrolaGry(self, self.plansza_g, self.plansza_p)
        self.kontrola_gry.grid(column=2, row=2)

    def buduj_pasek_stanu(self):
        """Buduje pasek stanu na dole okna głównego"""
        self.pasek_stanu = PasekStanu(self, self.plansza_g, self.plansza_p)
        self.pasek_stanu.grid(column=0, row=3, columnspan=3)

    def ustaw_grid(self):
        """Konfiguruje layout managera. Dopuszcza powiększanie trzeciej kolumny (w poziomie) i czwartego rzędu (w pionie)."""
        self.columnconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

    def wybierz_statek_startowy(self):
        """Wybiera największy statek na start gry."""
        self.plansza_g.wybierz_statek(self.plansza_g.gracz.plansza.statki[0])
        self.kontrola_floty.drzewo_g.see("niezatopione")


def main():
    """Uruchamia grę."""
    okno_glowne = tk.Tk()
    okno_glowne.title("Statki")

    # GraGUI(okno_glowne, 26, 30)
    GraGUI(okno_glowne, 26, 30)

    okno_glowne.resizable(False, False)
    okno_glowne.mainloop()


if __name__ == "__main__":
    main()
