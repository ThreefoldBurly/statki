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
        self.zawartosc = ttk.Frame(root, padding=10)
        self.zawartosc.grid(column=0, row=0)

    def buduj_sie(self):
        for i in range(self.plansza.kolumny):
            for j in range(self.plansza.rzedy):
                self.matryca_pol[j][i] = ttk.Button(self.zawartosc, text="S", width=2).grid(column=i, row=j, sticky=W, pady=2, padx=2)


def main():
    """
    Uruchamia skrypt
    """
    # przygotowanie planszy
    plansza = Plansza(20, 20)
    plansza.drukuj_sie()
    plansza.wypelnij_statkami()
    plansza.drukuj_sie()

    # GUI
    root = Tk()
    gui = PlanszaGUI(root, plansza)
    gui.buduj_sie()
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
