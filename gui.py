#!/usr/bin/env python3

"""
Graficzny interfejs użytkownika
"""

from tkinter import *
from tkinter import ttk

from statki import Plansza


class PlanszaGUI:
    """GUI dla planszy"""

    def __init__(self, root, plansza):
        super(PlanszaGUI, self).__init__()
        self.plansza = plansza
        self.matryca_pol = [[0 for kolumna in range(self.plansza.kolumny)] for rzad in range(self.plansza.rzedy)]
        # GUI
        self.ramka_pol = ttk.Frame(root, padding=10)
        self.ramka_pol.grid(column=0, row=0)

    def buduj_sie(self):
        # etykiety kolumn i rzędów
        for kolumna in range(self.plansza.kolumny):
            ttk.Label(
                self.ramka_pol,
                text=str(kolumna + 1),
                anchor=CENTER
            ).grid(
                row=0,
                column=kolumna + 1,
                sticky=W + E,
                pady=(0, 3)
            )
        for rzad in range(self.plansza.rzedy):
            ttk.Label(
                self.ramka_pol,
                text=str(rzad + 1)
            ).grid(
                column=0,
                row=rzad + 1,
                sticky=E,
                padx=(0, 6)
            )
        # pola
        for i in range(self.plansza.kolumny):
            for j in range(self.plansza.rzedy):
                self.matryca_pol[j][i] = ttk.Button(
                    self.ramka_pol,
                    text="",
                    width=2,
                    command=lambda x=i + 1, y=j + 1: self.sprawdz_pole(x, y)  # lambda bez własnych argumentów (w formie: lambda: self.sprawdz_pole(i+1, j+1) nie zadziała prawidłowo w tym przypadku - zostaną przypisane wartości zmiennych "i" i "j" z ostatniej iteracji do wszystkich przycisków, więcej tutaj: https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture/23557126)
                ).grid(
                    column=i + 1,
                    row=j + 1,
                    sticky=W,
                    pady=2,
                    padx=2
                )

    def sprawdz_pole(self, kolumna, rzad):
        print("Kliknięcie w polu: ({},{})".format(kolumna, rzad))


def main():
    """
    Uruchamia skrypt
    """
    # przygotowanie planszy
    plansza = Plansza(15, 20)
    plansza.drukuj_sie()
    plansza.wypelnij_statkami()
    plansza.drukuj_sie()

    # GUI
    root = Tk()
    root.title("Statki")
    gui = PlanszaGUI(root, plansza)
    gui.buduj_sie()
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
