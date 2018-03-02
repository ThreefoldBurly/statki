"""

    statki.gui.komunikaty
    ~~~~~~~~~~~~~~~~~~~~~

    Sekcja komunikatów znajdująca się na dole głównego interfejsu gry.

"""

import tkinter as tk
from tkinter import ttk

from .plansza import PoleGUI
from . import stale


class PasekKomunikatow(ttk.Frame):
    """
    Pasek wyświetlający komunikaty o grze w polu tekstowym na dole głównego interfejsu gry. Dopuszcza powiększanie w pionie.
    """

    def __init__(self, rodzic, odstep, szer_plansz, wys_plansz):
        super().__init__(rodzic, padding=odstep)
        self.szer_plansz, self.wys_plansz = szer_plansz, wys_plansz  # # ilość kolumn, ilość rzędów

        self.ustal_tlo_sytemowe()
        self.buduj_pole_tekstowe()
        self.wstaw_suwak()

    def podaj_wysokosc(self):
        """
        Podaje wysokość. Niezbędna wysokość uzależniona jest od wysokości plansz (oraz drzewa w sekcji kontroli floty) i została ustalona po testach.
        """
        wysokosci = {
            8: 17,
            9: 15,
            10: 13,
            11: 11,
            12: 10,
            13: 9,
            14: 8,
            15: 6,
            16: 5,
            17: 5,
            18: 5,
            19: 4,
            20: 5,
            21: 5,
            22: 5,
            23: 4,
            24: 5,
            25: 5,
            26: 5,
            27: 4,
            28: 5,
            29: 5,
            30: 4
        }
        return wysokosci[self.wys_plansz]

    def podaj_szerokosc(self):
        """Podaje szerokość."""
        # z testów wynikło, że dla bazowej szerokości planszy równej 8 kolumn prawidłowa szerokość pola tekstowego to 77 znaków i że z każdą dodatkową kolumną planszy pole powinno rosnąć o 7.5 znaku w szerz
        korekta = round(7.5 * (self.szer_plansz - 8))
        return 77 + korekta

    def buduj_pole_tekstowe(self):
        """Buduje pole tekstowe."""
        self.tekst = PoleTekstowe(
            self,
            width=self.podaj_szerokosc(),
            height=self.podaj_wysokosc(),
            font=stale.CZCIONKI["mała"],
            wrap=tk.WORD,
            bg=self.TLO_SYSTEMOWE,
            state=tk.DISABLED
        )
        self.tekst.grid(column=0, row=0, sticky="ns")

    def ustal_tlo_sytemowe(self):
        """Sprawdza kolor tla systemowego i zapisuje w stałej"""
        self.TLO_SYSTEMOWE = self.winfo_toplevel().cget("bg")

    def wstaw_suwak(self):
        """Wstawia pionowy suwak."""
        suwak = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tekst.yview)
        suwak.grid(column=1, row=0, sticky="ns")
        self.tekst.configure(yscrollcommand=suwak.set)


class PoleTekstowe(tk.Text):
    """
    Pole tekstowe Tkintera z ustawionymi tagami, zmodyfikowane o metody, które opakowują podstawe metody edycji tak, by nie trzeba było za każdym razem przed edycją przestawiać widżeta w stan `normal` i po edycji w stan `disabled` (co jest konieczne, ponieważ tk.Text nie ma defaultowo trybu readonly, a tylko `normal` i `disabled`, podczas którego nie można nic zmieniać w widżecie, również programistycznie.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<1>", lambda event: self.focus_set())  # to powiązanie przywraca możliwość selekcji tekstu (np. dla skopiowanie) po zablokowaniu (wzięte stąd: https://stackoverflow.com/questions/10817917/how-to-disable-input-to-a-text-widget-but-allow-programatic-input)
        self.ustaw_tagi()

    def ro_insert(self, *args, **kwargs):
        """Readonly insert - przesłonięcie metody rodzica."""
        self.configure(state=tk.NORMAL)
        self.insert(*args, **kwargs)
        self.configure(state=tk.DISABLED)

    def ro_delete(self, *args, **kwargs):
        """Readonly delete - przesłonięcie metody rodzica."""
        self.configure(state=tk.NORMAL)
        self.delete(*args, **kwargs)
        self.configure(state=tk.DISABLED)

    def ustaw_tagi(self):
        """Ustawia tagi zapewniające odpowiednie formatowanie komunikatów."""
        self.tag_configure("wyszarzone", foreground=stale.KOLORY["szare"])
        self.tag_configure("wyśrodkowane", justify=tk.CENTER)
        self.tag_configure("pogrubione", font=stale.CZCIONKI["mała-pogrubiona"])
        self.tag_configure("trafione", background=PoleGUI.KOLORY["trafione"])
