#!/usr/bin/env python3

"""
Graficzny interfejs użytkownika
"""

import tkinter as tk
from tkinter import ttk

from plansza import Plansza, Pole


class PoleGUI(ttk.Button):
    """Graficzna reprezentacja pola planszy"""

    KOLORY = {
        "woda": "powder blue",
        "woda-active": "light cyan",
        "pudło": "DeepSkyBlue3",
        "pudło-active": "deep sky blue",
        "trafione": "light coral",
        "trafione-active": "light pink",
        "zatopione": "ivory4",
        "zatopione-active": "ivory3",
        "nieodkryte-active": "DarkSeaGreen1"
    }

    def __init__(self, rodzic, pole, *args, **kwargs):
        super().__init__(rodzic, *args, **kwargs)
        self.pole = pole


class PlanszaGUI(ttk.Frame):
    """Graficzna reprezentacja planszy - szczegółowa implementacja w klasach potomnych"""

    def __init__(self, rodzic, kolumny, rzedy, tytul):
        super().__init__(rodzic, padding=10)
        self.tytul = tytul
        self.plansza = Plansza(kolumny, rzedy)
        self.pola_gui = [[0 for kolumna in range(self.plansza.kolumny)] for rzad in range(self.plansza.rzedy)]  # matryca (lista rzędów (list)) obiektów klasy PoleGUI (tu inicjalizowanych jako "0")
        # GUI
        self.grid()
        self.styl = ttk.Style()
        self.etykietoramka = ttk.LabelFrame(self, text=self.tytul, padding=10)
        self.etykietoramka.grid()
        self.ustaw_style()
        self.buduj_etykiety()
        self.buduj_pola()

    def ustaw_style(self):
        """Definiuje style dla pól"""
        # woda
        self.styl.configure(
            "Woda.TButton",
            relief="sunken",
            background=PoleGUI.KOLORY["woda"]
        )
        self.styl.map(
            "Woda.TButton",
            relief=[("active", "sunken"), ("disabled", "sunken")],
            background=[("active", PoleGUI.KOLORY["woda-active"]), ("disabled", "gray")]
        )
        # pudło
        self.styl.configure(
            "Pudło.TButton",
            relief="sunken",
            background=PoleGUI.KOLORY["pudło"]
        )
        self.styl.map(
            "Pudło.TButton",
            relief=[("active", "sunken"), ("disabled", "sunken")],
            background=[("active", PoleGUI.KOLORY["pudło-active"]), ("disabled", "gray")]
        )
        # trafione
        self.styl.configure(
            "Trafione.TButton",
            background=PoleGUI.KOLORY["trafione"]
        )
        self.styl.map(
            "Trafione.TButton",
            background=[("active", PoleGUI.KOLORY["trafione-active"]), ("disabled", "gray")]
        )
        # zatopione
        self.styl.configure(
            "Zatopione.TButton",
            relief="sunken",
            foreground="white",
            background=PoleGUI.KOLORY["zatopione"]
        )
        self.styl.map(
            "Zatopione.TButton",
            relief=[("active", "sunken"), ("disabled", "sunken")],
            foreground=[("active", "white"), ("disabled", "white")],
            background=[("active", PoleGUI.KOLORY["zatopione-active"]), ("disabled", "gray")]
        )

    def buduj_etykiety(self):
        """Buduje etykiety kolumn i rzędów"""
        for kolumna in range(self.plansza.kolumny):
            ttk.Label(
                self.etykietoramka,
                text=str(kolumna + 1),
                anchor=tk.CENTER
            ).grid(
                row=0,
                column=kolumna + 1,
                sticky=tk.W + tk.E,
                pady=(0, 3)
            )
        for rzad in range(self.plansza.rzedy):
            ttk.Label(
                self.etykietoramka,
                text=Plansza.ALFABET[rzad + 1]
            ).grid(
                column=0,
                row=rzad + 1,
                sticky=tk.E,
                padx=(0, 6)
            )

    def buduj_pola(self):
        """Buduje pola planszy"""
        for i in range(self.plansza.kolumny):
            for j in range(self.plansza.rzedy):
                kolumna, rzad = i + 1, j + 1
                pole_gui = PoleGUI(
                    self.etykietoramka,
                    self.plansza.podaj_pole(kolumna, rzad),
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
        """Podaje pole planszy"""
        return self.pola_gui[rzad - 1][kolumna - 1]

    @staticmethod
    def oznacz_pudlo(pole_gui):
        """Oznacza podane pole jako pudło"""
        pole_gui.pole.znacznik = Pole.ZNACZNIKI["pudło"]
        pole_gui.configure(style="Pudło.TButton", text="•")

    def zatop_statek(self, statek, symbole=False):
        """Oznacza pola wskazanego statku jako zatopione"""
        for pole in statek.pola:
            pole.znacznik = Pole.ZNACZNIKI["zatopione"]
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            pole_gui.configure(style="Zatopione.TButton")
            if symbole:
                pole_gui.configure(text=statek.SYMBOL)

        self.plansza.zatopione.append(statek)


class PlanszaGracza(PlanszaGUI):
    """Graficzna reprezentacja planszy gracza"""

    def __init__(self, rodzic, kolumny, rzedy, tytul="Gracz"):
        super().__init__(rodzic, kolumny, rzedy, tytul)
        self.odkryj_wszystkie_pola()

        # testy
        self.oznacz_pudlo(self.podaj_pole_gui(5, 5))
        statek = self.plansza.statki[0]
        self.oznacz_trafione(self.podaj_pole_gui(*statek.polozenie.podaj_wspolrzedne()))
        statek = self.plansza.statki[1]
        self.zatop_statek(statek)

    @staticmethod
    def oznacz_trafione(pole_gui):
        """Oznacza podane pole jako trafione"""
        pole_gui.pole.znacznik = Pole.ZNACZNIKI["trafione"]
        pole_gui.configure(style="Trafione.TButton")

    def odkryj_wszystkie_pola(self):
        """Odkrywa wszystkie pola planszy"""
        for rzad in self.pola_gui:
            for pole_gui in rzad:
                statek = self.plansza.podaj_statek(pole_gui.pole)
                if pole_gui.pole.znacznik in (Pole.ZNACZNIKI["puste"], Pole.ZNACZNIKI["obwiednia"]):
                    pole_gui.configure(style="Woda.TButton")
                else:
                    pole_gui.configure(text=statek.SYMBOL)


class PlanszaPrzeciwnika(PlanszaGUI):
    """Graficzna reprezentacja planszy przeciwnika"""
    ELKI = {
        "L90": "Г",
        "L180": "˥",
        "L270": "⅃"
    }
    TRYBY_ATAKU = {
        "zwykły": 1,
        "--": 2,
        "||": 3,
        "---": 4,
        "|||": 5,
        "L": 6,
        "Г": 7,
        "˥": 8,
        "⅃": 9
    }

    def __init__(self, rodzic, kolumny, rzedy, tytul="Przeciwnik"):
        super().__init__(rodzic, kolumny, rzedy, tytul)
        self.tryb_ataku = self.TRYBY_ATAKU["zwykły"]
        self.zmien_podswietlanie_nieodkrytych()
        self.rejestruj_callbacki()
        # test
        self.tryb_ataku = self.TRYBY_ATAKU[self.ELKI["L270"]]

    def zmien_podswietlanie_nieodkrytych(self):
        """Zmienia podświetlanie nieodkrytych pól na odpowiedni kolor"""
        self.styl.map("Nieodkryte.TButton", background=[("active", PoleGUI.KOLORY["nieodkryte-active"])])
        for rzad in self.pola_gui:
            for pole_gui in rzad:
                pole_gui.configure(styl="Nieodkryte.TButton")

    def rejestruj_callbacki(self):
        """Rejestruje callbacki na_klikniecie(), na_wejscie() i na_wyjscie() we wszystkich polach"""
        for i in range(self.plansza.kolumny):
            for j in range(self.plansza.rzedy):
                kolumna, rzad = i + 1, j + 1
                # lambda bez własnych argumentów (w formie: lambda: self.na_klikniecie(kolumna, rzad) nie zadziała prawidłowo w tym przypadku - zmienne przekazywane do każdej funkcji (anonimowej czy nie - bez różnicy) są zawsze ewaluowane dopiero w momencie wywołania tej funkcji, tak więc w tym przypadku w danej iteracji pętli zostają przekazane zmienne "i" i "j" (nazwy) a nie ich wartości - wartości zostaną ewaluowane dopiero w momencie wywołania callbacka (czyli naciśnięcia przycisku) i będzie to wartość z ostatniej iteracji dla wszystkich przycisków, więcej tutaj: https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture/23557126))
                pole_gui = self.podaj_pole_gui(kolumna, rzad)
                pole_gui.configure(command=lambda x=kolumna, y=rzad: self.na_klikniecie(x, y))  # lambda konieczna, bo nie da się tego obsłużyć tak jak niżej z bind() - w przypadku przypisywania callbacków opcją 'command' nie ma przekazywania obiektu zdarzenia, z którego można by pobrać współrzędne pola
                pole_gui.bind("<Enter>", self.na_wejscie)
                pole_gui.bind("<Leave>", self.na_wyjscie)

    def na_klikniecie(self, kolumna, rzad):
        """
        Callback każdego pola uruchamiany po naciśnięciu.
        W zależności od 9-stanowej flagi 'tryb_ataku' odkrywa na planszy odpowiednie pola (lub pole)
        """
        self.odkryj_pole(kolumna, rzad)
        if self.tryb_ataku == self.TRYBY_ATAKU["--"]:
            self.odkryj_pole(kolumna + 1, rzad)

        elif self.tryb_ataku == self.TRYBY_ATAKU["||"]:
            self.odkryj_pole(kolumna, rzad + 1)

        elif self.tryb_ataku == self.TRYBY_ATAKU["---"]:
            self.odkryj_pole(kolumna - 1, rzad)
            self.odkryj_pole(kolumna + 1, rzad)

        elif self.tryb_ataku == self.TRYBY_ATAKU["|||"]:
            self.odkryj_pole(kolumna, rzad - 1)
            self.odkryj_pole(kolumna, rzad + 1)

        elif self.tryb_ataku == self.TRYBY_ATAKU["L"]:
            self.odkryj_pole(kolumna, rzad - 1)
            self.odkryj_pole(kolumna + 1, rzad)

        elif self.tryb_ataku == self.TRYBY_ATAKU[self.ELKI["L90"]]:
            self.odkryj_pole(kolumna, rzad + 1)
            self.odkryj_pole(kolumna + 1, rzad)

        elif self.tryb_ataku == self.TRYBY_ATAKU[self.ELKI["L180"]]:
            self.odkryj_pole(kolumna - 1, rzad)
            self.odkryj_pole(kolumna, rzad + 1)

        elif self.tryb_ataku == self.TRYBY_ATAKU[self.ELKI["L270"]]:
            self.odkryj_pole(kolumna - 1, rzad)
            self.odkryj_pole(kolumna, rzad - 1)

        print("Kliknięcie w polu: ({}{})".format(Plansza.ALFABET[rzad], kolumna))  # test

    def odkryj_pole(self, kolumna, rzad):
        """Odkrywa na planszy pole wg podanych współrzędnych. Zaznacza pudło lub trafienie. Zatapia trafiony statek (i odkrywa pola jego obwiedni), jeśli trzeba"""
        if self.plansza.czy_pole_w_planszy(kolumna, rzad):
            pole_gui = self.podaj_pole_gui(kolumna, rzad)
            if pole_gui.pole.znacznik in (Pole.ZNACZNIKI["puste"], Pole.ZNACZNIKI["obwiednia"]):
                self.oznacz_pudlo(pole_gui)
            elif pole_gui.pole.znacznik == Pole.ZNACZNIKI["statek"]:
                pole_gui.pole.znacznik = Pole.ZNACZNIKI["trafione"]
                pole_gui.configure(style="Trafione.TButton", text="�")
                statek = self.plansza.podaj_statek(pole_gui.pole)
                if statek.czy_zatopiony():
                    self.zatop_statek(statek, symbole=True)
                    self.odkryj_obwiednie(statek)

    def odkryj_obwiednie(self, statek):
        """Odkrywa na planszy obwiednie zatopionego statku"""
        for pole in statek.obwiednia:
            # configure("style") zwraca krotkę, której ostatnim elementem jest nazwa stylu
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            if pole_gui.configure("style")[-1] not in ("Woda.TButton", "Pudło.TButton"):
                pole_gui.configure(style="Woda.TButton")
        # test
        print(statek.o_zatopieniu())

    def na_wejscie(self, event):
        """
        Callback każdego pola uruchamiany po wejściu kursora w obręb pola.
        W zależności od 9-stanowej flagi 'tryb_ataku' podświetla lub nie dodatkowe, sąsiednie pola w odpowiedniej konfiguracji
        """
        kolumna, rzad = event.widget.pole.podaj_wspolrzedne()
        if self.tryb_ataku == self.TRYBY_ATAKU["--"]:
            self.zmien_stan_pola(kolumna + 1, rzad, "active")

        elif self.tryb_ataku == self.TRYBY_ATAKU["||"]:
            self.zmien_stan_pola(kolumna, rzad + 1, "active")

        elif self.tryb_ataku == self.TRYBY_ATAKU["---"]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active")
            self.zmien_stan_pola(kolumna + 1, rzad, "active")

        elif self.tryb_ataku == self.TRYBY_ATAKU["|||"]:
            self.zmien_stan_pola(kolumna, rzad - 1, "active")
            self.zmien_stan_pola(kolumna, rzad + 1, "active")

        elif self.tryb_ataku == self.TRYBY_ATAKU["L"]:
            self.zmien_stan_pola(kolumna, rzad - 1, "active")
            self.zmien_stan_pola(kolumna + 1, rzad, "active")

        elif self.tryb_ataku == self.TRYBY_ATAKU[self.ELKI["L90"]]:
            self.zmien_stan_pola(kolumna, rzad + 1, "active")
            self.zmien_stan_pola(kolumna + 1, rzad, "active")

        elif self.tryb_ataku == self.TRYBY_ATAKU[self.ELKI["L180"]]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active")
            self.zmien_stan_pola(kolumna, rzad + 1, "active")

        elif self.tryb_ataku == self.TRYBY_ATAKU[self.ELKI["L270"]]:
            self.zmien_stan_pola(kolumna - 1, rzad, "active")
            self.zmien_stan_pola(kolumna, rzad - 1, "active")

    def na_wyjscie(self, event):
        """
        Callback każdego pola uruchamiany po wyjściu kursora z obrębu pola.
        W zależności od 9-stanowej flagi 'tryb_ataku' kasuje podświetlenie dodatkowych, sąsiednich pól (lub pola) wywołane wcześniej odpaleniem callbacka na_wejscie()
        """
        kolumna, rzad = event.widget.pole.podaj_wspolrzedne()
        if self.tryb_ataku == self.TRYBY_ATAKU["--"]:
            self.zmien_stan_pola(kolumna + 1, rzad, "!active")

        elif self.tryb_ataku == self.TRYBY_ATAKU["||"]:
            self.zmien_stan_pola(kolumna, rzad + 1, "!active")

        elif self.tryb_ataku == self.TRYBY_ATAKU["---"]:
            self.zmien_stan_pola(kolumna - 1, rzad, "!active")
            self.zmien_stan_pola(kolumna + 1, rzad, "!active")

        elif self.tryb_ataku == self.TRYBY_ATAKU["|||"]:
            self.zmien_stan_pola(kolumna, rzad - 1, "!active")
            self.zmien_stan_pola(kolumna, rzad + 1, "!active")

        elif self.tryb_ataku == self.TRYBY_ATAKU["L"]:
            self.zmien_stan_pola(kolumna, rzad - 1, "!active")
            self.zmien_stan_pola(kolumna + 1, rzad, "!active")

        elif self.tryb_ataku == self.TRYBY_ATAKU[self.ELKI["L90"]]:
            self.zmien_stan_pola(kolumna, rzad + 1, "!active")
            self.zmien_stan_pola(kolumna + 1, rzad, "!active")

        elif self.tryb_ataku == self.TRYBY_ATAKU[self.ELKI["L180"]]:
            self.zmien_stan_pola(kolumna - 1, rzad, "!active")
            self.zmien_stan_pola(kolumna, rzad + 1, "!active")

        elif self.tryb_ataku == self.TRYBY_ATAKU[self.ELKI["L270"]]:
            self.zmien_stan_pola(kolumna - 1, rzad, "!active")
            self.zmien_stan_pola(kolumna, rzad - 1, "!active")

    def zmien_stan_pola(self, kolumna, rzad, stan):
        """Zmienia stan pola wg podanych współrzędnych"""
        if self.plansza.czy_pole_w_planszy(kolumna, rzad):
            self.podaj_pole_gui(kolumna, rzad).state([stan])


class KontrolaAtaku(ttk.Frame):
    """Graficzna reprezentacja sekcji kontroli ataku znajdującej się w prawym górnym rogu głównego interfejsu gry"""

    def __init__(self, rodzic, plansza_gracza, plansza_przeciwnika):
        super().__init__(rodzic, padding=10)
        self.plansza_gracza = plansza_gracza
        self.plansza_przeciwnika = plansza_przeciwnika
        # GUI
        self.etykietoramka = ttk.Labelframe(self, text="Atak", padding=10)
        self.combo_statku = None
        self.combo_salwy = None
        self.combo_orientacji = None


def main():
    """Uruchamia skrypt"""
    root = tk.Tk()
    root.title("Statki")

    rama = ttk.Frame(root)
    rama.grid()

    # przy ekranie 1920x1200 sensowne wymiary (jednej) planszy to od 5x5 do 50x30, przy dwóch planszach (gracz+przeciwnik) to 5x5 do 25x30 ==> TODO: zaimplementować w GUI
    kolumny, rzedy = 15, 20
    # kolumny, rzedy = 25, 30
    gracz = PlanszaGracza(rama, kolumny, rzedy)
    gracz.grid(column=0, row=0)
    przeciwnik = PlanszaPrzeciwnika(rama, kolumny, rzedy)
    przeciwnik.grid(column=1, row=0)
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
