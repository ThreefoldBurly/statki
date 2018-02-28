"""Sekcja okna głównego."""

import tkinter as tk
from tkinter import ttk


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
