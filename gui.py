#!/usr/bin/env python3

"""
Graficzny interfejs użytkownika
"""

import tkinter as tk
from tkinter import ttk

from statki import Plansza, Pole


class PoleGUI(ttk.Button):
    """Pole planszy GUI jako przycisk posiadający pole planszy właściwej"""

    KOLORY = {
        "puste": "powder blue",
        "puste-active": "light cyan",
        "pudło": "DeepSkyBlue3",
        "pudło-active": "deep sky blue",
        "trafione": "light coral",
        "trafione-active": "light pink",
    }

    def __init__(self, pole, rodzic, *args, **kwargs):
        super().__init__(rodzic, *args, **kwargs)
        self.pole = pole


class PlanszaGUI(ttk.Frame):
    """GUI dla planszy - szczegółowa implementacja w klasach potomnych"""

    ALFABET = {
        1: "A",
        2: "B",
        3: "C",
        4: "D",
        5: "E",
        6: "F",
        7: "G",
        8: "H",
        9: "I",
        10: "J",
        11: "K",
        12: "L",
        13: "M",
        14: "N",
        15: "O",
        16: "P",
        17: "Q",
        18: "R",
        19: "S",
        20: "T",
        21: "U",
        22: "V",
        23: "W",
        24: "X",
        25: "Y",
        26: "Z",
        27: "AA",
        28: "AB",
        29: "AC",
        30: "AD"
    }

    def __init__(self, rodzic, kolumny, rzedy, tytul):
        super().__init__(rodzic, padding=10)
        self.tytul = tytul
        self.plansza = Plansza(kolumny, rzedy)
        self.pola_gui = [[0 for kolumna in range(self.plansza.kolumny)] for rzad in range(self.plansza.rzedy)]  # matryca (lista rzędów (list)) obiektów klasy PoleGUI (tu inicjalizowanych jako "0")
        # GUI
        self.grid()
        self.styl = ttk.Style()
        self.ramka_pol = ttk.LabelFrame(self, text=self.tytul, padding=10)
        self.ramka_pol.grid()
        self.ustaw_style()
        self.buduj_etykiety()
        self.buduj_pola()

    def ustaw_style(self):
        """Definiuje style dla pól"""
        # puste
        self.styl.configure(
            "Puste.TButton",
            relief="sunken",
            background=PoleGUI.KOLORY["puste"]
        )
        self.styl.map(
            "Puste.TButton",
            relief=[('active', 'sunken'), ('disabled', 'sunken')],
            background=[('active', PoleGUI.KOLORY["puste-active"]), ('disabled', "gray")]
        )
        # pudło
        self.styl.configure(
            "Pudło.TButton",
            relief="sunken",
            background=PoleGUI.KOLORY["pudło"]
        )
        self.styl.map(
            "Pudło.TButton",
            relief=[('active', 'sunken'), ('disabled', 'sunken')],
            background=[('active', PoleGUI.KOLORY["pudło-active"]), ('disabled', "gray")]
        )
        # trafione
        self.styl.configure(
            "Trafione.TButton",
            # relief="sunken",
            background=PoleGUI.KOLORY["trafione"]
        )
        self.styl.map(
            "Trafione.TButton",
            # relief=[('active', 'sunken'), ('disabled', 'sunken')],
            background=[('active', PoleGUI.KOLORY["trafione-active"]), ('disabled', "gray")]
        )

    def buduj_etykiety(self):
        """Buduje etykiety kolumn i rzędów"""
        for kolumna in range(self.plansza.kolumny):
            ttk.Label(
                self.ramka_pol,
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
                self.ramka_pol,
                text=self.ALFABET[rzad + 1]
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
                    self.plansza.podaj_pole(kolumna, rzad),
                    self.ramka_pol,
                    text="",
                    width=2
                )
                pole_gui.grid(
                    column=kolumna,
                    row=rzad,
                    sticky=tk.W
                    # pady=1,
                    # padx=1
                )
                self.pola_gui[j][i] = pole_gui

    def podaj_pole_gui(self, kolumna, rzad):
        """Podaje wskazane pole (przycisk)"""
        return self.pola_gui[rzad - 1][kolumna - 1]


class PlanszaGospodarza(PlanszaGUI):
    """GUI dla planszy gospodarza"""

    def __init__(self, rodzic, kolumny, rzedy, tytul="Gospodarz"):
        super().__init__(rodzic, kolumny, rzedy, tytul)
        self.odkryj_pola()
        # testy
        self.oznacz_pudlo(self.podaj_pole_gui(5, 5))
        statek = self.plansza.statki[0]
        self.oznacz_trafione(self.podaj_pole_gui(*statek.polozenie.podaj_wspolrzedne()))

    def odkryj_pola(self):
        """Odkrywa wszystkie pola planszy"""
        for i in range(self.plansza.kolumny):
            for j in range(self.plansza.rzedy):
                kolumna, rzad = i + 1, j + 1
                pole_gui = self.podaj_pole_gui(kolumna, rzad)
                statek = self.plansza.podaj_statek(pole_gui.pole)
                if pole_gui.pole.znacznik in (Pole.ZNACZNIKI["puste"], Pole.ZNACZNIKI["obwiednia"]):
                    pole_gui.configure(style="Puste.TButton")
                else:
                    pole_gui.configure(text=statek.SYMBOL)

    def oznacz_pudlo(self, pole_gui):
        """Oznacza podane pole jako pudło"""
        pole_gui.pole.znacznik = Pole.ZNACZNIKI["pudło"]
        pole_gui.configure(style="Pudło.TButton", text="•")

    def oznacz_trafione(self, pole_gui):
        """Oznacza podane pole jako trafione"""
        pole_gui.pole.znacznik = Pole.ZNACZNIKI["trafione"]
        pole_gui.configure(style="Trafione.TButton")


class PlanszaGoscia(PlanszaGUI):
    """GUI dla planszy gościa"""

    def __init__(self, rodzic, kolumny, rzedy, tytul="Gość"):
        super().__init__(rodzic, kolumny, rzedy, tytul)
        self.rejestruj_callback()

    def rejestruj_callback(self):
        """Rejestruje na_klikniecie() z wszystkimi polami"""
        for i in range(self.plansza.kolumny):
            for j in range(self.plansza.rzedy):
                kolumna, rzad = i + 1, j + 1
                # lambda bez własnych argumentów (w formie: lambda: self.na_klikniecie(kolumna, rzad) nie zadziała prawidłowo w tym przypadku - zmienne przekazywane do każdej funkcji (anonimowej czy nie - bez różnicy) są zawsze ewaluowane dopiero w momencie wywołania tej funkcji, tak więc w tym przypadku w danej iteracji pętli zostają przekazane zmienne "i" i "j" (nazwy) a nie ich wartości - wartości zostaną ewaluowane dopiero w momencie wywołania callbacka (czyli naciśnięcia przycisku) i będzie to wartość z ostatniej iteracji dla wszystkich przycisków, więcej tutaj: https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture/23557126))
                self.podaj_pole_gui(kolumna, rzad).configure(command=lambda x=kolumna, y=rzad: self.na_klikniecie(x, y))

    def na_klikniecie(self, kolumna, rzad):
        """Callback każdego pola uruchamiany po naciśnięciu"""
        print("Kliknięcie w polu: ({}{})".format(self.ALFABET[rzad], kolumna))
        pole_gui = self.podaj_pole_gui(kolumna, rzad)
        if pole_gui.pole.znacznik in (Pole.ZNACZNIKI["puste"], Pole.ZNACZNIKI["obwiednia"], Pole.ZNACZNIKI["pudło"]):
            pole_gui.configure(style="Puste.TButton")
            print("pudło")
        else:
            pole_gui.configure(text="&")
            # pole_gui.state(["disabled"])
            print("TRAFIONY!")


def main():
    """Uruchamia skrypt"""
    root = tk.Tk()
    root.title("Statki")

    rama = ttk.Frame(root)
    rama.grid()

    # przy ekranie 1920x1200 sensowne wymiary (jednej) planszy to od 5x5 do 50x30, przy dwóch planszach (gracz+przeciwnik) to 5x5 do 25x30 ==> TODO: zaimplementować w GUI
    kolumny, rzedy = 25, 30
    host = PlanszaGospodarza(rama, kolumny, rzedy)
    host.grid(column=0, row=0)
    guest = PlanszaGoscia(rama, kolumny, rzedy)
    guest.grid(column=1, row=0)
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
