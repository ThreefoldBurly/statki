#!/usr/bin/env python3

"""
Graficzny interfejs użytkownika
"""

import tkinter as tk
from tkinter import ttk

from plansza import Plansza, Pole
from mechanika import Gracz


def main():
    """Uruchamia grę."""
    root = tk.Tk()
    root.title("Statki")

    gra_gui = ttk.Frame(root)
    gra_gui.grid()
    kf = ttk.Frame(gra_gui, padding=(0, 0, 10, 0))
    kf.grid()
    etyramka = ttk.Labelframe(kf, text="Flota", padding=5)
    etyramka.grid()
    # ttk.Label(
    #     etyramka,
    #     text="Wybierz statek:"
    # ).grid(
    # row=0,
    # column=0,
    # sticky=tk.W
    # )

    drzewo = ttk.Treeview(etyramka)
    drzewo.grid(
        row=0,
        column=0,
        sticky=tk.W
    )
    drzewo.insert("", "0", "item1", text="First Item")

    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()
