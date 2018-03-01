"""

    statki.gui.plansza
    ~~~~~~~~~~~~~~~~~~

    Graficzna reprezentacja plansz: gracza i przeciwnika.

"""

import tkinter as tk
from tkinter import ttk

from statki.plansza import Plansza, Pole, Salwa
from .sekcja import Sekcja


class PoleGUI(ttk.Button):
    """Graficzna reprezentacja pola planszy."""

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
        "atak-active": "DarkSeaGreen1"
    }
    STYLE = {
        "woda": "Woda.TButton",
        "pudło": "Pudło.TButton",
        "trafione": "Trafione.TButton",
        "zatopione": "Zatopione.TButton",
        "wybrane": "Wybrane.TButton",
        "wybrane&trafione": "Wybrane&Trafione.TButton",
        "atak": "Atak.TButton",
        "bazowe": "TButton"
    }

    def __init__(self, rodzic, pole, *args, **kwargs):
        super().__init__(rodzic, *args, **kwargs)
        self.pole = pole


class PlanszaGUI(Sekcja):
    """
    Graficzna reprezentacja planszy - szczegółowa implementacja w klasach potomnych. Nie powinna być powiększana.
    """

    def __init__(self, rodzic, odstep_zewn, odstep_wewn, tytul, **kwargs):
        super().__init__(rodzic, odstep_zewn, odstep_wewn, tytul)
        self.gra = kwargs["gra"]
        # self.tytul = tytul
        self.pola_gui = [[0 for kolumna in range(self.gra.plansza.kolumny)] for rzad in range(self.gra.plansza.rzedy)]  # matryca (lista rzędów (list)) obiektów klasy PoleGUI (tu inicjalizowanych jako "0")
        self.ustaw_style()
        self.buduj_etykiety()
        self.buduj_pola()

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
        pole_gui.pole.znacznik = Pole.ZNACZNIKI["pudło"]
        pole_gui.configure(style=PoleGUI.STYLE["pudło"], text=PoleGUI.GLIFY["pudło"])

    def oznacz_trafione(self, pole_gui, symbol=None):
        """Oznacza podane pole jako trafione."""
        pole_gui.pole.znacznik = Pole.ZNACZNIKI["trafione"]
        if symbol:
            pole_gui.configure(style=PoleGUI.STYLE["trafione"], text=symbol)
        else:
            pole_gui.configure(style=PoleGUI.STYLE["trafione"])

    def zatop_statek(self, statek, z_symbolami=False):
        """Oznacza pola wskazanego statku jako zatopione."""
        for pole in statek.pola:
            pole.znacznik = Pole.ZNACZNIKI["zatopione"]
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            pole_gui.configure(style=PoleGUI.STYLE["zatopione"])
            if z_symbolami:
                pole_gui.configure(text=statek.SYMBOLE[statek.RANGA_BAZOWA])

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
        for i in range(self.gra.plansza.kolumny):
            for j in range(self.gra.plansza.rzedy):
                kolumna, rzad = i + 1, j + 1
                # lambda bez własnych argumentów (w formie: lambda: self.na_klikniecie(kolumna, rzad) nie zadziała prawidłowo w tym przypadku - zmienne przekazywane do każdej funkcji (anonimowej czy nie - bez różnicy) są zawsze ewaluowane dopiero w momencie wywołania tej funkcji, tak więc w tym przypadku w danej iteracji pętli zostają przekazane zmienne "i" i "j" (nazwy) a nie ich wartości - wartości zostaną ewaluowane dopiero w momencie wywołania callbacka (czyli naciśnięcia przycisku) i będzie to wartość z ostatniej iteracji dla wszystkich przycisków, więcej tutaj: https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture/23557126))
                pole_gui = self.podaj_pole_gui(kolumna, rzad)
                pole_gui.configure(command=lambda x=kolumna, y=rzad: self.na_klikniecie(x, y))  # lambda konieczna, bo nie da się tego obsłużyć tak jak niżej z bind() - w przypadku przypisywania callbacków opcją 'command' nie ma przekazywania obiektu zdarzenia, z którego można by pobrać współrzędne pola
                pole_gui.bind("<Enter>", self.na_wejscie)
                pole_gui.bind("<Leave>", self.na_wyjscie)
        # okno główne
        self.winfo_toplevel().bind("[", self.na_nawias_kw_lewy)
        self.winfo_toplevel().bind("]", self.na_nawias_kw_prawy)

    # CALLBACK wszystkich pól
    def na_klikniecie(self, kolumna, rzad):
        """
        Wybiera kliknięty statek, kasując wybór poprzedniego. Zatopione statki nie są wybierane. Ten sam mechanizm jest uruchamiany po wyborze statku w sekcjach kontroli ataku i floty.
        """
        statek = self.gra.plansza.podaj_statek(self.podaj_pole_gui(kolumna, rzad).pole)
        self.zmien_statek(statek)

        print("Kliknięcie w polu: ({}{})".format(Plansza.ALFABET[kolumna], rzad))  # test

    # CALLBACK wszystkich pól
    def na_wejscie(self, event=None):
        """
        Wyświetla pozycję pola w sekcji kontroli floty.
        """
        self.kf.pozycja_pola.set(event.widget.pole)

    # CALLBACK wszystkich pól
    def na_wyjscie(self, event=None):
        """
        Kasuje wyświetlaną pozycję pola w sekcji kontroli floty.
        """
        self.kf.pozycja_pola.set("")

    # CALLBACK okna głównego
    def na_nawias_kw_lewy(self, event=None):
        """
        Przewija wybrany statek do tyłu.
        """
        if len(self.gra.tura.statki) > 1:  # jeśli jest co przewijać
            indeks = self.gra.tura.statki.index(self.gra.tura.runda.statek)
            if indeks > 0:  # jeśli nie jesteśmy na początku kolejki
                statek = self.gra.tura.statki[indeks - 1]
            else:
                statek = self.gra.tura.statki[len(self.gra.tura.statki) - 1]
            self.zmien_statek(statek)

    # CALLBACK okna głównego
    def na_nawias_kw_prawy(self, event=None):
        """
        Przewija wybrany statek do przodu.
        """
        if len(self.gra.tura.statki) > 1:  # jeśli jest co przewijać
            indeks = self.gra.tura.statki.index(self.gra.tura.runda.statek)
            if indeks < len(self.gra.tura.statki) - 1:  # jeśli nie jesteśmy na końcu kolejki
                statek = self.gra.tura.statki[indeks + 1]
            else:
                statek = self.gra.tura.statki[0]
            self.zmien_statek(statek)

    def zmien_statek(self, statek):
        """Zmienia wybrany statek"""
        if statek in self.gra.tura.statki and self.gra.tura.runda.mozna_zmienic_statek:
            self.kasuj_wybor_statku(self.gra.tura.runda.statek)
            self.wybierz_statek(statek)

    def wybierz_statek(self, statek):
        """Wybiera statek na planszy"""
        for pole in statek.pola:
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            if pole_gui.pole.znacznik == Pole.ZNACZNIKI["trafione"]:
                pole_gui.configure(style=PoleGUI.STYLE["wybrane&trafione"])
            else:
                pole_gui.configure(style=PoleGUI.STYLE["wybrane"])
        self.gra.tura.runda.ustaw_statek(statek)
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
        """Kasuje wybór statku na planszy"""
        for pole in statek.pola:
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            if pole_gui.pole.znacznik == Pole.ZNACZNIKI["trafione"]:
                pole_gui.configure(style=PoleGUI.STYLE["trafione"])
            else:
                pole_gui.configure(style=PoleGUI.STYLE["bazowe"])

    def odkryj_wszystkie_pola(self):
        """Odkrywa wszystkie pola planszy."""
        for rzad in self.pola_gui:
            for pole_gui in rzad:
                statek = self.gra.plansza.podaj_statek(pole_gui.pole)
                if pole_gui.pole.znacznik in (Pole.ZNACZNIKI["puste"], Pole.ZNACZNIKI["obwiednia"]):
                    pole_gui.configure(style=PoleGUI.STYLE["woda"])
                else:
                    pole_gui.configure(text=statek.SYMBOLE[statek.RANGA_BAZOWA])

    def wylacz_zablokowane_statki(self):
        """
        Wyłącza pola zablokowanych statków. Uruchamiana w sekcji kontroli ataku razem z blokadą zmiany statku w momencie wykonania pierwszej salwy.
        """
        wybrany_statek = self.gra.tura.runda.statek
        for statek in [statek for statek in self.gra.tura.statki if statek != wybrany_statek]:
            self.zmien_stan_statku(statek, "disabled")

    def wlacz_zablokowane_statki(self):
        """
        Włącza pola zablokowanych statków. Uruchamiana w sekcji kontroli gry na koniec rundy - już po dodaniu nowej rundy w turze, ale jeszcze PRZED wyborem nowego statku na początek tury.
        """
        for statek in self.gra.tura.statki:
            self.zmien_stan_statku(statek, "!disabled")

    def zmien_stan_statku(self, statek, stan):
        """Zmienia stan podanego statek."""
        for pole in statek.pola:
            pole_gui = self.podaj_pole_gui(*pole.podaj_wspolrzedne())
            pole_gui.state([stan])

    def oznacz_salwy(self, salwy):
        """Oznacza otrzymane salwy."""
        pass  # TODO


class PlanszaPrzeciwnika(PlanszaGUI):
    """Graficzna reprezentacja planszy przeciwnika."""

    def __init__(self, rodzic, odstep_zewn, odstep_wewn, tytul="Przeciwnik", **kwargs):
        super().__init__(rodzic, odstep_zewn, odstep_wewn, tytul, **kwargs)
        self.pg = None  # jw.
        self.ka = None  # przekazywane przez GręGUI
        self.kf = None  # jw.
        self.kg = None  # jw.
        self.komunikator = None  # jw.
        self.ustaw_style_przeciwnika()
        self.powiaz_callbacki()
        self.wlacz_atak()

    def ustaw_style_przeciwnika(self):
        """Definiuje style dla pól."""
        # atak
        self.styl.map(
            PoleGUI.STYLE["atak"],
            background=[("active", PoleGUI.KOLORY["atak-active"])]
        )

    def wlacz_atak(self):
        """Włącza nieodkryte pola oraz celownik."""
        for rzad in self.pola_gui:
            for pole_gui in rzad:
                if pole_gui.configure("style")[-1] in [PoleGUI.STYLE["bazowe"], ""]:
                    pole_gui.state(["!disabled"])
                    pole_gui.configure(style=PoleGUI.STYLE["atak"])

    def wylacz_atak(self):
        """Wyłącza nieodkryte pola oraz celownik."""
        for rzad in self.pola_gui:
            for pole_gui in rzad:
                if pole_gui.configure("style")[-1] == PoleGUI.STYLE["atak"]:
                    pole_gui.state(["disabled"])
                    pole_gui.configure(style=PoleGUI.STYLE["bazowe"])

    def powiaz_callbacki(self):
        """Wiąże callbacki we wszystkich polach."""
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
        W zależności od wybranej orientacji w sekcji kontroli ataku oddaje salwę w wybrane pola oraz wyświetla komunikaty o salwie i zatopieniu.
        """
        if self.pg.gra.tura.runda.mozna_atakowac:
            ilosc_zatopionych = len(self.gra.plansza.zatopione)
            # 1 pole
            if self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[0]:
                self.oddaj_salwe((kolumna, rzad))
            # 2 pola (w prawo)
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[1]:
                self.oddaj_salwe((kolumna, rzad), (kolumna + 1, rzad))
            # 2 pola (w dół)
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[2]:
                self.oddaj_salwe((kolumna, rzad), (kolumna, rzad + 1))
            # 2 pola (w lewo)
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[3]:
                self.oddaj_salwe((kolumna, rzad), (kolumna - 1, rzad))
            # 2 pola (w górę)
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[4]:
                self.oddaj_salwe((kolumna, rzad), (kolumna, rzad - 1))
            # 3 pola poziomo
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[5]:
                self.oddaj_salwe((kolumna, rzad), (kolumna - 1, rzad), (kolumna + 1, rzad))
            # 3 pola pionowo
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[6]:
                self.oddaj_salwe((kolumna, rzad), (kolumna, rzad - 1), (kolumna, rzad + 1))
            # 3 pola L
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[7]:
                self.oddaj_salwe((kolumna, rzad), (kolumna, rzad - 1), (kolumna + 1, rzad))
            # 3 pola Г
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[8]:
                self.oddaj_salwe((kolumna, rzad), (kolumna, rzad + 1), (kolumna + 1, rzad))
            # 3 pola Ꞁ
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[9]:
                self.oddaj_salwe((kolumna, rzad), (kolumna - 1, rzad), (kolumna, rzad + 1))
            # 3 pola ⅃
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[10]:
                self.oddaj_salwe((kolumna, rzad), (kolumna - 1, rzad), (kolumna, rzad - 1))

            oddana_salwa = self.pg.gra.tura.runda.salwy_oddane[-1]
            napastnik = self.pg.gra.tura.runda.statek
            # komunikaty
            self.komunikator.o_salwie(oddana_salwa, napastnik)
            if len(self.gra.plansza.zatopione) > ilosc_zatopionych:  # jeśli było zatopienie
                ofiara = self.gra.plansza.zatopione[-1]
                self.komunikator.o_zatopieniu(ofiara, napastnik)

        print("Kliknięcie w polu: ({}{})".format(Plansza.ALFABET[kolumna], rzad))  # test

    def oddaj_salwe(self, *wspolrzedne):
        """Oddaje salwę w pola o podanych współrzędnych."""
        if len(self.gra.tura.runda.salwy_oddane) == 0:
            self.blokuj_zmiane_statku()
        # współrzędne sortowane od pola najbardziej na NW do pola najbardziej na SE
        wspolrzedne = sorted(wspolrzedne, key=lambda w: w[0] + w[1])
        pola_salwy = []
        niewypaly = []
        for kolumna, rzad in wspolrzedne:
            if self.gra.plansza.czy_pole_w_planszy(kolumna, rzad):
                self.odkryj_pole(kolumna, rzad)
                pola_salwy.append(self.gra.plansza.podaj_pole(kolumna, rzad))
            else:
                niewypaly.append((kolumna, rzad))
        oddana_salwa = Salwa(pola_salwy, niewypaly)
        self.pg.gra.tura.runda.salwy_oddane.append(oddana_salwa)
        self.pg.gra.tura.runda.sila_ognia.remove(len(oddana_salwa))
        self.ka.ustaw_combo_salwy()

    def blokuj_zmiane_statku(self):
        """Blokuje możliwość zmiany statku na planszy gracza po oddaniu pierwszej salwy w widżetach."""
        self.pg.gra.tura.runda.mozna_zmienic_statek = False
        self.pg.wylacz_zablokowane_statki()
        self.ka.combo_statku.state(["disabled"])
        self.kf.drzewo_g.wyszarz_zablokowane_statki()
        self.kf.przycisk_do_tylu.state(["disabled"])
        self.kf.przycisk_do_przodu.state(["disabled"])

    def odkryj_pole(self, kolumna, rzad):
        """Odkrywa na planszy pole wg podanych współrzędnych. Zaznacza pudło lub trafienie. Jeśli trzeba, zatapia trafiony statek (i odkrywa pola jego obwiedni)."""
        pole_gui = self.podaj_pole_gui(kolumna, rzad)
        if pole_gui.pole.znacznik in (Pole.ZNACZNIKI["puste"], Pole.ZNACZNIKI["obwiednia"]):
            self.oznacz_pudlo(pole_gui)
        elif pole_gui.pole.znacznik == Pole.ZNACZNIKI["statek"]:
            self.oznacz_trafione(pole_gui, PoleGUI.GLIFY["trafione"])
            self.kg.aktualizuj_stan_gry("przeciwnika")
            statek = self.gra.plansza.podaj_statek(pole_gui.pole)
            if statek.czy_zatopiony():
                self.zatop_statek(statek, z_symbolami=True)
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

    # CALLBACK wszystkich pól
    def na_wejscie(self, event):
        """
        W zależności od wybranej orientacji w sekcji kontroli ataku zmienia celownik (podświetla pola) i aktualizuje pozycje odpowiadających pól w sekcji kontroli ataku.
        """
        if self.pg.gra.tura.runda.mozna_atakowac:
            kolumna, rzad = event.widget.pole.podaj_wspolrzedne()
            # 1 pole
            if self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[0]:
                self.aktualizuj_pozycje_pol("wejście", (kolumna, rzad))
            # 2 pola (w prawo)
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[1]:
                self.zmien_celownik("active", (kolumna + 1, rzad))
                self.aktualizuj_pozycje_pol("wejście", (kolumna, rzad), (kolumna + 1, rzad))
            # 2 pola (w dół)
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[2]:
                self.zmien_celownik("active", (kolumna, rzad + 1))
                self.aktualizuj_pozycje_pol("wejście", (kolumna, rzad), (kolumna, rzad + 1))
            # 2 pola (w lewo)
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[3]:
                self.zmien_celownik("active", (kolumna - 1, rzad))
                self.aktualizuj_pozycje_pol("wejście", (kolumna, rzad), (kolumna - 1, rzad))
            # 2 pola (w górę)
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[4]:
                self.zmien_celownik("active", (kolumna, rzad - 1))
                self.aktualizuj_pozycje_pol("wejście", (kolumna, rzad), (kolumna, rzad - 1))
            # 3 pola poziomo
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[5]:
                self.zmien_celownik("active", (kolumna - 1, rzad), (kolumna + 1, rzad))
                self.aktualizuj_pozycje_pol("wejście", (kolumna, rzad), (kolumna - 1, rzad), (kolumna + 1, rzad))
            # 3 pola pionowo
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[6]:
                self.zmien_celownik("active", (kolumna, rzad - 1), (kolumna, rzad + 1))
                self.aktualizuj_pozycje_pol("wejście", (kolumna, rzad), (kolumna, rzad - 1), (kolumna, rzad + 1))
            # 3 pola L
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[7]:
                self.zmien_celownik("active", (kolumna, rzad - 1), (kolumna + 1, rzad))
                self.aktualizuj_pozycje_pol("wejście", (kolumna, rzad), (kolumna, rzad - 1), (kolumna + 1, rzad))
            # 3 pola Г
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[8]:
                self.zmien_celownik("active", (kolumna, rzad + 1), (kolumna + 1, rzad))
                self.aktualizuj_pozycje_pol("wejście", (kolumna, rzad), (kolumna, rzad + 1), (kolumna + 1, rzad))
            # 3 pola Ꞁ
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[9]:
                self.zmien_celownik("active", (kolumna - 1, rzad), (kolumna, rzad + 1))
                self.aktualizuj_pozycje_pol("wejście", (kolumna, rzad), (kolumna - 1, rzad), (kolumna, rzad + 1))
            # 3 pola ⅃
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[10]:
                self.zmien_celownik("active", (kolumna - 1, rzad), (kolumna, rzad - 1))
                self.aktualizuj_pozycje_pol("wejście", (kolumna, rzad), (kolumna - 1, rzad), (kolumna, rzad - 1))

    # CALLBACK wszystkich pól
    def na_wyjscie(self, event):
        """
        W zależności od wybranej orientacji w sekcji kontroli ataku zmienia celownik (gasi pola) i aktualizuje pozycje odpowiadających pól w sekcji kontroli ataku.
        """
        if self.pg.gra.tura.runda.mozna_atakowac:
            kolumna, rzad = event.widget.pole.podaj_wspolrzedne()
            # 1 pole
            if self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[0]:
                self.aktualizuj_pozycje_pol("wyjście", (kolumna, rzad))
            # 2 pola (w prawo)
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[1]:
                self.zmien_celownik("!active", (kolumna + 1, rzad))
                self.aktualizuj_pozycje_pol("wyjście", (kolumna, rzad), (kolumna + 1, rzad))
            # 2 pola (w dół)
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[2]:
                self.zmien_celownik("!active", (kolumna, rzad + 1))
                self.aktualizuj_pozycje_pol("wyjście", (kolumna, rzad), (kolumna, rzad + 1))
            # 2 pola (w lewo)
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[3]:
                self.zmien_celownik("!active", (kolumna - 1, rzad))
                self.aktualizuj_pozycje_pol("wyjście", (kolumna, rzad), (kolumna - 1, rzad))
            # 2 pola (w górę)
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[4]:
                self.zmien_celownik("!active", (kolumna, rzad - 1))
                self.aktualizuj_pozycje_pol("wyjście", (kolumna, rzad), (kolumna, rzad - 1))
            # 3 pola poziomo
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[5]:
                self.zmien_celownik("!active", (kolumna - 1, rzad), (kolumna + 1, rzad))
                self.aktualizuj_pozycje_pol("wyjście", (kolumna, rzad), (kolumna - 1, rzad), (kolumna + 1, rzad))
            # 3 pola pionowo
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[6]:
                self.zmien_celownik("!active", (kolumna, rzad - 1), (kolumna, rzad + 1))
                self.aktualizuj_pozycje_pol("wyjście", (kolumna, rzad), (kolumna, rzad - 1), (kolumna, rzad + 1))
            # 3 pola L
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[7]:
                self.zmien_celownik("!active", (kolumna, rzad - 1), (kolumna + 1, rzad))
                self.aktualizuj_pozycje_pol("wyjście", (kolumna, rzad), (kolumna, rzad - 1), (kolumna + 1, rzad))
            # 3 pola Г
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[8]:
                self.zmien_celownik("!active", (kolumna, rzad + 1), (kolumna + 1, rzad))
                self.aktualizuj_pozycje_pol("wyjście", (kolumna, rzad), (kolumna, rzad + 1), (kolumna + 1, rzad))
            # 3 pola Ꞁ
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[9]:
                self.zmien_celownik("!active", (kolumna - 1, rzad), (kolumna, rzad + 1))
                self.aktualizuj_pozycje_pol("wyjście", (kolumna, rzad), (kolumna - 1, rzad), (kolumna, rzad + 1))
            # 3 pola ⅃
            elif self.ka.combo_orientacji.get() == self.ka.ORIENTACJE[10]:
                self.zmien_celownik("!active", (kolumna - 1, rzad), (kolumna, rzad - 1))
                self.aktualizuj_pozycje_pol("wyjście", (kolumna, rzad), (kolumna - 1, rzad), (kolumna, rzad - 1))

    def zmien_celownik(self, stan, *wspolrzedne):
        """
        Zmienia stan (włącza na wejściu/wyłącza na wyjściu) celownika (pól, w które oddawana jest salwa po naciśnięciu lewego klawisza myszy) wg podanych współrzędnych.
        """
        for kolumna, rzad in wspolrzedne:
            if self.gra.plansza.czy_pole_w_planszy(kolumna, rzad):
                pole_gui = self.podaj_pole_gui(kolumna, rzad)
                pole_gui.state([stan])

    def aktualizuj_pozycje_pol(self, stan, *wspolrzedne):
        """Aktualizuje treść odpowiadających celownikowi pozycji pól w sekcji kontroli ataku."""
        def ustaw_pozycje(stan, pozycja):
            if stan == "wejście":
                pozycja.set(self.gra.plansza.podaj_pole(kolumna, rzad))
            elif stan == "wyjście":
                pozycja.set("")
        # współrzędne sortowane od pola najbardziej na NW do pola najbardziej na SE
        wspolrzedne = sorted(wspolrzedne, key=lambda w: w[0] + w[1])
        for i in range(len(wspolrzedne)):
            kolumna, rzad = wspolrzedne[i]
            if self.gra.plansza.czy_pole_w_planszy(kolumna, rzad):
                if i == 0:
                    ustaw_pozycje(stan, self.ka.pozycje_salwy.pierwsza)
                elif i == 1:
                    ustaw_pozycje(stan, self.ka.pozycje_salwy.druga)
                elif i == 2:
                    ustaw_pozycje(stan, self.ka.pozycje_salwy.trzecia)
