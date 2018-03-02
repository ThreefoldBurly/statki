"""

    statki.gui.kontrola
    ~~~~~~~~~~~~~~~~~~~

    Sekcje kontroli zajmujące prawą stronę głównego interfejsu gry.

"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import math

from statki.plansza import Statek
from .sekcja import Sekcja
from . import stale


class KontrolaAtaku(Sekcja):
    """
    Sekcja kontroli ataku znajdująca się w prawym górnym rogu głównego interfejsu gry. Dopuszcza powiększanie w poziomie.
    """

    ORIENTACJE = ["•", "•• prawo", "╏ dół", "•• lewo", "╏ góra", "•••", "┇", "L", "Г", "Ꞁ", "⅃"]

    def __init__(self, rodzic, odstep_zewn, odstep_wewn, tytul="Atak", **kwargs):
        super().__init__(rodzic, odstep_zewn, odstep_wewn, tytul)
        self.pg = kwargs["plansza_gracza"]
        self.pp = kwargs["plansza_przeciwnika"]
        self.ustaw_style()
        self.ustaw_etyramke()
        self.buduj_etykiety()
        self.buduj_comboboksy()
        self.przestaw_na_readonly()
        self.pozycje_salwy = PozycjeSalwy(self.etyramka)
        self.powiaz_callbacki()

    def ustaw_style(self):
        """Ustawia style dla widżetów"""
        self.styl = ttk.Style()
        self.styl.configure("KA.TCombobox")
        self.styl.map(
            "KA.TCombobox",
            fieldbackground=[("readonly", "white")]
        )
        self.styl.configure(
            "PozycjaPolaKA.TLabel",
            anchor=tk.CENTER,
            font=stale.CZCIONKI["mała"],
            width=4
        )

    def ustaw_etyramke(self):
        """Ustawia etyramkę pod widżety."""
        self.etyramka.grid(sticky="we")
        self.etyramka.columnconfigure(0, weight=1)  # zgłasza wyżej powiększanie w poziomie

    def buduj_etykiety(self):
        """Buduje etykiety."""
        ttk.Label(
            self.etyramka,
            text="Wybierz statek:",
            style="Mała.TLabel"
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky=tk.W
        )
        ttk.Label(
            self.etyramka,
            text="Wybierz salwę:",
            style="Mała.TLabel"
        ).grid(
            row=2,
            column=0,
            sticky=tk.W,
            pady=(5, 0)
        )
        ttk.Label(
            self.etyramka,
            text="Wybierz orientację:",
            style="Mała.TLabel"
        ).grid(
            row=2,
            column=1,
            sticky=tk.W,
            pady=(5, 0)
        )

    def buduj_comboboksy(self):
        """Buduje comboboksy."""
        # wybór statku
        self.combo_statku = ComboZeZmianaCzcionki(
            self.etyramka,
            styl="KA.TCombobox",
            font=stale.CZCIONKI["mała"],
            values=self.pg.gra.tura.napastnicy,
            width=35
        )
        self.combo_statku.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=tk.W
        )
        self.combo_statku.configure(font=stale.CZCIONKI["mała"])  # to zmienia tylko czcionkę pola tekstowego (Entry), które jest częścią comboboksa

        # wybór salwy
        self.combo_salwy = ComboZeZmianaCzcionki(
            self.etyramka,
            styl="KA.TCombobox",
            font=stale.CZCIONKI["mała"],
            width=6
        )
        self.combo_salwy.grid(
            row=3,
            column=0,
            sticky=tk.W,
            pady=(0, 10)
        )
        self.combo_salwy.configure(font=stale.CZCIONKI["mała"])

        # wybór orientacji
        self.combo_orientacji = ComboOrientacji(
            self.etyramka,
            styl="KA.TCombobox",
            font=stale.CZCIONKI["mała"],
            width=7
        )
        self.combo_orientacji.grid(
            row=3,
            column=1,
            sticky=tk.W,
            pady=(0, 10)
        )
        self.combo_orientacji.configure(font=stale.CZCIONKI["mała"])

    def przestaw_na_readonly(self):
        """Ustawia stan comboboksów jako `readonly`"""
        self.combo_statku.state(["readonly"])
        self.combo_salwy.state(["readonly"])
        self.combo_orientacji.state(["readonly"])

    def powiaz_callbacki(self):
        """Wiąże callbacki"""
        self.combo_statku.bind("<<ComboboxSelected>>", self.na_wybor_statku)
        self.combo_salwy.bind("<<ComboboxSelected>>", self.na_wybor_salwy)
        self.combo_orientacji.bind("<<ComboboxSelected>>", self.na_wybor_orientacji)
        self.winfo_toplevel().bind("<Button-3>", self.na_prawy_przycisk_myszy)

    # CALLBACK combo_statku
    def na_wybor_statku(self, event=None):
        """Zmienia statek na planszy i aktualizuje combo_salwy."""
        event.widget.selection_clear()  # czyści tło pola tekstowego comboboksa
        indeks = event.widget.current()
        wybrany_statek = self.pg.gra.tura.napastnicy[indeks]
        self.pg.zmien_statek(wybrany_statek)

    # CALLBACK combo_salwy
    def na_wybor_salwy(self, event=None):
        """Aktualizuje combo_orientacji."""
        event.widget.selection_clear()
        self.ustaw_combo_orientacji(event.widget.get())

    # CALLBACK combo_orientacji
    def na_wybor_orientacji(self, event=None):
        """Czyści pole tekstowe combo_orientacji"""
        event.widget.selection_clear()
        self.combo_orientacji.ostatnia_orientacja = self.combo_orientacji.get()

    def wylacz_salwe_i_orientacje(self):
        """Wyłącza combo salwy i orientacji. Uruchamiane po oddaniu ostatniej salwy."""
        self.combo_salwy.state(["disabled"])
        self.combo_orientacji.state(["disabled"])

    def wlacz_comboboksy(self):
        """Włącza i wypełnia danymi startowymi wszystkie comboboksy. Uruchamiane na początku nowej rundy."""
        self.combo_statku.state(["!disabled"])
        self.combo_statku.state(["readonly"])
        self.combo_statku["values"] = self.pg.gra.tura.napastnicy
        self.combo_salwy.state(["!disabled"])
        self.combo_salwy.state(["readonly"])
        self.combo_salwy["values"] = self.pg.gra.tura.runda.sila_ognia
        self.combo_orientacji.state(["!disabled"])
        self.combo_orientacji.state(["readonly"])
        self.ustaw_combo_orientacji(self.combo_salwy["values"][0])

    def blokuj_atak(self):
        """Blokuje możliwość oddania salwy w pola planszy przeciwnika."""
        self.wylacz_salwe_i_orientacje()
        self.pg.gra.tura.runda.mozna_atakowac = False
        self.pp.wylacz_atak()
        self.pozycje_salwy.wyczysc()

    def ustaw_combo_salwy(self):
        """Ustawia aktualną siłę ognia w comboboksie salwy."""
        sila_ognia = self.pg.gra.tura.runda.sila_ognia
        if len(sila_ognia) > 0:
            self.combo_salwy["values"] = ["{} pole".format(salwa) if salwa == 1 else "{} pola".format(salwa) for salwa in self.pg.gra.tura.runda.sila_ognia]
            self.combo_salwy.set(self.combo_salwy["values"][0])
            self.ustaw_combo_orientacji(self.combo_salwy["values"][0])
        else:
            self.blokuj_atak()

    def ustaw_combo_orientacji(self, salwa_tekst):
        """
        Ustawia w comboboksie orientację wybranej salwy. Zachowuje wcześniejszą orientację, jeśli wybrana salwa odpowiada poprzedniej.
        """
        salwa = int(salwa_tekst[0])
        if salwa == 1:
            self.combo_orientacji["values"] = [self.ORIENTACJE[0]]
            self.wylacz_pozycje_salwy("druga")
            self.wylacz_pozycje_salwy("trzecia")
        elif salwa == 2:
            self.combo_orientacji["values"] = self.ORIENTACJE[1:5]
            self.wlacz_pozycje_salwy("druga")
            self.wylacz_pozycje_salwy("trzecia")
        elif salwa == 3:
            self.combo_orientacji["values"] = self.ORIENTACJE[5:]
            self.wlacz_pozycje_salwy("druga")
            self.wlacz_pozycje_salwy("trzecia")

        if salwa == self.combo_orientacji.ostatnia_salwa:
            self.combo_orientacji.set(self.combo_orientacji.ostatnia_orientacja)
        else:
            self.combo_orientacji.set(self.combo_orientacji["values"][0])
        self.combo_orientacji.ostatnia_salwa = salwa
        self.combo_orientacji.ostatnia_orientacja = self.combo_orientacji.get()

    def wylacz_pozycje_salwy(self, pozycja):
        """Wyłącza podaną pozycję salwy"""
        if pozycja == "druga":
            self.pozycje_salwy.numer_drugiej.grid_remove()
            self.pozycje_salwy.etykieta_drugiej.grid_remove()
        elif pozycja == "trzecia":
            self.pozycje_salwy.numer_trzeciej.grid_remove()
            self.pozycje_salwy.etykieta_trzeciej.grid_remove()

    def wlacz_pozycje_salwy(self, pozycja):
        """Włącza podaną pozycję salwy"""
        if pozycja == "druga":
            self.pozycje_salwy.numer_drugiej.grid()
            self.pozycje_salwy.etykieta_drugiej.grid()
        elif pozycja == "trzecia":
            self.pozycje_salwy.numer_trzeciej.grid()
            self.pozycje_salwy.etykieta_trzeciej.grid()

    # CALLBACK okna głównego
    def na_prawy_przycisk_myszy(self, event=None):
        """Rotuje wybraną orientacją salw (i w efekcie celownikiem na planszy przeciwnika)."""
        indeks = self.combo_orientacji.current()
        if indeks == len(self.combo_orientacji["values"]) - 1:
            indeks = 0
        else:
            indeks += 1
        self.combo_orientacji.set(self.combo_orientacji["values"][indeks])
        self.combo_orientacji.ostatnia_orientacja = self.combo_orientacji.get()


class ComboZeZmianaCzcionki(ttk.Combobox):
    """
    Combobox z możliwością zmiany czcionki w liście rozwijanej. Wzięte stąd: https://stackoverflow.com/questions/43086378/how-to-modify-ttk-combobox-fonts/ .Standardowy combobox nie daje takiej możliwości.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<Map>", self._obsluz_czcionke_listy_rozwijanej)

    def _obsluz_czcionke_listy_rozwijanej(self, *args):
        lista_rozwijana = self.tk.eval("ttk::combobox::PopdownWindow {}".format(self))
        self.tk.call("{}.f.l".format(lista_rozwijana), 'configure', '-font', self['font'])


class ComboOrientacji(ComboZeZmianaCzcionki):
    """
    Combobox orientacji salwy - zachowuje informację o ostatniej salwie i wybranej orientacji, tak że jeśli kolejna salwa ataku odpowiada poprzedniej - orientacja wybrana poprzednio w comboboksie pozostaje niezmieniona.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ostatnia_salwa = 0
        self.ostatnia_orientacja = ""


class PozycjeSalwy(ttk.Frame):
    """
    Podsekcja kontroli ataku pokazująca aktualne pozycje pól wybranej salwy.
    """

    def __init__(self, rodzic):
        super().__init__(rodzic)
        self.pierwsza = tk.StringVar()
        self.druga = tk.StringVar()
        self.trzecia = tk.StringVar()
        self.ustal_tlo_sytemowe()
        self.ustaw_sie()
        self.buduj_etykiety()

    def ustaw_sie(self):
        """Ustawia interfejs pod widżety."""
        self.grid(row=4, column=0, columnspan=2, sticky="we", pady=(0, 10))

    def buduj_etykiety(self):
        """Buduje etykiety."""
        self.numer_pierwszej = ttk.Label(self, style="Mała.TLabel", text="#1:")
        self.numer_pierwszej.grid(
            row=0,
            column=0,
            sticky=tk.W
        )
        self.numer_drugiej = ttk.Label(self, style="Mała.TLabel", text="#2:")
        self.numer_drugiej.grid(
            row=0,
            column=2,
            sticky=tk.W,
            padx=(25, 0)
        )
        self.numer_trzeciej = ttk.Label(self, style="Mała.TLabel", text="#3:")
        self.numer_trzeciej.grid(
            row=0,
            column=4,
            sticky=tk.W,
            padx=(25, 0)
        )
        self.etykieta_pierwszej = ttk.Label(
            self,
            style="PozycjaPolaKA.TLabel",
            text="",
            textvariable=self.pierwsza
        )
        self.etykieta_pierwszej.grid(row=0, column=1, sticky=tk.W)
        self.etykieta_drugiej = ttk.Label(
            self,
            style="PozycjaPolaKA.TLabel",
            text="",
            textvariable=self.druga
        )
        self.etykieta_drugiej.grid(row=0, column=3, sticky=tk.W)
        self.etykieta_trzeciej = ttk.Label(
            self,
            style="PozycjaPolaKA.TLabel",
            text="",
            textvariable=self.trzecia
        )
        self.etykieta_trzeciej.grid(row=0, column=5, sticky=tk.W)
        self.pierwsza.trace("w", lambda n, i, m, poz=self.pierwsza, et=self.etykieta_pierwszej: self.na_zmiane(poz, et))
        self.druga.trace("w", lambda n, i, m, poz=self.druga, et=self.etykieta_drugiej: self.na_zmiane(poz, et))
        self.trzecia.trace("w", lambda n, i, m, poz=self.trzecia, et=self.etykieta_trzeciej: self.na_zmiane(poz, et))

    def ustal_tlo_sytemowe(self):
        """Sprawdza kolor tla systemowego i zapisuje w stałej"""
        self.TLO_SYSTEMOWE = self.winfo_toplevel().cget("bg")

    # CALLBACK każdej pozycji pola
    def na_zmiane(self, pozycja, etykieta):
        """Zmienia tło etykiety pozycji pola."""
        if pozycja.get() == "":
            etykieta.configure(background=self.TLO_SYSTEMOWE)
        else:
            etykieta.configure(background=stale.KOLORY["pozycja-pola"])

    def wyczysc(self):
        self.pierwsza.set("")
        self.druga.set("")
        self.trzecia.set("")


class KontrolaFloty(Sekcja):
    """
    Sekcja kontroli floty (całej gracza i zatopionej przeciwnika) znajdująca się w środku po prawej stronie głównego interfejsu gry. Dopuszcza powiększanie w poziomie i w pionie.
    """

    def __init__(self, rodzic, odstep_zewn, odstep_wewn, tytul="Flota", **kwargs):
        super().__init__(rodzic, odstep_zewn, odstep_wewn, tytul)
        self.pg = kwargs["plansza_gracza"]
        self.pp = kwargs["plansza_przeciwnika"]
        self.ustal_tlo_sytemowe()
        self.ustaw_style()
        self.ustaw_etyramke()
        self.buduj_drzewa()
        self.buduj_przyciski()
        self.buduj_pozycje_pola()

    def ustaw_style(self):
        """Ustawia style dla widżetów"""
        self.styl = ttk.Style()
        self.styl.configure(
            "PozycjaPolaKF.TLabel",
            anchor=tk.CENTER,
            width=4
        )

    def ustaw_etyramke(self):
        """Ustawia etyramkę pod widżety."""
        self.etyramka.grid(sticky="nsew")
        # zgłasza wyżej powiększanie w poziomie i w pionie
        self.etyramka.rowconfigure(0, weight=1)
        self.etyramka.columnconfigure(0, weight=1)

    def buduj_drzewa(self):
        """Buduje drzewa floty (gracza i przeciwnika) umieszczone w notesie."""
        notes = ttk.Notebook(self.etyramka)
        # drzewa nie mogą być bezpośrednio umieszczane w notesie - potrzebne ramki pośrednie
        ramka_drzewa_g = ttk.Frame(notes)
        ramka_drzewa_p = ttk.Frame(notes)
        self.drzewo_g = DrzewoFlotyGracza(ramka_drzewa_g, self.pg)
        self.drzewo_p = DrzewoFlotyPrzeciwnika(ramka_drzewa_p, self.pp)
        ramka_drzewa_g.grid(sticky="nsew")
        # zgłasza wyżej powiększanie w poziomie i w pionie
        ramka_drzewa_g.rowconfigure(0, weight=1)
        ramka_drzewa_g.columnconfigure(0, weight=1)
        ramka_drzewa_p.grid(sticky="nsew")
        # zgłasza wyżej powiększanie w poziomie i w pionie
        ramka_drzewa_p.rowconfigure(0, weight=1)
        ramka_drzewa_p.columnconfigure(0, weight=1)
        notes.add(ramka_drzewa_g, text="Gracz")
        notes.add(ramka_drzewa_p, text="Przeciwnik")
        notes.grid(row=0, column=0, columnspan=3, sticky="nsew")
        # zgłasza wyżej powiększanie w poziomie i w pionie
        notes.rowconfigure(0, weight=1)
        notes.columnconfigure(0, weight=1)

    def buduj_przyciski(self):
        """Buduje przyciski przewijania statków."""

        def zaladuj_ikone(sciezka):
            """Otwiera i ładuję ikonę z pliku graficznego"""
            try:
                with Image.open(sciezka) as plik:
                    ikona = ImageTk.PhotoImage(plik)
            except IOError:
                print("Nieudane wczytanie ikony statku. Brak pliku {}".format(sciezka[3:]))
                raise
            return ikona

        # przycisk do tyłu
        ikona_do_tylu = zaladuj_ikone("zasoby/ikona_statku/statek-w-lewo_32x32.png")
        self.przycisk_do_tylu = ttk.Button(
            self.etyramka,
            # text="Poprzedni",
            # compound=tk.LEFT,
            image=ikona_do_tylu,
            command=self.pg.na_nawias_kw_lewy
        )
        self.przycisk_do_tylu.image = ikona_do_tylu  # konieczne ze względu na bug Tkintera (https://stackoverflow.com/questions/22200003/tkinter-button-not-showing-image)
        self.przycisk_do_tylu.grid(row=1, column=0, sticky=tk.W, pady=(13, 0), padx=35)
        # przycisk do przodu
        ikona_do_przodu = zaladuj_ikone("zasoby/ikona_statku/statek-w-prawo_32x32.png")
        self.przycisk_do_przodu = ttk.Button(
            self.etyramka,
            # text="Kolejny",
            # compound=tk.LEFT,
            image=ikona_do_przodu,
            command=self.pg.na_nawias_kw_prawy
        )
        self.przycisk_do_przodu.image = ikona_do_przodu
        self.przycisk_do_przodu.grid(row=1, column=2, sticky=tk.E, pady=(13, 0), padx=35)

    def buduj_pozycje_pola(self):
        """Buduje etykietę wyświetlającą pozycję pola planszy gracza wskazywanego aktualnie przez kursor."""
        self.pozycja_pola = tk.StringVar()
        self.etykieta_pozycji_pola = ttk.Label(
            self.etyramka,
            style="PozycjaPolaKF.TLabel",
            text="",
            textvariable=self.pozycja_pola
        )
        self.etykieta_pozycji_pola.grid(row=1, column=1, sticky="we", pady=(13, 0))
        self.pozycja_pola.trace("w", self.na_zmiane_pozycji_pola)

    def ustal_tlo_sytemowe(self):
        """Sprawdza kolor tla systemowego i zapisuje w stałej"""
        self.TLO_SYSTEMOWE = self.winfo_toplevel().cget("bg")

    # CALLBACK pozycji pola
    def na_zmiane_pozycji_pola(self, *args):
        """Zmienia tło etykiety pozycji pola."""
        if self.pozycja_pola.get() == "":
            self.etykieta_pozycji_pola.configure(background=self.TLO_SYSTEMOWE)
        else:
            self.etykieta_pozycji_pola.configure(background=stale.KOLORY["pozycja-pola"])

    def wlacz_widzety(self):
        """
        Włącza przyciski zmiany statku i kasuje wyszarzenie drzewa floty. Uruchamiane na początku nowej rundy.
        """
        self.przycisk_do_tylu.state(["!disabled"])
        self.przycisk_do_przodu.state(["!disabled"])
        self.drzewo_g.kasuj_wyszarzenie_statkow()


class DrzewoFloty(ttk.Treeview):
    """
    Drzewo wyświetlające statki floty (gracza/przeciwnika). Szczegółowa implementacja w klasach potomnych.
    """

    KOLORY = {
        "zablokowane": "gray64",
        "rangi": "LemonChiffon2",
        "rangi-zatopione": "plum3",  # TODO
        "rangi-przeciwnik": "DarkOliveGreen2"  # TODO
    }

    def __init__(self, rodzic, plansza_gui):
        super().__init__(rodzic)
        self.plansza_gui = plansza_gui
        self.wys_wiersza = 15

        self.ustaw_style()
        self.ustaw_sie()
        self.wstaw_suwaki(rodzic)
        self.powiaz_escape()

    def ustaw_style(self):
        """Ustawia style dla drzewa."""
        self.styl = ttk.Style()
        self.styl.configure(
            "KF.Treeview",
            font=stale.CZCIONKI["mała"],
            rowheight=self.wys_wiersza
        )
        self.styl.configure(
            "KF.Treeview.Heading",
            font=stale.CZCIONKI["mała"]
        )

    def ustaw_sie(self):
        """Konfiguruje to drzewo."""
        self.configure(
            style="KF.Treeview",
            height=self.podaj_wysokosc(),
            columns=("statek", "gdzie", "rozmiar", "siła ognia", "ofiary"),
            displaycolumns="#all",
            selectmode="browse"
        )
        self.grid(sticky="nsew")

    def podaj_wysokosc(self):
        """
        Podaje wysokość (w wierszach) obliczaną na podstawie rozmiaru planszy.

        Punktem wyjścia do obliczeń były testy, z których wynika, że dla planszy w rozmiarze 26x26 idealna wysokość to 19 wierszy (przy wysokości wiersza równej 15 px - taka wysokość wiersza jest optymalna dla czytelności i wyglądu drzewa, ale dla prostego przeliczania względem planszy lepsza byłaby wysokość równa 13 px (ponieważ pole planszy ma 26 px)).
        """
        # TODO: testy pod Windowsem

        def skoryguj_wysokosc_pod_pasek_komunikatow(wysokosc, rzedy_planszy):
            # po decyzji o tym, że pasek komunikatów będzie umiejscowiony tylko pod planszami a nie pod całym oknem głównym, kolumna sekcji kontroli musi być odpowiednio wyższa, co oznacza konieczność korekty wysokości drzewa
            if rzedy_planszy >= 14:
                korekta = 6  # daje od 31 wierszy drzewa przy 30 wierszach planszy do 7 przy 14
            elif rzedy_planszy == 13:
                korekta = 5  # daje 6 wierszy drzewa
            elif rzedy_planszy == 12:
                korekta = 4  # daje 5 wierszy drzewa
            else:
                korekta = 3  # daje 4 wiersze
            return wysokosc + korekta

        bazowe_wiersze, bazowe_rzedy, wys_pola = 19, 26, 26
        rzedy_planszy = self.plansza_gui.gra.plansza.rzedy
        delta_planszy = (rzedy_planszy - bazowe_rzedy) * wys_pola
        if delta_planszy < 0:
            wysokosc = bazowe_wiersze - math.ceil(abs(delta_planszy) / self.wys_wiersza)
            if wysokosc < 1:
                wysokosc = 1
            return skoryguj_wysokosc_pod_pasek_komunikatow(wysokosc, rzedy_planszy)
        else:
            wysokosc = bazowe_wiersze + math.floor(abs(delta_planszy) / self.wys_wiersza)
            return skoryguj_wysokosc_pod_pasek_komunikatow(wysokosc, rzedy_planszy)

    def wstaw_suwaki(self, rodzic):
        """Wstawia suwaki."""
        suwak_pionowy = ttk.Scrollbar(rodzic, orient=tk.VERTICAL, command=self.yview)
        suwak_pionowy.grid(column=1, row=0, sticky="ns")
        suwak_poziomy = ttk.Scrollbar(rodzic, orient=tk.HORIZONTAL, command=self.xview)
        suwak_poziomy.grid(column=0, row=1, sticky="we")
        self.configure(yscrollcommand=suwak_pionowy.set, xscrollcommand=suwak_poziomy.set)

    def ustaw_kolumny(self, naglowek_rozmiar):
        """Konfiguruje kolumny."""
        self.heading("#0", text="Ranga")
        self.heading("statek", text="Statek")
        self.heading("gdzie", text="Poz")
        self.heading("rozmiar", text=naglowek_rozmiar)
        self.heading("siła ognia", text="Siła")
        self.heading("ofiary", text=Statek.ORDER)
        self.column("#0", stretch=True, minwidth=70, width=39)
        self.column("statek", stretch=True, minwidth=85, width=39)
        self.column("gdzie", stretch=True, minwidth=35, width=39, anchor=tk.CENTER)
        self.column("rozmiar", stretch=True, minwidth=40, width=39, anchor=tk.E)
        self.column("siła ognia", stretch=True, minwidth=50, width=39, anchor=tk.W)
        self.column("ofiary", stretch=True, minwidth=12, width=39)

    def powiaz_escape(self):
        """Wiąże callback obsługujący naćiśnięcie ESCAPE."""
        self.bind("<Escape>", self.na_escape)

    # CALLBACK całego drzewa
    def na_escape(self, event=None):
        """Kasuje selekcję."""
        element_id = self.focus()
        if element_id != "":  # jeśli jakiś element był w ogóle wybrany
            self.selection_remove(element_id)


class DrzewoFlotyGracza(DrzewoFloty):
    """
    Pokazuje statki gracza. Kolumny: `Ranga` (#0), `Statek`, `Poz` (pozycja), `NT/R` (pola nietrafione/rozmiar), `Siła` (siła ognia), `★` (ilość gwiazdek = ilość ofiar danego statku).
    """

    def __init__(self, rodzic, plansza_gui):
        super().__init__(rodzic, plansza_gui)

        self.ustaw_kolumny("NT/R")
        self.dodaj_statki(self.plansza_gui.gra.plansza.niezatopione, "niezatopione")
        self.ustaw_wyglad()
        self.powiaz_podwojne_klikniecie()

    def dodaj_statki(self, statki, kategoria):
        """
        Dodaje podane (niezatopione/zatopione) statki do drzewa. Wartość parametru `kategoria` to albo 'niezatopione' albo 'zatopione'.
        """
        # kategoria
        self.insert("", "0", kategoria,
                    text=kategoria + " (" + str(len(statki)) + ")",
                    open=True,
                    tags="kategoria"
                    )
        # rangi
        ilosc_wg_rang = self.plansza_gui.gra.plansza.podaj_ilosc_niezatopionych_wg_rang()
        for ranga in Statek.RANGI[::-1]:
            if ilosc_wg_rang[ranga] > 0:
                ranga_i_ilosc = Statek.SYMBOLE[ranga] + " (" + str(ilosc_wg_rang[ranga]) + ")"
                self.insert(kategoria, "end",
                            ranga,
                            text=ranga_i_ilosc,
                            open=True,
                            tags=(kategoria, "ranga")
                            )
        # statki
        for i, statek in enumerate(statki):
            self.insert(
                statek.RANGA_BAZOWA, "end",
                str(statek.polozenie),  # tekstowa reprezentacja położenia statku jako ID w drzewie - upraszcza późniejszą translację wybranego elementu drzewa z powrotem na statek na planszy
                values=(
                    '"' + statek.nazwa + '"',
                    str(statek.polozenie),
                    statek.podaj_nietrafione_na_rozmiar(),
                    str(statek.sila_ognia),
                    "".join([statek.ORDER for ofiara in statek.ofiary])
                ),
                tags=(kategoria, "statek")
            )

    def ustaw_wyglad(self):
        """Konfiguruje wygląd zawartości drzewa."""
        self.tag_configure("kategoria", font=stale.CZCIONKI["mała-pogrubiona"])
        self.tag_configure("ranga", background=self.KOLORY["rangi"])
        self.tag_configure("zablokowane", foreground=self.KOLORY["zablokowane"])

    def powiaz_podwojne_klikniecie(self):
        """Wiąże callback obsługujący podóœjne kliknięcie."""
        self.tag_bind("statek", "<Double-Button-1>", self.na_podwojne_klikniecie)

    # CALLBACK elementów z tagiem `statek`
    def na_podwojne_klikniecie(self, event=None):
        """Wybiera kliknięty podwójnie statek na planszy gracza."""
        statek = self.plansza_gui.gra.plansza.podaj_statek(self.focus(), tryb="str")
        self.plansza_gui.zmien_statek(statek)

    def wyszarz_zablokowane_statki(self):
        """Wyszarza zablokowane statki."""
        napastnik = self.plansza_gui.gra.tura.runda.napastnik
        lista_iid = [str(statek.polozenie) for statek in self.plansza_gui.gra.tura.napastnicy if statek != napastnik]
        for iid in lista_iid:
            tag_ranga, tag_statek = self.item(iid)["tags"][:2]
            self.item(iid, tags=(tag_ranga, tag_statek, "zablokowane"))

    def kasuj_wyszarzenie_statkow(self):
        """Kasuje wyszarzenie zablokowanych statków."""
        lista_iid = [str(statek.polozenie) for statek in self.plansza_gui.gra.tura.napastnicy]
        for iid in lista_iid:
            tag_ranga, tag_statek = self.item(iid)["tags"][:2]
            self.item(iid, tags=(tag_ranga, tag_statek))

    def wyszarz_statek(self, statek):
        """Wyszarza podany statek"""
        iid = str(statek.polozenie)
        tag_ranga, tag_statek = self.item(iid)["tags"][:2]
        self.item(iid, tags=(tag_ranga, tag_statek, "zablokowane"))


class DrzewoFlotyPrzeciwnika(DrzewoFloty):
    """
    Pokazuje zatopione statki przeciwnika. Kolumny: `Kategoria` (bez nagłówka), `Statek`, `Poz` (pozycja), `Roz` (rozmiar), `★` (ilość gwiazdek = ilość ofiar danego statku).
    """

    def __init__(self, rodzic, plansza_gui):
        super().__init__(rodzic, plansza_gui)

        self.ustaw_kolumny("Rozm")
        self.configure(displaycolumns=(0, 1, 2, 4))

    def dodaj_statek(self):
        """
        Dodaje zatopiony statek przeciwnika. Przy pierwszym dodaniu statku danej rangi tworzy odpowiedni folder rangi.
        """
        pass  # TODO


class KontrolaGry(Sekcja):
    """
    Sekcja kontroli gry znajdująca się w prawym dolnym rogu głównego interfejsu gry. Dopuszcza powiększanie w poziomie.
    """

    KOLORY = {
        "stan-gry-g": "LemonChiffon4",
        "stan-gry-p": "LemonChiffon4"
    }
    SZER_STANU = 15  # szerokość stanu gry (etykiety) w znakach

    def __init__(self, rodzic, odstep_zewn, odstep_wewn, tytul, **kwargs):
        super().__init__(rodzic, odstep_zewn, odstep_wewn, tytul)
        self.nowa_tura = False
        self.pg = kwargs["plansza_gracza"]
        self.pp = kwargs["plansza_przeciwnika"]
        self.ka = None  # sekcja kontroli ataku przekazywana przez GręGUI
        self.kf = None  # sekcja kontroli floty przekazywana przez GręGUI
        self.ustaw_style()
        self.ustaw_etyramke()
        self.ustaw_tytul()
        self.buduj_etykiety()
        self.buduj_przycisk()
        self.powiaz_enter()
        self.komunikator = None  # przekazywane przez GręGUI

    def ustaw_etyramke(self):
        """Ustawia etyramkę pod widżety."""
        self.etyramka.grid(sticky="we")
        self.etyramka.columnconfigure(0, weight=1)  # zgłasza wyżej powiększanie w poziomie

    def ustaw_tytul(self):
        """Ustawia tytuł sekcji. Format tytułu: Tura #[liczba]/Runda #[liczba]"""
        self.tytul.set(self.pg.gra.podaj_info_o_rundzie().title())

    def ustaw_style(self):
        """Ustawia style dla sekcji."""
        self.styl = ttk.Style()
        self.styl.configure(
            "GraczKG.TLabel",
            font=stale.CZCIONKI["duża-pogrubiona"],
            # background=stale.KOLORY["pozycja-pola"],
            foreground=self.KOLORY["stan-gry-g"]
        )
        self.styl.configure(
            "PrzeciwnikKG.TLabel",
            font=stale.CZCIONKI["duża-pogrubiona"],
            # background=stale.KOLORY["pozycja-pola"],
            foreground=self.KOLORY["stan-gry-p"]
        )
        self.styl.configure(
            "KG.TButton",
            font=stale.CZCIONKI["pogrubiona"]
        )

    def buduj_etykiety(self):
        """Buduje etykiety stanu gry dla gracza i przeciwnika."""
        # gracz
        etykieta_g = ttk.Label(
            self.etyramka,
            style="Mała.TLabel",
            text=self.pg.tytul.get() + ":"
        ).grid(
            row=0,
            column=0,
            sticky=tk.W,
            padx=(28, 13),
            pady=(0, 5)
        )
        tekst_g = self.podaj_tekst_stanu(self.pg.gra)
        self.stan_g = ttk.Label(
            self.etyramka,
            style="GraczKG.TLabel",
            text=tekst_g,
            anchor=tk.E,
            width=self.SZER_STANU
        )
        self.stan_g.grid(
            row=0,
            column=1,
            sticky=tk.E,
            padx=(0, 23),
            pady=(0, 5)
        )
        # przeciwnik
        etykieta_p = ttk.Label(
            self.etyramka,
            style="Mała.TLabel",
            text=self.pp.tytul.get() + ":"
        ).grid(
            row=1,
            column=0,
            sticky=tk.W,
            padx=(28, 13),
            pady=(5, 5)
        )
        tekst_p = self.podaj_tekst_stanu(self.pp.gra)
        self.stan_p = ttk.Label(
            self.etyramka,
            style="PrzeciwnikKG.TLabel",
            text=tekst_p,
            anchor=tk.E,
            width=self.SZER_STANU
        )
        self.stan_p.grid(
            row=1,
            column=1,
            sticky=tk.E,
            padx=(0, 23),
            pady=(5, 5)
        )

    def podaj_tekst_stanu(self, gra):
        """Podaje tekst stanu gry dla danej planszy."""
        nietrafione, procent = gra.plansza.podaj_info_o_nietrafionych()
        tekst = nietrafione + "/"
        tekst += str(gra.plansza.ilosc_pol_statkow) + " ("
        tekst += procent + ")"
        return tekst

    def buduj_przycisk(self):
        """Buduje przycisk KONIEC RUNDY."""
        self.koniec_rundy = ttk.Button(
            self.etyramka,
            text="KONIEC RUNDY",
            style="KG.TButton",
            command=self.na_koniec_rundy
        )
        self.koniec_rundy.grid(
            row=2,
            column=1,
            sticky=tk.E,
            padx=(0, 23),
            pady=10
        )

    def ustaw_przycisk(self):
        """Ustawia tekst przycisku KONIEC RUNDY oraz flagę nowej tury."""
        if len(self.pg.gra.tura.napastnicy) == 1:
            self.koniec_rundy.configure(text="KONIEC TURY")
            self.nowa_tura = True
        else:
            self.koniec_rundy.configure(text="KONIEC RUNDY")
            self.nowa_tura = False

    def aktualizuj_stan_gry(self, czyj="gracza"):
        """Aktualizuje etykietę stanu gry."""
        if czyj == "gracza":
            self.stan_g.configure(text=self.podaj_tekst_stanu(self.pg.gra))
        elif czyj == "przeciwnika":
            self.stan_p.configure(text=self.podaj_tekst_stanu(self.pp.gra))

    # CALLBACK przycisku KONIEC RUNDY
    def na_koniec_rundy(self, event=None):
        """Kończy rundę."""
        zgrany_statek = self.pg.gra.tura.runda.napastnik
        self.pg.kasuj_wybor_statku(zgrany_statek)
        self.pg.zmien_stan_statku(zgrany_statek, "disabled")
        self.kf.drzewo_g.wyszarz_statek(zgrany_statek)
        self.pp.gra.tura.runda.salwy_otrzymane = self.pg.gra.tura.runda.salwy_oddane
        self.pg.gra.tura.dodaj_runde() if not self.nowa_tura else self.pg.gra.dodaj_ture()
        self.odblokuj_widzety()
        self.pg.wybierz_statek(self.pg.gra.tura.runda.napastnik)
        self.ustaw_tytul()
        self.ustaw_przycisk()
        self.komunikator.o_rundzie(self.pg.gra)  # TODO: komunikat o ruchu przeciwnika
        # TODO
        # self.wykonaj_ruch_przeciwnika()

    def powiaz_enter(self):
        """Wiąże callback obsługujący naciśnięcie ENTER."""
        self.winfo_toplevel().bind("<Return>", self.na_koniec_rundy)
        self.winfo_toplevel().bind("<KP_Enter>", self.na_koniec_rundy)

    def odblokuj_widzety(self):
        """
        Odblokowuje widżety umożliwiające zmianę statku zablokowane po pierwszej salwie w rundzie oraz comboboksy zablokowane po oddaniu ostatniej salwy.
        """
        self.pg.wlacz_zablokowane_statki()
        self.pp.wlacz_atak()
        self.ka.wlacz_comboboksy()
        self.kf.wlacz_widzety()

    def wykonaj_ruch_przeciwnika(self):
        """
        Wykonuje ruch przeciwnika.
        """
        # self.pp.gra.zrob_ruch()
        # salwy = self.pp.gra.tura.runda.salwy_oddane
        # self.pg.oznacz_salwy(salwy)
        # self.pg.gra.tura.runda.salwy_otrzymane = salwy
        # self.pg.gra.tura.filtruj_zatopione()
