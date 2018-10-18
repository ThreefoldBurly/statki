"""

    statki.gui.plansza
    ~~~~~~~~~~~~~~~~~~

    Graficzna reprezentacja plansz: gracza i przeciwnika.

"""

import tkinter as tk
from tkinter import ttk
from collections import namedtuple

from statki.plansza import Plansza, Pole, Salwa
from .sekcja import Sekcja


class PoleGUI(ttk.Button):
    """Graficzna reprezentacja pola planszy."""

    Glify = namedtuple("Glify", "pudlo trafiony")
    GLIFY = Glify(pudlo="•", trafiony="�")

    Kolory = namedtuple("Kolory", [
        "woda", "woda_active", "pudlo", "pudlo_active", "trafiony", "trafiony_active",
        "zatopiony", "zatopiony_active", "wybrany", "wybrany_active", "wybrany_trafiony",
        "wybrany_trafiony_active", "atak_active"
    ])
    KOLORY = Kolory(
        woda="powder blue",
        woda_active="light cyan",
        pudlo="DeepSkyBlue3",
        pudlo_active="deep sky blue",
        trafiony="light coral",
        trafiony_active="light pink",
        zatopiony="ivory4",
        zatopiony_active="ivory3",
        wybrany="khaki2",
        wybrany_active="lemon chiffon",
        wybrany_trafiony="OrangeRed2",
        wybrany_trafiony_active="chocolate1",
        atak_active="DarkSeaGreen1"
    )

    Style = namedtuple(
        "Style",
        "woda pudlo trafiony zatopiony wybrany wybrany_trafiony atak bazowy"
    )
    STYLE = Style(
        woda="Woda.TButton",
        pudlo="Pudło.TButton",
        trafiony="Trafiony.TButton",
        zatopiony="Zatopiony.TButton",
        wybrany="Wybrany.TButton",
        wybrany_trafiony="Wybrany&Trafiony.TButton",
        atak="Atak.TButton",
        bazowy="TButton"
    )

    def __init__(self, rodzic, pole, *args, **kwargs):
        super().__init__(rodzic, *args, **kwargs)
        self.pole = pole


class PlanszaGUI(Sekcja):  # nie powinna być powiększana.
    """
    Graficzna reprezentacja planszy - szczegółowa implementacja w klasach potomnych.
    """

    def __init__(self, rodzic, odstep_zewn, odstep_wewn, tytul, **kwargs):
        super().__init__(rodzic, odstep_zewn, odstep_wewn, tytul)
        self.gra = kwargs["gra"]
        # self.tytul = tytul
        self.pola_gui = [[0 for kolumna in range(self.gra.plansza.kolumny)]
                         for rzad in range(self.gra.plansza.rzedy)]  # matryca (lista rzędów (list)) obiektów klasy PoleGUI (tu inicjalizowanych jako "0")
        self.ustaw_style()
        self.buduj_etykiety()
        self.buduj_pola()

    def ustaw_style(self):
        """Definiuje style dla pól."""
        self.styl = ttk.Style()
        # woda
        self.styl.configure(
            PoleGUI.STYLE.woda,
            relief="sunken",
            background=PoleGUI.KOLORY.woda
        )
        self.styl.map(
            PoleGUI.STYLE.woda,
            relief=[("active", "sunken"), ("disabled", "sunken")],
            background=[("active", PoleGUI.KOLORY.woda_active), ("disabled", "gray")]
        )
        # pudło
        self.styl.configure(
            PoleGUI.STYLE.pudlo,
            relief="sunken",
            background=PoleGUI.KOLORY.pudlo
        )
        self.styl.map(
            PoleGUI.STYLE.pudlo,
            relief=[("active", "sunken"), ("disabled", "sunken")],
            background=[("active", PoleGUI.KOLORY.pudlo_active), ("disabled", "gray")]
        )
        # trafione
        self.styl.configure(
            PoleGUI.STYLE.trafiony,
            background=PoleGUI.KOLORY.trafiony
        )
        self.styl.map(
            PoleGUI.STYLE.trafiony,
            background=[("active", PoleGUI.KOLORY.trafiony_active), ("disabled", "gray")]
        )
        # zatopione
        self.styl.configure(
            PoleGUI.STYLE.zatopiony,
            relief="sunken",
            foreground="white",
            background=PoleGUI.KOLORY.zatopiony
        )
        self.styl.map(
            PoleGUI.STYLE.zatopiony,
            relief=[("active", "sunken"), ("disabled", "sunken")],
            foreground=[("active", "white"), ("disabled", "white")],
            background=[("active", PoleGUI.KOLORY.zatopiony_active), ("disabled", "gray")]
        )

    def buduj_etykiety(self):
        """Buduje etykiety kolumn i rzędów."""
        for kolumna in range(self.gra.plansza.kolumny):
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
        for rzad in range(self.gra.plansza.rzedy):
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
        for i in range(self.gra.plansza.kolumny):
            for j in range(self.gra.plansza.rzedy):
                kolumna, rzad = i + 1, j + 1
                pole_gui = PoleGUI(
                    self.etyramka,
                    self.gra.plansza.podaj_pole(kolumna, rzad),
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
        pole_gui.pole.znacznik = Pole.ZNACZNIKI.pudlo
        pole_gui.configure(style=PoleGUI.STYLE.pudlo, text=PoleGUI.GLIFY.pudlo)

    def oznacz_trafione(self, pole_gui, symbol=None):
        """Oznacza podane pole jako trafione."""
        pole_gui.pole.znacznik = Pole.ZNACZNIKI.trafiony
        if symbol:
            pole_gui.configure(style=PoleGUI.STYLE.trafiony, text=symbol)
        else:
            pole_gui.configure(style=PoleGUI.STYLE.trafiony)

    def zatop_statek(self, statek, z_symbolami=False):
        """Oznacza pola wskazanego statku jako zatopione."""
        for pole in statek.pola:
            pole.znacznik = Pole.ZNACZNIKI.zatopiony
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            pole_gui.configure(style=PoleGUI.STYLE.zatopiony)
            if z_symbolami:
                pole_gui.configure(text=statek.RANGA_BAZOWA.symbol)

        self.gra.plansza.zatopione.append(statek)
        self.gra.plansza.niezatopione.remove(statek)


class PlanszaGracza(PlanszaGUI):
    """Graficzna reprezentacja planszy gracza."""

    def __init__(self, rodzic, odstep_zewn, odstep_wewn, tytul="Gracz", **kwargs):
        super().__init__(rodzic, odstep_zewn, odstep_wewn, tytul, **kwargs)
        self.ka = None  # sekcja kontroli ataku przekazywana przez GręGUI
        self.kf = None  # sekcja kontroli floty przekazywana przez GręGUI
        self.ustaw_style_gracza()
        self.powiaz_callbacki()
        self.odkryj_wszystkie_pola()

        # testy
        # statek = self.gra.plansza.statki[0]
        # self.oznacz_trafione(self.podaj_pole_gui(*statek.polozenie.podaj_wspolrzedne()))
        # statek = self.gra.plansza.statki[3]
        # self.zatop_statek(statek)

    def ustaw_style_gracza(self):
        """Definiuj style dla pól."""
        # wybrane
        self.styl.configure(
            PoleGUI.STYLE.wybrany,
            background=PoleGUI.KOLORY.wybrany
        )
        self.styl.map(
            PoleGUI.STYLE.wybrany,
            background=[("active", PoleGUI.KOLORY.wybrany_active), ("disabled", "gray")]
        )
        # wybrane&trafione
        self.styl.configure(
            PoleGUI.STYLE.wybrany_trafiony,
            background=PoleGUI.KOLORY.wybrany_trafiony
        )
        self.styl.map(
            PoleGUI.STYLE.wybrany_trafiony,
            background=[("active", PoleGUI.KOLORY.wybrany_trafiony_active), ("disabled", "gray")]
        )

    def powiaz_callbacki(self):
        """Powiąż callbacki."""
        # wszystkie pola
        for i in range(self.gra.plansza.kolumny):
            for j in range(self.gra.plansza.rzedy):
                kolumna, rzad = i + 1, j + 1
                pole_gui = self.podaj_pole_gui(kolumna, rzad)
                # lambda bez własnych argumentów (w formie: lambda: self.na_klikniecie(kolumna, rzad) nie zadziała prawidłowo w tym przypadku - zmienne przekazywane do każdej funkcji (anonimowej czy nie - bez różnicy) są zawsze ewaluowane dopiero w momencie wywołania tej funkcji, tak więc w tym przypadku w danej iteracji pętli zostają przekazane zmienne "i" i "j" (nazwy) a nie ich wartości - wartości zostaną ewaluowane dopiero w momencie wywołania callbacka (czyli naciśnięcia przycisku) i będzie to wartość z ostatniej iteracji dla wszystkich przycisków, więcej tutaj: https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture/23557126))
                pole_gui.configure(command=lambda x=kolumna, y=rzad: self.na_klikniecie(x, y))  # lambda konieczna, bo nie da się tego obsłużyć tak jak niżej z bind() - w przypadku przypisywania callbacków opcją 'command' nie ma przekazywania obiektu zdarzenia, z którego można by pobrać współrzędne pola
                pole_gui.bind("<Enter>", self.na_wejscie)
                pole_gui.bind("<Leave>", self.na_wyjscie)
        # okno główne
        self.winfo_toplevel().bind("[", self.na_nawias_kw_lewy)
        self.winfo_toplevel().bind("]", self.na_nawias_kw_prawy)

    # CALLBACK wszystkich pól
    def na_klikniecie(self, kolumna, rzad):
        """
        Wybierz kliknięty statek, kasując wybór poprzedniego. Zatopione statki nie są wybierane. Ten sam mechanizm jest uruchamiany po wyborze statku w sekcjach kontroli ataku i floty.
        """
        statek = self.gra.plansza.podaj_statek(self.podaj_pole_gui(kolumna, rzad).pole)
        self.zmien_statek(statek)

        print("Kliknięcie w polu: ({}{})".format(Plansza.ALFABET[kolumna], rzad))  # test

    # CALLBACK wszystkich pól
    def na_wejscie(self, event=None):
        """Wyświetl pozycję pola w sekcji kontroli floty."""
        self.kf.pozycja_pola.set(event.widget.pole)

    # CALLBACK wszystkich pól
    def na_wyjscie(self, event=None):
        """Kasuj wyświetlaną pozycję pola w sekcji kontroli floty."""
        self.kf.pozycja_pola.set("")

    # CALLBACK okna głównego
    def na_nawias_kw_lewy(self, event=None):
        """Przewiń wybrany statek do tyłu."""
        if len(self.gra.tura.napastnicy) > 1:  # jeśli jest co przewijać
            indeks = self.gra.tura.napastnicy.index(self.gra.tura.runda.napastnik)
            if indeks > 0:  # jeśli nie jesteśmy na początku kolejki
                statek = self.gra.tura.napastnicy[indeks - 1]
            else:
                statek = self.gra.tura.napastnicy[-1]
            self.zmien_statek(statek)

    # CALLBACK okna głównego
    def na_nawias_kw_prawy(self, event=None):
        """Przewiń wybrany statek do przodu."""
        if len(self.gra.tura.napastnicy) > 1:  # jeśli jest co przewijać
            indeks = self.gra.tura.napastnicy.index(self.gra.tura.runda.napastnik)
            if indeks < len(self.gra.tura.napastnicy) - 1:  # jeśli nie jesteśmy na końcu kolejki
                statek = self.gra.tura.napastnicy[indeks + 1]
            else:
                statek = self.gra.tura.napastnicy[0]
            self.zmien_statek(statek)

    def zmien_statek(self, statek):
        """Zmień wybrany statek"""
        if statek in self.gra.tura.napastnicy and self.gra.tura.runda.mozna_zmienic_napastnika:
            self.kasuj_wybor_statku(self.gra.tura.runda.napastnik)
            self.wybierz_statek(statek)

    def wybierz_statek(self, statek):
        """Wybierz statek na planszy"""
        for pole in statek.pola:
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            if pole_gui.pole.znacznik == Pole.ZNACZNIKI.trafiony:
                pole_gui.configure(style=PoleGUI.STYLE.wybrany_trafiony)
            else:
                pole_gui.configure(style=PoleGUI.STYLE.wybrany)
        self.gra.tura.runda.ustaw_napastnika(statek)
        # kontrola widżetów w innych sekcjach
        self.ka.combo_statku.set(statek)
        self.ka.ustaw_combo_salwy()
        if len(self.kf.drzewo_g.selection()) > 0:
            self.kf.drzewo_g.selection_remove(self.kf.drzewo_g.selection()[0])
        iid = str(statek.polozenie)
        self.kf.drzewo_g.selection_add(iid)
        if self.kf.drzewo_g.bbox(iid, column="statek") == "":
            self.kf.drzewo_g.see(iid)

    def kasuj_wybor_statku(self, statek):
        """Kasuj wybór statku na planszy"""
        for pole in statek.pola:
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            if pole_gui.pole.znacznik == Pole.ZNACZNIKI.trafiony:
                pole_gui.configure(style=PoleGUI.STYLE.trafiony)
            else:
                pole_gui.configure(style=PoleGUI.STYLE.bazowy)

    def odkryj_wszystkie_pola(self):
        """Odkryj wszystkie pola planszy."""
        for rzad in self.pola_gui:
            for pole_gui in rzad:
                if pole_gui.pole.znacznik in (Pole.ZNACZNIKI.pusty, Pole.ZNACZNIKI.obwiednia):
                    pole_gui.configure(style=PoleGUI.STYLE.woda)
                else:
                    statek = self.gra.plansza.podaj_statek(pole_gui.pole)
                    pole_gui.configure(text=statek.RANGA_BAZOWA.symbol)

    def wylacz_zablokowane_statki(self):
        """
        Wyłącz pola zablokowanych statków. Uruchamiana w sekcji kontroli ataku razem z blokadą zmiany napastnika w momencie wykonania pierwszej salwy.
        """
        napastnik = self.gra.tura.runda.napastnik
        for statek in [statek for statek in self.gra.tura.napastnicy if statek != napastnik]:
            self.zmien_stan_statku(statek, "disabled")

    def wlacz_zablokowane_statki(self):
        """
        Włącz pola zablokowanych statków. Uruchamiana w sekcji kontroli gry na koniec rundy - już po dodaniu nowej rundy w turze, ale jeszcze PRZED wyborem nowego napastnika na początek tury.
        """
        for statek in self.gra.tura.napastnicy:
            self.zmien_stan_statku(statek, "!disabled")

    def zmien_stan_statku(self, statek, stan):
        """Zmień stan podanego statku."""
        for pole in statek.pola:
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            pole_gui.state([stan])

    def oznacz_salwy(self, salwy):
        """Oznacz otrzymane salwy. Obsłuż ewentualne zatopienia."""
        pass  # TODO


class PlanszaPrzeciwnika(PlanszaGUI):
    """Graficzna reprezentacja planszy przeciwnika."""

    def __init__(self, rodzic, odstep_zewn, odstep_wewn, tytul="Przeciwnik", **kwargs):
        super().__init__(rodzic, odstep_zewn, odstep_wewn, tytul, **kwargs)
        self.pg = None  # przekazywane przez GręGUI
        self.ka = None  # jw.
        self.kf = None  # jw.
        self.kg = None  # jw.
        self.komunikator = None  # jw.
        self.ustaw_style_przeciwnika()
        self.powiaz_callbacki()
        self.wlacz_atak()

    def ustaw_style_przeciwnika(self):
        """Definiuj style dla pól."""
        # atak
        self.styl.map(
            PoleGUI.STYLE.atak,
            background=[("active", PoleGUI.KOLORY.atak_active)]
        )

    def wlacz_atak(self):
        """Włącz nieodkryte pola oraz celownik."""
        for rzad in self.pola_gui:
            for pole_gui in rzad:
                if pole_gui.configure("style")[-1] in [PoleGUI.STYLE.bazowy, ""]:
                    pole_gui.state(["!disabled"])
                    pole_gui.configure(style=PoleGUI.STYLE.atak)

    def wylacz_atak(self):
        """Wyłącza nieodkryte pola oraz celownik."""
        for rzad in self.pola_gui:
            for pole_gui in rzad:
                if pole_gui.configure("style")[-1] == PoleGUI.STYLE.atak:
                    pole_gui.state(["disabled"])
                    pole_gui.configure(style=PoleGUI.STYLE.bazowy)

    def powiaz_callbacki(self):
        """Powiąż callbacki we wszystkich polach."""
        for i in range(self.gra.plansza.kolumny):
            for j in range(self.gra.plansza.rzedy):
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
        W zależności od wybranej orientacji w sekcji kontroli ataku oddaj salwę w wybrane pola oraz wyświetl komunikaty o salwie i zatopieniu.
        """
        if self.pg.gra.tura.runda.mozna_atakowac:
            ilosc_zatopionych = len(self.gra.plansza.zatopione)
            # 1 pole
            if self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.C:
                self.oddaj_salwe((kolumna, rzad))
            # 2 pola (w prawo)
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.E:
                self.oddaj_salwe((kolumna, rzad), (kolumna + 1, rzad))
            # 2 pola (w dół)
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.S:
                self.oddaj_salwe((kolumna, rzad), (kolumna, rzad + 1))
            # 2 pola (w lewo)
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.W:
                self.oddaj_salwe((kolumna, rzad), (kolumna - 1, rzad))
            # 2 pola (w górę)
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.N:
                self.oddaj_salwe((kolumna, rzad), (kolumna, rzad - 1))
            # 3 pola poziomo
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.WE:
                self.oddaj_salwe((kolumna, rzad), (kolumna - 1, rzad), (kolumna + 1, rzad))
            # 3 pola pionowo
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.NS:
                self.oddaj_salwe((kolumna, rzad), (kolumna, rzad - 1), (kolumna, rzad + 1))
            # 3 pola L
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.NE:
                self.oddaj_salwe((kolumna, rzad), (kolumna, rzad - 1), (kolumna + 1, rzad))
            # 3 pola Г
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.SE:
                self.oddaj_salwe((kolumna, rzad), (kolumna, rzad + 1), (kolumna + 1, rzad))
            # 3 pola Ꞁ
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.SW:
                self.oddaj_salwe((kolumna, rzad), (kolumna - 1, rzad), (kolumna, rzad + 1))
            # 3 pola ⅃
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.NW:
                self.oddaj_salwe((kolumna, rzad), (kolumna - 1, rzad), (kolumna, rzad - 1))

            oddana_salwa = self.pg.gra.tura.runda.salwy_oddane[-1]
            napastnik = self.pg.gra.tura.runda.napastnik
            # komunikaty
            self.komunikator.o_salwie(oddana_salwa, napastnik)
            if len(self.gra.plansza.zatopione) > ilosc_zatopionych:  # jeśli było zatopienie
                ofiara = self.gra.plansza.zatopione[-1]
                self.komunikator.o_zatopieniu(ofiara, napastnik)

        print("Kliknięcie w polu: ({}{})".format(Plansza.ALFABET[kolumna], rzad))  # test

    def oddaj_salwe(self, *wspolrzedne):
        """Oddaj salwę w pola o podanych współrzędnych."""
        if len(self.gra.tura.runda.salwy_oddane) == 0:
            self.blokuj_zmiane_statku()

        pola_salwy = []
        for kolumna, rzad in wspolrzedne:
            if self.gra.plansza.czy_w_planszy(kolumna, rzad):
                self.odkryj_pole(kolumna, rzad)
            pola_salwy.append(self.gra.plansza.podaj_pole(kolumna, rzad))

        napastnik = self.pg.gra.tura.runda.napastnik
        self.pg.gra.tura.runda.dodaj_salwe_oddana(Salwa(napastnik.polozenie, pola_salwy))
        self.ka.ustaw_combo_salwy()

    def blokuj_zmiane_statku(self):
        """Blokuj w widżetach możliwość zmiany statku po oddaniu pierwszej salwy."""
        self.pg.gra.tura.runda.mozna_zmienic_statek = False
        self.pg.wylacz_zablokowane_statki()
        self.ka.combo_statku.state(["disabled"])
        self.kf.drzewo_g.wyszarz_zablokowane_statki()
        self.kf.przycisk_do_tylu.state(["disabled"])
        self.kf.przycisk_do_przodu.state(["disabled"])

    def odkryj_pole(self, kolumna, rzad):
        """
        Odkryj na planszy pole wg podanych współrzędnych. Zaznacz pudło lub trafienie. Jeśli trzeba, zatop trafiony statek (i odkryj pola jego obwiedni).
        """
        pole_gui = self.podaj_pole_gui(kolumna, rzad)
        if pole_gui.pole.znacznik in (Pole.ZNACZNIKI.pusty, Pole.ZNACZNIKI.obwiednia):
            self.oznacz_pudlo(pole_gui)
        elif pole_gui.pole.znacznik == Pole.ZNACZNIKI.statek:
            self.oznacz_trafione(pole_gui, PoleGUI.GLIFY.trafiony)
            self.kg.aktualizuj_stan_gry("przeciwnika")
            statek = self.gra.plansza.podaj_statek(pole_gui.pole)
            if statek.czy_zatopiony():
                self.zatop_statek(statek, z_symbolami=True)
                self.odkryj_obwiednie(statek)

    def odkryj_obwiednie(self, statek):
        """Odkryj na planszy obwiednie zatopionego statku."""
        for pole in statek.obwiednia:
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            # configure("style") zwraca krotkę, której ostatnim elementem jest nazwa stylu
            if pole_gui.configure("style")[-1] not in (PoleGUI.STYLE.woda, PoleGUI.STYLE.pudlo):
                pole_gui.configure(style=PoleGUI.STYLE.woda)
        # test
        print(statek.o_zatopieniu())

    # CALLBACK wszystkich pól
    def na_wejscie(self, event):
        """
        W zależności od wybranej orientacji w sekcji kontroli ataku zmień celownik (podświetl pola) i aktualizuj pozycje odpowiadających pól w sekcji kontroli ataku.
        """
        if self.pg.gra.tura.runda.mozna_atakowac:
            kolumna, rzad = event.widget.pole.podaj_wspolrzedne()
            # 1 pole
            if self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.C:
                self.aktualizuj_pozycje_pol("wejście", (kolumna, rzad))
            # 2 pola (w prawo)
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.E:
                self.zmien_celownik("active", (kolumna + 1, rzad))
                self.aktualizuj_pozycje_pol("wejście", (kolumna, rzad), (kolumna + 1, rzad))
            # 2 pola (w dół)
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.S:
                self.zmien_celownik("active", (kolumna, rzad + 1))
                self.aktualizuj_pozycje_pol("wejście", (kolumna, rzad), (kolumna, rzad + 1))
            # 2 pola (w lewo)
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.W:
                self.zmien_celownik("active", (kolumna - 1, rzad))
                self.aktualizuj_pozycje_pol("wejście", (kolumna, rzad), (kolumna - 1, rzad))
            # 2 pola (w górę)
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.N:
                self.zmien_celownik("active", (kolumna, rzad - 1))
                self.aktualizuj_pozycje_pol("wejście", (kolumna, rzad), (kolumna, rzad - 1))
            # 3 pola poziomo
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.WE:
                self.zmien_celownik("active", (kolumna - 1, rzad), (kolumna + 1, rzad))
                self.aktualizuj_pozycje_pol(
                    "wejście",
                    (kolumna, rzad),
                    (kolumna - 1, rzad),
                    (kolumna + 1, rzad)
                )
            # 3 pola pionowo
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.NS:
                self.zmien_celownik("active", (kolumna, rzad - 1), (kolumna, rzad + 1))
                self.aktualizuj_pozycje_pol(
                    "wejście",
                    (kolumna, rzad),
                    (kolumna, rzad - 1),
                    (kolumna, rzad + 1)
                )
            # 3 pola L
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.NE:
                self.zmien_celownik("active", (kolumna, rzad - 1), (kolumna + 1, rzad))
                self.aktualizuj_pozycje_pol(
                    "wejście",
                    (kolumna, rzad),
                    (kolumna, rzad - 1),
                    (kolumna + 1, rzad)
                )
            # 3 pola Г
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.SE:
                self.zmien_celownik("active", (kolumna, rzad + 1), (kolumna + 1, rzad))
                self.aktualizuj_pozycje_pol(
                    "wejście",
                    (kolumna, rzad),
                    (kolumna, rzad + 1),
                    (kolumna + 1, rzad)
                )
            # 3 pola Ꞁ
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.SW:
                self.zmien_celownik("active", (kolumna - 1, rzad), (kolumna, rzad + 1))
                self.aktualizuj_pozycje_pol(
                    "wejście",
                    (kolumna, rzad),
                    (kolumna - 1, rzad),
                    (kolumna, rzad + 1)
                )
            # 3 pola ⅃
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.NW:
                self.zmien_celownik("active", (kolumna - 1, rzad), (kolumna, rzad - 1))
                self.aktualizuj_pozycje_pol(
                    "wejście",
                    (kolumna, rzad),
                    (kolumna - 1, rzad),
                    (kolumna, rzad - 1)
                )

    # CALLBACK wszystkich pól
    def na_wyjscie(self, event):
        """
        W zależności od wybranej orientacji w sekcji kontroli ataku zmień celownik i aktualizuj pozycje odpowiadających pól w sekcji kontroli ataku.
        """
        if self.pg.gra.tura.runda.mozna_atakowac:
            kolumna, rzad = event.widget.pole.podaj_wspolrzedne()
            # 1 pole
            if self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.C:
                self.aktualizuj_pozycje_pol("wyjście", (kolumna, rzad))
            # 2 pola (w prawo)
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.E:
                self.zmien_celownik("!active", (kolumna + 1, rzad))
                self.aktualizuj_pozycje_pol("wyjście", (kolumna, rzad), (kolumna + 1, rzad))
            # 2 pola (w dół)
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.S:
                self.zmien_celownik("!active", (kolumna, rzad + 1))
                self.aktualizuj_pozycje_pol("wyjście", (kolumna, rzad), (kolumna, rzad + 1))
            # 2 pola (w lewo)
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.W:
                self.zmien_celownik("!active", (kolumna - 1, rzad))
                self.aktualizuj_pozycje_pol("wyjście", (kolumna, rzad), (kolumna - 1, rzad))
            # 2 pola (w górę)
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.N:
                self.zmien_celownik("!active", (kolumna, rzad - 1))
                self.aktualizuj_pozycje_pol("wyjście", (kolumna, rzad), (kolumna, rzad - 1))
            # 3 pola poziomo
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.WE:
                self.zmien_celownik("!active", (kolumna - 1, rzad), (kolumna + 1, rzad))
                self.aktualizuj_pozycje_pol(
                    "wyjście",
                    (kolumna, rzad),
                    (kolumna - 1, rzad),
                    (kolumna + 1, rzad)
                )
            # 3 pola pionowo
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.NS:
                self.zmien_celownik("!active", (kolumna, rzad - 1), (kolumna, rzad + 1))
                self.aktualizuj_pozycje_pol(
                    "wyjście",
                    (kolumna, rzad),
                    (kolumna, rzad - 1),
                    (kolumna, rzad + 1)
                )
            # 3 pola L
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.NE:
                self.zmien_celownik("!active", (kolumna, rzad - 1), (kolumna + 1, rzad))
                self.aktualizuj_pozycje_pol(
                    "wyjście",
                    (kolumna, rzad),
                    (kolumna, rzad - 1),
                    (kolumna + 1, rzad)
                )
            # 3 pola Г
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.SE:
                self.zmien_celownik("!active", (kolumna, rzad + 1), (kolumna + 1, rzad))
                self.aktualizuj_pozycje_pol(
                    "wyjście",
                    (kolumna, rzad),
                    (kolumna, rzad + 1),
                    (kolumna + 1, rzad)
                )
            # 3 pola Ꞁ
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.SW:
                self.zmien_celownik("!active", (kolumna - 1, rzad), (kolumna, rzad + 1))
                self.aktualizuj_pozycje_pol(
                    "wyjście",
                    (kolumna, rzad),
                    (kolumna - 1, rzad),
                    (kolumna, rzad + 1)
                )
            # 3 pola ⅃
            elif self.ka.combo_orientacji.get() == Salwa.ORIENTACJE.NW:
                self.zmien_celownik("!active", (kolumna - 1, rzad), (kolumna, rzad - 1))
                self.aktualizuj_pozycje_pol(
                    "wyjście",
                    (kolumna, rzad),
                    (kolumna - 1, rzad),
                    (kolumna, rzad - 1)
                )

    def zmien_celownik(self, stan, *wspolrzedne):
        """
        Zmień stan (włącz na wejściu/wyłącz na wyjściu) celownika (pól, w które oddawana jest salwa po naciśnięciu lewego klawisza myszy) wg podanych współrzędnych.
        """
        for kolumna, rzad in wspolrzedne:
            if self.gra.plansza.czy_w_planszy(kolumna, rzad):
                pole_gui = self.podaj_pole_gui(kolumna, rzad)
                pole_gui.state([stan])

    def aktualizuj_pozycje_pol(self, stan, *wspolrzedne):
        """Aktualizuj treść odpowiadających celownikowi pozycji pól w sekcji kontroli ataku."""
        def ustaw_pozycje(stan, pozycja):
            if stan == "wejście":
                pozycja.set(self.gra.plansza.podaj_pole(kolumna, rzad))
            elif stan == "wyjście":
                pozycja.set("")
        # współrzędne sortowane od pola najbardziej na NW do pola najbardziej na SE
        wspolrzedne = sorted(wspolrzedne, key=lambda w: w[0] + w[1])
        for i in range(len(wspolrzedne)):
            kolumna, rzad = wspolrzedne[i]
            if self.gra.plansza.czy_w_planszy(kolumna, rzad):
                if i == 0:
                    ustaw_pozycje(stan, self.ka.pozycje_salwy.pierwsza)
                elif i == 1:
                    ustaw_pozycje(stan, self.ka.pozycje_salwy.druga)
                elif i == 2:
                    ustaw_pozycje(stan, self.ka.pozycje_salwy.trzecia)
