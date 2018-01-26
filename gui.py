#!/usr/bin/env python3

"""
Graficzny interfejs użytkownika
"""

import tkinter as tk
from tkinter import ttk

from statki import Plansza


class PlanszaGUI:
    """GUI dla planszy"""

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

    def __init__(self, root, kolumny, rzedy):
        self.plansza = Plansza(kolumny, rzedy)
        self.matryca_pol = [[0 for kolumna in range(self.plansza.kolumny)] for rzad in range(self.plansza.rzedy)]
        # GUI
        self.ramka_glowna = ttk.Frame(root, padding=10)
        self.ramka_glowna.grid()
        self.ramka_pol = ttk.LabelFrame(self.ramka_glowna, text="Gracz #1", padding=10)
        self.ramka_pol.grid()
        self.ustaw_style()
        self.buduj_etykiety()
        self.buduj_pola()

    # TODO: rozdzielić na osobne metody (style, etykiety, pola)
    @staticmethod
    def ustaw_style():
        """Definiuje style dla pól"""
        styl = ttk.Style()
        styl.configure(
            "Puste.TButton",
            relief="sunken",
            background="powder blue"
        )
        styl.map(
            "Puste.TButton",
            relief=[('active', 'sunken'), ('disabled', 'sunken')],
            background=[('active', 'sky blue'), ('active', 'light blue')],
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
                pole = ttk.Button(
                    self.ramka_pol,
                    text="",
                    width=2,
                    command=lambda x=i + 1, y=j + 1: self.sprawdz_pole(x, y)  # lambda bez własnych argumentów (w formie: lambda: self.sprawdz_pole(i+1, j+1) nie zadziała prawidłowo w tym przypadku - zmienne przekazywane do każdej funkcji (anonimowej czy nie - bez różnicy) są zawsze ewaluowane dopiero w momencie wywołania tej funkcji, tak więc w tym przypadku w danej iteracji pętli zostają przekazane zmienne "i" i "j" (nazwy) a nie ich wartości - wartości zostaną ewaluowane dopiero w momencie wywołania callbacka (czyli naciśnięcia przycisku) i będzie to wartość z ostatniej iteracji dla wszystkich przycisków, więcej tutaj: https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture/23557126)
                )
                pole.grid(
                    column=i + 1,
                    row=j + 1,
                    sticky=tk.W,
                    pady=2,
                    padx=2
                )
                self.matryca_pol[j][i] = pole

    def podaj_pole(self, kolumna, rzad):
        """Podaje wskazane pole (przycisk)"""
        return self.matryca_pol[rzad - 1][kolumna - 1]

    def sprawdz_pole(self, kolumna, rzad):
        """Callback każdego pola uruchamiany po naciśnięciu"""
        print("Kliknięcie w polu: ({}{})".format(self.ALFABET[rzad], kolumna))
        pole = self.podaj_pole(kolumna, rzad)
        if self.plansza.podaj_pole(kolumna, rzad).znacznik in (Plansza.ZNACZNIKI["pusty"], Plansza.ZNACZNIKI["obwiednia"]):
            pole.configure(style="Puste.TButton")
            print("pudło")
        else:
            pole.configure(text="&")
            # pole.state(["disabled"])
            print("TRAFIONY!")


def main():
    """Uruchamia skrypt"""
    root = tk.Tk()
    root.title("Statki")
    gui = PlanszaGUI(root, 25, 30)  # przy ekranie 1920x1200 sensowne wymiary (jednej) planszy to od 5x5 do 50x30, przy dwóch planszach (gracz+przeciwnik) to 5x5 do 25x30 ==> TODO: zaimplementować w GUI
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
