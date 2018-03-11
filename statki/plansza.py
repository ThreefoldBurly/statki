"""

    statki.plansza
    ~~~~~~~~~~~~~~

    Plansza gry wraz z jej podstawowymi elementami.

"""

from random import randint, choice, gauss
from decimal import Decimal as D
from collections import namedtuple

from statki.pamiec import Parser


class Plansza:
    """
    Reprezentacja planszy do gry. Zapisuje całą informację o stanie gry po stronie jednego gracza w danym momencie. Na początku gry tworzone są 2 obiekty tej klasy - jeden dla gracza, drugi dla przeciwnika. Moduł `statki.gui.plansza` powiela tę dychotomię.
    """
    ALFABET = {
        1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J",
        11: "K", 12: "L", 13: "M", 14: "N", 15: "O", 16: "P", 17: "Q", 18: "R", 19: "S", 20: "T",
        21: "U", 22: "V", 23: "W", 24: "X", 25: "Y", 26: "Z", 27: "AA", 28: "AB", 29: "AC", 30: "AD",
        31: "AE", 32: "AF", 33: "AG", 34: "AH", 35: "AI", 36: "AJ", 37: "AK", 38: "AL", 39: "AM", 40: "AN"
    }
    MIN_ROZMIAR_STATKU, MAX_ROZMIAR_STATKU = Parser.podaj_minmax_rozmiar_statku()
    ZAPELNIENIE, ODCH_ST, PRZ_MEDIANY = Parser.podaj_parametry_wypelniania()

    Kierunki = namedtuple("Kierunki", "E S W N NE SE SW NW")
    KIERUNKI = Kierunki._make(Kierunki._fields)

    def __init__(self, kolumny, rzedy):
        self.kolumny, self.rzedy, self.rozmiar = kolumny, rzedy, rzedy * kolumny
        self.pola = self.stworz_pola()  # matryca pól (krotka krotek (rzędów))
        self.statki = []
        self.wypelnij_statkami(self.ZAPELNIENIE, self.ODCH_ST, self.PRZ_MEDIANY)
        self.o_statkach()  # test
        self.drukuj()  # test
        self.ilosc_pol_statkow = sum([statek.rozmiar for statek in self.statki])
        self.zatopione = []  # statki zatopione tej planszy
        self.niezatopione = self.statki[:]  # statki niezatopione tej planszy

    def stworz_pola(self):
        """Tworzy pola planszy"""
        pola = []
        for y in range(1, self.rzedy + 1):
            rzad = []
            for x in range(1, self.kolumny + 1):
                rzad.append(Pole(id(self), x, y))
            pola.append(rzad)
        return tuple(tuple(rzad) for rzad in pola)

    def drukuj(self):  # do testów
        """Drukuje planszę w standard output."""
        # numeracja kolumn
        print()
        print("##### PLANSZA #####".center(self.kolumny * 3 + 2))
        print()
        # print("    " + "  ".join([str(liczba) for liczba in range(1, self.kolumny + 1) if liczba < 10]) + " " + " ".join([str(liczba) for liczba in range(1, self.kolumny + 1) if liczba >= 10]))
        print("    " + "  ".join([self.ALFABET[liczba] for liczba in range(1, self.kolumny + 1)]))
        print()
        for i in range(len(self.pola)):
            # numeracja rzędów
            if i + 1 < 10:
                print(str(i + 1) + "  ", end=" ")
            else:
                print(str(i + 1) + " ", end=" ")
            # właściwe pola planszy
            print("  ".join([pole.znacznik for pole in self.pola[i]]))

    def podaj_pole(self, kolumna, rzad):
        """
        Podaje pole wg wskazanych współrzędnych. Jeśli podane współrzędne wykraczają poza zakres planszy zwraca None.
        """
        if self.czy_w_planszy(kolumna, rzad):
            return self.pola[rzad - 1][kolumna - 1]
        else:
            return None

    def czy_w_planszy(self, kolumna, rzad):
        """Sprawdza czy wskazane wspolrzedne są w obrębie planszy."""
        if rzad < 1 or rzad > self.rzedy or kolumna < 1 or kolumna > self.kolumny:
            return False
        else:
            return True

    def podaj_sasiednie_pole(self, pole, kierunek):
        """Podaje pole sąsiednie dla wskazanego pola wg podanego kierunku."""
        kolumna, rzad = pole.podaj_wspolrzedne()
        if kierunek == self.KIERUNKI.E:
            kolumna += 1
        elif kierunek == self.KIERUNKI.S:
            rzad += 1
        elif kierunek == self.KIERUNKI.W:
            kolumna -= 1
        elif kierunek == self.KIERUNKI.N:
            rzad -= 1
        elif kierunek == self.KIERUNKI.NE:
            kolumna += 1
            rzad -= 1
        elif kierunek == self.KIERUNKI.SE:
            kolumna += 1
            rzad += 1
        elif kierunek == self.KIERUNKI.SW:
            kolumna -= 1
            rzad += 1
        elif kierunek == self.KIERUNKI.NW:
            kolumna -= 1
            rzad -= 1

        return self.podaj_pole(kolumna, rzad)  # None jeśli poza planszą!

    def umiesc_statek(self, kolumna, rzad, rozmiar):
        """
        Stara się umieścić statek o podanym rozmiarze na planszy. Statek rozrasta się w przypadkowych kierunkach ze wskazanego pola początkowego. W razie sukcesu metoda zwraca umieszczony statek, w razie porażki zwraca None (czyszcząc oznaczone wcześniej pola).
        """
        licznik_iteracji = 0
        pola_statku = []
        pole = self.podaj_pole(kolumna, rzad)  # pole początkowe

        def dodaj_pole_statku(pole):
            pole.znacznik = Pole.ZNACZNIKI.statek
            pola_statku.append(pole)

        while len(pola_statku) < rozmiar:
            if licznik_iteracji > rozmiar * 5:  # za dużo iteracji - NIEUDANE UMIESZCZENIE
                return None

            if licznik_iteracji == 0:  # pole początkowe
                if pole is not None and pole.znacznik == Pole.ZNACZNIKI.pusty:
                    dodaj_pole_statku(pole)
                else:
                    return None  # NIEUDANE UMIESZCZENIE
            else:
                pula_kierunkow = list(self.KIERUNKI[:4])

                while True:
                    if len(pula_kierunkow) < 1:  # powrót po wyczerpaniu kierunków
                        indeks = pola_statku.index(pole)
                        if indeks > 0:
                            pole = pola_statku[indeks - 1]
                            break
                        else:  # powrót do pola początkowego - NIEUDANE UMIESZCZENIE
                            for pole in pola_statku:  # czyszczenie nieudanego umieszczenia
                                pole.znacznik = Pole.ZNACZNIKI.pusty
                            return None

                    # próba dodania w losowym kierunku spośród ciągle obecnych w puli
                    kierunek = choice(pula_kierunkow)
                    sasiad = self.podaj_sasiednie_pole(pole, kierunek)
                    if sasiad is not None and sasiad.znacznik == Pole.ZNACZNIKI.pusty:
                        pole = sasiad
                        dodaj_pole_statku(pole)
                        break
                    else:
                        pula_kierunkow.remove(kierunek)

            licznik_iteracji += 1

        return Statek.fabryka(pola_statku)

    def umiesc_obwiednie_statku(self, statek):
        """Umieszcza na planszy i w statku obwiednię wskazanego statku."""
        for pole in statek.pola:
            for kierunek in self.KIERUNKI:
                sasiad = self.podaj_sasiednie_pole(pole, kierunek)
                if sasiad is not None:
                    if sasiad.znacznik == Pole.ZNACZNIKI.pusty:
                        sasiad.znacznik = Pole.ZNACZNIKI.obwiednia
                        statek.obwiednia.append(sasiad)
                    elif sasiad.znacznik == Pole.ZNACZNIKI.obwiednia:
                        if sasiad not in statek.obwiednia:
                            statek.obwiednia.append(sasiad)

    def podaj_statek(self, pole, tryb="pole"):
        """Zwraca statek zajmujący podane pole - również dla pól podanych jako string."""
        if tryb == "str":
            odwr_alfabet = {v: k for k, v in self.ALFABET.items()}
            litera, cyfra = "", ""
            for znak in pole:
                if znak.isalpha():
                    litera += znak
                else:
                    cyfra += znak
            kolumna, rzad = odwr_alfabet[litera], int(cyfra)
            pole = self.podaj_pole(kolumna, rzad)

        for statek in self.statki:
            if pole in statek.pola:
                return statek

        return None

    def wypelnij_statkami(self, zapelnienie=20, odch_st=9.5, prz_mediany=-12):
        """
        Wypełnia planszę statkami. Każdy kolejny statek ma losowy rozmiar w zakresie 1-20 i jest umieszczany w losowym miejscu. O ilości i rozmiarach statków decydują parametry.

        zapelnienie
        ~~~~~~~~~~~
        to wyrażony w procentach stosunek sumarycznego rozmiaru umieszczonych statków do rozmiaru planszy. W klasycznych `Statkach` zapełnienie wynosi: 20.

        odch_st
        ~~~~~~~
        to odchylenie standardowe w rozkładzie Gaussa, z którego losowany jest rozmiar statku. Czym wyższa wartość, tym większy rozrzut rozmiarów standardowa wartość: 9.5 (mediana - minimum przedziału losowania).

        prz_mediany
        ~~~~~~~~~~~
        to przesunięcie mediany w rozkładzie Gaussa, z którego losowany jest rozmiar statku. Wartość ujemna spowoduje losowanie większej ilości małych statków. Wartość dodatnia spowoduje losowanie większej ilości dużych statków. Zero (brak przesunięcia) powoduje losowanie wg standardowego rozkładu normalnego, gdzie mediana jest średnią arytmetyczną przedziału losowania.
        """

        # wartości domyślne parametrów zostały ustalone po testach (przy (50/9.5/-12) nie da się umieścić
        # wszystkich statków - z grubsza max warunek brzegowy)
        #
        # UWAGA: wpływ gracza na rodzaj floty jaki dostanie na planszy (od dużo małych statków do dużo
        # dużych statków) powinień sprowadzać się do manipulacji tylko jednym parametrem: PRZESUNIĘCIEM
        # MEDIANY

        def podaj_rozmiar_z_rozkladu_Gaussa(mediana, odch_st, minimum, maximum, prz_mediany=0):
            """
            Podaje rozmiar statku jako losową liczbę całkowitą wg rozkładu Gaussa we wskazanym przedziale oraz ze wskazanym przesunięciem mediany. Liczby losowane spoza żądanego przedziału są ignorowane.
            """
            while True:
                i = int(round(gauss(mediana + prz_mediany, odch_st)))
                if i in range(minimum, maximum + 1):
                    return i

        mediana = (self.MIN_ROZMIAR_STATKU + self.MAX_ROZMIAR_STATKU) / 2.0  # 10.5

        licznik_iteracji = 0
        sum_rozmiar_statkow = int(self.rozmiar * zapelnienie / 100)
        akt_rozmiar_statkow = sum_rozmiar_statkow

        while akt_rozmiar_statkow > 0:
            rozmiar_statku = podaj_rozmiar_z_rozkladu_Gaussa(mediana, odch_st, self.MIN_ROZMIAR_STATKU, self.MAX_ROZMIAR_STATKU, prz_mediany)
            if rozmiar_statku > akt_rozmiar_statkow:
                continue
            pole_startowe_x = randint(1, self.kolumny)
            pole_startowe_y = randint(1, self.rzedy)

            umieszczony_statek = self.umiesc_statek(pole_startowe_x, pole_startowe_y, rozmiar_statku)

            if umieszczony_statek is not None:
                self.umiesc_obwiednie_statku(umieszczony_statek)
                self.statki.append(umieszczony_statek)
                akt_rozmiar_statkow -= rozmiar_statku

            # obsługa wyjścia
            if licznik_iteracji > sum_rozmiar_statkow * 50:  # wielkość do przetestowania
                print(  # test
                    "Ilość iteracji pętli zapełniającej planszę statkami większa od oczekiwanej ({})".format(sum_rozmiar_statkow * 50),
                    "Nastąpiło przedwczesne przerwanie petli. Umieszczono mniej statków ({})".format(len(self.statki))
                )
                break

            licznik_iteracji += 1

        self.statki.sort(key=lambda s: s.rozmiar, reverse=True)  # od największego do najmniejszego

    def odkryj_pola(self, pola):
        """Odkrywa wskazane pola."""
        for pole in pola:
            if pole.znacznik in (Pole.ZNACZNIKI.pusty, Pole.ZNACZNIKI.obwiednia):
                pole.znacznik = Pole.ZNACZNIKI.pudlo
            elif pole.znacznik == Pole.ZNACZNIKI.statek:
                pole.znacznik = Pole.ZNACZNIKI.trafiony

    def oznacz_zatopione(self):
        """Oznacza statki posiadające wszystkie pola trafione jako zatopione."""
        for statek in self.niezatopione[:]:
            if not statek.czy_zatopiony():
                if all([True for pole in statek.pola if pole.znacznik == Pole.ZNACZNIKI.trafiony]):
                    statek.zatop()
                    self.niezatopione.remove(statek)
                    self.zatopione.append(statek)

    def o_statkach(self):  # do testów
        """Drukuje informację o umieszczonych statkach"""
        print()
        print("##### STATKI #####".center(self.kolumny * 3 + 2))
        sum_rozmiar = 0
        for statek in self.statki:
            sum_rozmiar += statek.rozmiar
            print('\nUmieszczony statek: {} "{}" [{}]'.format(statek.RANGA_BAZOWA.nazwa, statek.nazwa, statek.rozmiar))

        print("\nWszystkich umieszczonych statków: {}. Ich sumaryczny rozmiar: [{}]".format(len(self.statki), sum_rozmiar))

    def podaj_ilosc_niezatopionych_wg_rang(self):
        """
        Podaje zestawienie ilości niezatopionych statków wg rang w postaci słownika w formacie {'ranga': ilość}
        """
        lista_rang = [statek.RANGA_BAZOWA.nazwa for statek in self.niezatopione]
        return dict([(ranga.nazwa, lista_rang.count(ranga.nazwa)) for ranga in Statek.RANGI])

    def podaj_ilosc_zatopionych_wg_rang(self):
        """
        Podaje zestawienie ilości zatopionych statków wg rang w postaci słownika w formacie {'ranga': ilość}
        """
        lista_rang = [statek.RANGA_BAZOWA.nazwa for statek in self.zatopione]
        return dict([(ranga.nazwa, lista_rang.count(ranga.nazwa)) for ranga in Statek.RANGI])

    def podaj_ilosc_nietrafionych_pol(self):
        """Podaje ilość nietrafionych pól statków. Pola zatopione zalicza do trafionych."""
        licznik = 0
        for statek in self.statki:
            for pole in statek.pola:
                if pole.znacznik in (Pole.ZNACZNIKI.trafiony, Pole.ZNACZNIKI.zatopiony):
                    licznik += 1
        return self.ilosc_pol_statkow - licznik  # int

    def podaj_info_o_nietrafionych(self):
        """
        Podaje informację o nietrafionych polach w postaci 2 stringów: ilości nietrafionych pól planszy oraz stosunku nietrafionych pól statków do wszystkich pól zajętych przez statki w procentach.
        """
        nietrafione = D(self.podaj_ilosc_nietrafionych_pol())
        wszystkie = D(self.ilosc_pol_statkow)
        procent = round(nietrafione * 100 / wszystkie, 1)
        return (str(nietrafione), str(procent) + "%")


class Pole:
    """
    Reprezentacja pola planszy. Posiada 6 podstawowych stanów pola oznaczonych znacznikami. Z czego tylko pierwsze 3 są używane przy inicjalizacji planszy (pola zakryte), a pozostałe 3 pojawiają się tylko jako efekt działań graczy (pola odkryte).
    """
    Znaczniki = namedtuple("Znaczniki", "pusty obwiednia statek pudlo trafiony zatopiony")
    ZNACZNIKI = Znaczniki(
        # zakryte
        pusty="0",
        obwiednia=".",
        statek="&",
        # odkryte
        pudlo="x",
        trafiony="T",
        zatopiony="Z"
    )

    def __init__(self, id_planszy, kolumna, rzad, znacznik=None):
        self.id_planszy = id_planszy
        self.kolumna, self.rzad = kolumna, rzad
        self.znacznik = znacznik if znacznik is not None else self.ZNACZNIKI.pusty

    def __str__(self):
        """Zwraca informację o polu w formacie: litera kolumny+cyfra rzędu np. B9"""
        return "{}{}".format(Plansza.ALFABET[self.kolumna], self.rzad)

    def __eq__(self, other):
        """
        Przeładowanie operatora "==" (wzięte z: https://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes). Pola są równe jeśli: 1) należą do tej samej planszy, 2) ich współrzędne są równe i 3) ich znaczniki są równe.
        """
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __hash__(self):
        """
        Przeładowanie operatora "==" (dla porównań przy poprawnej obsłudze wyjątkowości w zbiorach)
        """
        return hash(tuple(sorted(self.__dict__.items())))

    def podaj_wspolrzedne(self):
        """Podaje współrzędne pola."""
        return (self.kolumna, self.rzad)

    def str_w_nawiasach(self):
        """Zwraca informację o polu w formacie __str__ tylko dodaje nawiasy, np. (B9)"""
        return "(" + str(self) + ")"


class Salwa:
    """
    Kolekcja pól planszy, w które strzela napastnik (UWAGA - nie są to pola planszy napastnika) wraz ze źródłem (jego położeniem).
    """
    Orientacje = namedtuple("Orientacje", "C E S W N WE NS NE SE SW NW")
    ORIENTACJE = Orientacje(
        C="•",
        E="•• prawo",
        S="╏ dół",
        W="•• lewo",
        N="╏ góra",
        WE="•••",
        NS="┇",
        NE="L",
        SE="Г",
        SW="Ꞁ",
        NW="⅃"
    )

    def __init__(self, zrodlo, pola, niewypaly=None):
        self.zrodlo = zrodlo  # polozenie statku który oddał salwę
        self.pola = pola
        self.trafienia = [True if pole.znacznik in (Pole.ZNACZNIKI.trafiony, Pole.ZNACZNIKI.zatopiony) else False for pole in self.pola]
        self.pudla = [True if pole.znacznik == Pole.ZNACZNIKI.pudlo else False for pole in self.pola]
        self.niewypaly = niewypaly if niewypaly is not None else []  # strzały poza planszę

    def __eq__(self, other):
        """
        Przeładowanie operatora '=='. Salwy są równe, jeśli wszystkie ich pola są równe.
        """
        if isinstance(self, other.__class__):
            if len(self) == len(other):
                for pole_tu, pole_tam in zip(self.pola, other.pola):
                    if pole_tu != pole_tam:
                        return False
                return True
            return False
        return NotImplemented

    def __str__(self):
        """Zwraca reprezentację salwy w postaci współrzędnych pól w formacie: (A5), (B4) i (C6)."""
        pola_tekst = ["(" + str(pole) + ")" for pole in self.pola]
        if len(self.pola) == 1:
            return pola_tekst[0]
        elif len(self.pola) == 2:
            return " i ".join(pola_tekst)
        else:
            return pola_tekst[0] + ", " + " i ".join(pola_tekst[1:])

    def __len__(self):
        return len(self.pola) + len(self.niewypaly)


class Statek:
    """
    Reprezentacja statku. Tworzone są tylko instancje klas potomnych.
    """

    RANGI = Parser.podaj_rangi()  # namedtuple
    ORDER = "★"

    @classmethod
    def fabryka(cls, pola_statku):
        """Tworzy statki odpowiedniej rangi."""
        rozmiar = len(pola_statku)
        if rozmiar in cls.RANGI.kuter.zakres:
            return Kuter(pola_statku)
        elif rozmiar in cls.RANGI.patrolowiec.zakres:
            return Patrolowiec(pola_statku)
        elif rozmiar in cls.RANGI.korweta.zakres:
            return Korweta(pola_statku)
        elif rozmiar in cls.RANGI.fregata.zakres:
            return Fregata(pola_statku)
        elif rozmiar in cls.RANGI.niszczyciel.zakres:
            return Niszczyciel(pola_statku)
        elif rozmiar in cls.RANGI.krazownik.zakres:
            return Krazownik(pola_statku)
        elif rozmiar in cls.RANGI.pancernik.zakres:
            return Pancernik(pola_statku)

    def __init__(self, pola):
        self.pola = sorted(pola, key=lambda p: p.kolumna + p.rzad)  # sortowanie od pola najbardziej na NW (self.polozenie) do pola najbardziej na SE
        self.polozenie = self.pola[0]
        self.obwiednia = []  # lista pól obwiedni wokół statku
        self.rozmiar = len(pola)
        self.ofiary = []  # statki przeciwnika zatopione przez ten statek

    def __eq__(self, other):
        """
        Przeładowanie operatora '=='. Statki są równe, jeśli: 1) wszystkie ich pola są równe, 2) ich rangi bazowe są równe i 3) ich nazwy są równe.
        """
        if isinstance(self, other.__class__):
            if self.rozmiar == other.rozmiar:
                for pole_tu, pole_tam in zip(self.pola, other.pola):
                    if pole_tu != pole_tam:
                        return False
                if self.RANGA_BAZOWA != other.RANGA_BAZOWA:
                    return False
                if self.nazwa != other.nazwa:
                    return False
                return True
            return False
        return NotImplemented

    def __str__(self):
        """
        Zwraca informację o statku w formacie:

        ranga "nazwa" (A6) [10/17] **

        gdzie:
        - (A6) to położenie pola najbardziej wysuniętego na NW (self.polozenie)
        - [10/17] to pola nietrafione/wszystkie pola
        - ** - tyle gwiazdek ile dodatkowych salw za zatopienie przeciwnika
        """
        info = '{} "{}" ({}) [{}] '.format(
            self.RANGA_BAZOWA.nazwa,
            self.nazwa,
            str(self.polozenie),
            self.podaj_nietrafione_na_rozmiar()
        )
        for gwiazdka in [self.ORDER for ofiara in self.ofiary]:
            info += gwiazdka
        else:
            info = info[:-1]

        return info

    def ile_otrzymanych_trafien(self):
        """Podaje ilość otrzymanych trafień."""
        licznik_trafien = 0
        for pole in self.pola:
            if pole.znacznik in (Pole.ZNACZNIKI.trafiony, Pole.ZNACZNIKI.zatopiony):
                licznik_trafien += 1
        return licznik_trafien

    def czy_zatopiony(self):
        """Sprawdza czy statek jest zatopiony."""
        if self.ile_otrzymanych_trafien() == self.rozmiar:
            return True
        else:
            return False

    def zatop(self):
        """Zatapia ten statek."""
        for pole in self.pola:
            pole.znacznik = Pole.ZNACZNIKI.zatopiony

    def o_zatopieniu(self):
        """Zwraca komunikat o swoim zatopieniu."""
        if self.RANGA_BAZOWA in self.RANGI[2:4]:  # korweta lub fregata
            return "{} zatopiona!".format(str(self))
        else:
            return "{} zatopiony!".format(str(self))

    def obniz_range(self):
        """Obniża rangę statku jako efekt otrzymanych trafień."""
        indeks = self.RANGI.index(self.ranga) - 1
        if indeks >= 0:  # obniżać można tylko powyżej kutra
            self.ranga = self.RANGI[indeks]
            self.sila_ognia = self.ranga.sila_ognia[:]

    def podaj_nietrafione_na_rozmiar(self):
        """Podaje informację o stosunku nietrafionych do wszystkich pól jako string w formacie: 16/20."""
        nietrafione = self.rozmiar - self.ile_otrzymanych_trafien()
        return str(nietrafione) + "/" + str(self.rozmiar)


class Kuter(Statek):
    """Statek o rozmiarze 1 pola."""

    RANGA_BAZOWA = Statek.RANGI.kuter  # explicit is better than implicit

    def __init__(self, pola):
        super().__init__(pola)
        self.nazwa = self.RANGA_BAZOWA.losuj_nazwe_statku()
        self.ranga = self.RANGA_BAZOWA  # ranga rzeczywista - zależna od ilości trafień
        self.sila_ognia = self.ranga.sila_ognia[:]  # sila_ognia rzeczywista - zależna od aktualnej rangi rzeczywistej


class Patrolowiec(Statek):
    """Statek o rozmiarze 2-3 pól."""

    RANGA_BAZOWA = Statek.RANGI.patrolowiec

    def __init__(self, pola):
        super().__init__(pola)
        self.nazwa = self.RANGA_BAZOWA.losuj_nazwe_statku()
        self.ranga = self.RANGA_BAZOWA  # jw.
        self.sila_ognia = self.ranga.sila_ognia[:]  # jw.


class Korweta(Statek):
    """Statek o rozmiarze 4-6 pól."""

    RANGA_BAZOWA = Statek.RANGI.korweta

    def __init__(self, pola):
        super().__init__(pola)
        self.nazwa = self.RANGA_BAZOWA.losuj_nazwe_statku()
        self.ranga = self.RANGA_BAZOWA  # jw.
        self.sila_ognia = self.ranga.sila_ognia[:]  # jw.


class Fregata(Statek):
    """Statek o rozmiarze 7-9 pól."""

    RANGA_BAZOWA = Statek.RANGI.fregata

    def __init__(self, pola):
        super().__init__(pola)
        self.nazwa = self.RANGA_BAZOWA.losuj_nazwe_statku()
        self.ranga = self.RANGA_BAZOWA  # jw.
        self.sila_ognia = self.ranga.sila_ognia[:]  # jw.


class Niszczyciel(Statek):
    """Statek o rozmiarze 10-12 pól."""

    RANGA_BAZOWA = Statek.RANGI.niszczyciel

    def __init__(self, pola):
        super().__init__(pola)
        self.nazwa = self.RANGA_BAZOWA.losuj_nazwe_statku()
        self.ranga = self.RANGA_BAZOWA  # jw.
        self.sila_ognia = self.ranga.sila_ognia[:]  # jw.


class Krazownik(Statek):
    """Statek o rozmiarze 13-16 pól."""

    RANGA_BAZOWA = Statek.RANGI.krazownik

    def __init__(self, pola):
        super().__init__(pola)
        self.nazwa = self.RANGA_BAZOWA.losuj_nazwe_statku()
        self.ranga = self.RANGA_BAZOWA  # jw.
        self.sila_ognia = self.ranga.sila_ognia[:]  # jw.


class Pancernik(Statek):
    """Statek o rozmiarze 17-20 pól."""

    RANGA_BAZOWA = Statek.RANGI.pancernik

    def __init__(self, pola):
        super().__init__(pola)
        self.nazwa = self.RANGA_BAZOWA.losuj_nazwe_statku()
        self.ranga = self.RANGA_BAZOWA  # jw.
        self.sila_ognia = self.ranga.sila_ognia[:]  # jw.
