"""

    statki.plansza
    ~~~~~~~~~~~~~~

    Plansza gry wraz z jej podstawowymi elementami.

"""

# TODO: skrócić wszystkie gettery o "podaj", lepiej usystematyzować nazwy metod

from random import randint, choice, gauss
from decimal import Decimal as D
from collections import namedtuple

from statki.pamiec import Parser


class Plansza:
    """
    Plansza gry złożona z pól. Zapisuje całą informację o stanie gry po stronie jednego gracza w danym momencie. Na początku gry tworzone są 2 obiekty tej klasy - jeden dla gracza, drugi dla przeciwnika. Moduł `statki.gui.plansza` powiela tę dychotomię.
    """
    ALFABET = {
        1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J",
        11: "K", 12: "L", 13: "M", 14: "N", 15: "O", 16: "P", 17: "Q", 18: "R", 19: "S", 20: "T",
        21: "U", 22: "V", 23: "W", 24: "X", 25: "Y", 26: "Z", 27: "AA", 28: "AB", 29: "AC",
        30: "AD", 31: "AE", 32: "AF", 33: "AG", 34: "AH", 35: "AI", 36: "AJ", 37: "AK", 38: "AL",
        39: "AM", 40: "AN"
    }
    MIN_KOLUMNY, MAX_KOLUMNY = Parser.podaj_minmax_kolumny()
    MIN_RZEDY, MAX_RZEDY = Parser.podaj_minmax_rzedy()
    MIN_ROZMIAR_STATKU, MAX_ROZMIAR_STATKU = Parser.podaj_minmax_rozmiar_statku()
    ZAPELNIENIE, ODCH_ST, PRZ_MEDIANY = Parser.podaj_parametry_wypelniania()

    Kierunki = namedtuple("Kierunki", "E S W N NE SE SW NW")
    KIERUNKI = Kierunki._make(Kierunki._fields)

    def __init__(self, kolumny, rzedy):
        self.sprawdz_wymiary(kolumny, rzedy)
        self.kolumny, self.rzedy, self.rozmiar = kolumny, rzedy, rzedy * kolumny
        self.pola = self.stworz_pola()  # matryca pól (krotka krotek (rzędów))
        self.statki = []
        self.wypelnij_statkami(self.ZAPELNIENIE, self.ODCH_ST, self.PRZ_MEDIANY)
        self.sprawdz_statki()
        # self.o_statkach()  # test
        # self.drukuj()  # test
        self.ilosc_pol_statkow = sum([statek.rozmiar for statek in self.statki])
        # TODO: zamienić na generatory
        self.zatopione = []  # statki zatopione tej planszy
        self.niezatopione = self.statki[:]  # statki niezatopione tej planszy

    def sprawdz_wymiary(self, kolumny, rzedy):
        """Sprawdź wymiary planszy podane przy inicjalizacji."""
        if kolumny not in range(self.MIN_KOLUMNY, self.MAX_KOLUMNY + 1) or rzedy not in range(
                self.MIN_RZEDY, self.MAX_RZEDY + 1):
            tekst_bledu = "Błąd wymiarów planszy. "
            tekst_bledu += "Prawidłowe wymiary planszy to: {}-{} kolumn x {}-{} rzędów. "
            tekst_bledu += "Otrzymane wymiary: {} x {}."
            raise ValueError(tekst_bledu.format(
                self.MIN_KOLUMNY, self.MAX_KOLUMNY,
                self.MIN_RZEDY, self.MAX_RZEDY,
                str(kolumny), str(rzedy)
            ))

    def stworz_pola(self):
        """Stwórz pola planszy."""
        pola = []
        for y in range(1, self.rzedy + 1):
            rzad = []
            for x in range(1, self.kolumny + 1):
                rzad.append(Pole(id(self), x, y))
            pola.append(rzad)
        return tuple(tuple(rzad) for rzad in pola)

    def drukuj(self):  # do testów
        """Drukuj planszę w standard output."""
        # numeracja kolumn
        print()
        print("##### PLANSZA #####".center(self.kolumny * 3 + 2))
        print()
        print("    " + "  ".join([self.ALFABET[liczba] for liczba in range(1, self.kolumny + 1)]))
        print()
        for i, rzad in enumerate(self.pola):
            # numeracja rzędów
            if i + 1 < 10:
                print(str(i + 1) + "  ", end=" ")
            else:
                print(str(i + 1) + " ", end=" ")
            # właściwe pola planszy
            print("  ".join([pole.znacznik for pole in rzad]))
        print()

    def podaj_pole(self, kolumna, rzad):
        """
        Podaj pole wg wskazanych współrzędnych. Jeśli podane współrzędne wykraczają poza zakres planszy zwróć None.
        """
        if self.czy_w_planszy(kolumna, rzad):
            return self.pola[rzad - 1][kolumna - 1]
        else:
            return None

    def czy_w_planszy(self, kolumna, rzad):
        """Sprawdź czy wskazane wspolrzedne są w obrębie planszy."""
        if rzad < 1 or rzad > self.rzedy or kolumna < 1 or kolumna > self.kolumny:
            return False
        else:
            return True

    def podaj_sasiednie_pole(self, pole, kierunek):
        """Podaj pole sąsiednie dla wskazanego pola wg podanego kierunku."""
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
        Spróbuj umieścić statek o podanym rozmiarze na planszy. Statek rozrasta się w przypadkowych kierunkach ze wskazanego pola początkowego. W razie sukcesu zwróć umieszczony statek, w razie porażki zwróć None (czyszcząc oznaczone wcześniej pola).
        """
        licznik_iteracji = 0
        pola_statku = []
        pole = self.podaj_pole(kolumna, rzad)  # pole początkowe

        def dodaj_pole_statku(pole):
            pole.znacznik = Pole.ZNACZNIKI.statek
            pola_statku.append(pole)

        while len(pola_statku) < rozmiar:
            if licznik_iteracji > rozmiar * 10:  # za dużo iteracji - NIEUDANE UMIESZCZENIE
                return None

            if licznik_iteracji == 0:  # pole początkowe
                if pole is not None and pole.znacznik == Pole.ZNACZNIKI.pusty:
                    dodaj_pole_statku(pole)
                else:
                    return None  # NIEUDANE UMIESZCZENIE
            else:
                pula_kierunkow = list(self.KIERUNKI[:4])

                while True:
                    if not pula_kierunkow:  # powrót po wyczerpaniu kierunków
                        indeks = pola_statku.index(pole)
                        if indeks:
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
        """Umieść na planszy i w statku obwiednię wskazanego statku."""
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
        """Podaj statek zajmujący wskazane pole (które może mieć postać stringa)."""
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
        Wypełnij planszę statkami. Każdy kolejny statek ma losowy rozmiar w określonym przez planszę zakresie i jest umieszczany w losowym miejscu. O ilości i rozmiarach statków decydują parametry.

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
            Podaj rozmiar statku jako losową liczbę całkowitą wg rozkładu Gaussa we wskazanym przedziale oraz ze wskazanym przesunięciem mediany. Liczby losowane spoza żądanego przedziału są ignorowane.
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
            rozmiar_statku = podaj_rozmiar_z_rozkladu_Gaussa(
                mediana,
                odch_st,
                self.MIN_ROZMIAR_STATKU,
                self.MAX_ROZMIAR_STATKU,
                prz_mediany
            )
            if rozmiar_statku > akt_rozmiar_statkow:
                continue
            pole_startowe_x = randint(1, self.kolumny)
            pole_startowe_y = randint(1, self.rzedy)

            umieszczony_statek = self.umiesc_statek(
                pole_startowe_x,
                pole_startowe_y,
                rozmiar_statku
            )

            if umieszczony_statek is not None:
                self.umiesc_obwiednie_statku(umieszczony_statek)
                self.statki.append(umieszczony_statek)
                akt_rozmiar_statkow -= rozmiar_statku

            # obsługa wyjścia
            if licznik_iteracji > sum_rozmiar_statkow * 50:  # wielkość do przetestowania
                print(  # test
                    "Ilość iteracji pętli zapełniającej planszę statkami"
                    "większa od oczekiwanej ({})".format(sum_rozmiar_statkow * 50),
                    "Nastąpiło przedwczesne przerwanie petli."
                    " Umieszczono mniej statków ({})".format(len(self.statki))
                )
                break

            licznik_iteracji += 1

        self.statki.sort(key=lambda s: s.rozmiar, reverse=True)  # od największego do najmniejszego

    def sprawdz_pola_statku(self, statek):
        """Zweryfikuj poprawność pól wskazanego statku."""

        # unikalność pól
        if len(statek.pola) != len(set(statek.pola)):
            tekst_bledu = "Błąd pól statku: {}. "
            tekst_bledu += "Statek może składać się tylko z unikalnych pól"
            tekst_bledu += "Otrzymane pola statku zawierają duplikaty: {}. "
            raise ValueError(tekst_bledu.format(
                str(statek),
                [str(pole) for pole in statek.pola]
            ))

        # ortogonalne sąsiedztwo pól
        def czy_nastepne_pole_sasiadem(pole, nastepne_pole):
            """Sprawdza czy następne pole jest sąsiadem"""
            pula_kierunkow = list(Plansza.KIERUNKI[:4])
            while pula_kierunkow:
                kierunek = pula_kierunkow[0]
                sasiad = self.podaj_sasiednie_pole(pole, kierunek)
                if sasiad == nastepne_pole:
                    return True
                else:
                    pula_kierunkow.remove(kierunek)
            return False

        pola_do_sprawdzenia = statek.pola[:]
        pola_sprawdzone = []

        while pola_do_sprawdzenia:
            pole = pola_do_sprawdzenia[0]

            if len(pola_do_sprawdzenia) > 1:
                nastepne_pole = pola_do_sprawdzenia[1]
                if czy_nastepne_pole_sasiadem(pole, nastepne_pole):
                    pola_sprawdzone.append(pole)
                    pola_do_sprawdzenia.remove(pole)
                else:
                    sciezka_cofania = pola_sprawdzone[::-1]
                    # ostatnie pole przed powrotem należy dodać do sprawdzonych i usunąć ze sprawdzanych
                    pola_sprawdzone.append(pole)
                    pola_do_sprawdzenia.remove(pole)

                    while sciezka_cofania:
                        pole = sciezka_cofania[0]
                        if czy_nastepne_pole_sasiadem(pole, nastepne_pole):
                            break
                        else:
                            sciezka_cofania.remove(pole)

                    if not sciezka_cofania:
                        tekst_bledu = "Błąd pól statku: {}. "
                        tekst_bledu += "Statek może składać się tylko z pól sąsiadujących"
                        tekst_bledu += " ze sobą ortogonalnie. Otrzymane pola statku: {}. "
                        tekst_bledu += "Pole nie sąsiadujące ortogonalnie: {}."
                        raise ValueError(tekst_bledu.format(
                            str(statek),
                            [str(pole) for pole in statek.pola],
                            nastepne_pole
                        ))
            else:
                break

    def sprawdz_statki(self):
        """Zweryfikuj poprawność umieszczonych statków."""
        for statek in self.statki:
            self.sprawdz_pola_statku(statek)

    def stworz_statek(self, *wspolrzedne):
        """Stwórz statek z pól o podanych współrzędnych (tylko dla testów jednostkowych)."""
        if len(wspolrzedne) not in range(self.MIN_ROZMIAR_STATKU, self.MAX_ROZMIAR_STATKU + 1):
            raise ValueError("Błąd tworzenia statku. Podano złą ilość współrzędnych pól.")

        pola_statku = [self.podaj_pole(kolumna, rzad) for kolumna, rzad in wspolrzedne]
        for pole in pola_statku:
            if pole is None:
                raise ValueError("Błąd tworzenia statku. Podano współrzędne pól spoza planszy.")
            pole.znacznik = Pole.ZNACZNIKI.statek
        return Statek.fabryka(pola_statku)

    def stworz_salwe(self, zrodlo, *wspolrzedne):  # TODO
        """Stwórz salwę z pól o podanych współrzędnych (tylko dla testów jednostkowych)."""
        if len(wspolrzedne) not in range(Salwa.MIN_ROZMIAR, Salwa.MAX_ROZMIAR + 1):
            raise ValueError("Błąd tworzenia salwy. Podano złą ilość współrzędnych pól.")
        pola_salwy = [self.podaj_pole(kolumna, rzad) for kolumna, rzad in wspolrzedne]
        self.odkryj_pola([pole for pole in pola_salwy if pole is not None])
        return Salwa(zrodlo, pola_salwy)

    def odkryj_pola(self, pola):
        """Odkryj wskazane pola."""
        for pole in pola:
            if pole.znacznik in (Pole.ZNACZNIKI.pusty, Pole.ZNACZNIKI.obwiednia):
                pole.znacznik = Pole.ZNACZNIKI.pudlo
            elif pole.znacznik == Pole.ZNACZNIKI.statek:
                pole.znacznik = Pole.ZNACZNIKI.trafiony

    def oznacz_zatopione(self):
        """Oznacz statki posiadające wszystkie pola trafione jako zatopione."""
        for statek in self.niezatopione[:]:
            if not statek.czy_zatopiony():
                if all(True for pole in statek.pola if pole.znacznik == Pole.ZNACZNIKI.trafiony):
                    statek.zatop()
                    self.niezatopione.remove(statek)
                    self.zatopione.append(statek)

    def o_statkach(self):  # do testów
        """Drukuj informację o umieszczonych statkach"""
        print()
        print()
        print("##### STATKI #####".center(self.kolumny * 3 + 2))
        sum_rozmiar = 0
        for statek in self.statki:
            sum_rozmiar += statek.rozmiar
            print('\nUmieszczony statek: {} "{}" [{}]'.format(
                statek.RANGA_BAZOWA.nazwa,
                statek.nazwa,
                statek.rozmiar
            ))

        print("\nWszystkich umieszczonych statków: {}. Ich sumaryczny rozmiar: [{}]".format(
            len(self.statki),
            sum_rozmiar
        ))

    def podaj_ilosc_niezatopionych_wg_rang(self):
        """
        Podaj zestawienie ilości niezatopionych statków wg rang w postaci słownika w formacie {'ranga': ilość}
        """
        lista_rang = [statek.RANGA_BAZOWA.nazwa for statek in self.niezatopione]
        return dict([(ranga.nazwa, lista_rang.count(ranga.nazwa)) for ranga in Statek.RANGI])

    def podaj_ilosc_zatopionych_wg_rang(self):
        """
        Podaj zestawienie ilości zatopionych statków wg rang w postaci słownika w formacie {'ranga': ilość}
        """
        lista_rang = [statek.RANGA_BAZOWA.nazwa for statek in self.zatopione]
        return dict([(ranga.nazwa, lista_rang.count(ranga.nazwa)) for ranga in Statek.RANGI])

    def podaj_ilosc_nietrafionych_pol(self):
        """Podaj ilość nietrafionych pól statków. Pola zatopione traktowane są jak trafione."""
        licznik = 0
        for statek in self.statki:
            for pole in statek.pola:
                if pole.znacznik in (Pole.ZNACZNIKI.trafiony, Pole.ZNACZNIKI.zatopiony):
                    licznik += 1
        return self.ilosc_pol_statkow - licznik  # int

    def podaj_info_o_nietrafionych(self):
        """
        Podaj informację o nietrafionych polach w postaci 2 stringów: ilości nietrafionych pól planszy oraz stosunku nietrafionych pól statków do wszystkich pól zajętych przez statki w procentach.
        """
        nietrafione = D(self.podaj_ilosc_nietrafionych_pol())
        wszystkie = D(self.ilosc_pol_statkow)
        procent = round(nietrafione * 100 / wszystkie, 1)
        return str(nietrafione), str(procent) + "%"


class Pole:
    """
    Pole planszy. Posiada 6 podstawowych stanów oznaczonych znacznikami. Trzy pierwsze są używane przy inicjalizacji planszy (pola zakryte), podczas gry trzy pozostałe pojawiają się tylko jako efekt działań graczy (pola odkryte).
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
        """Zwróć informację o polu w formacie: litera kolumny+cyfra rzędu np. B9"""
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
        Przeładowanie operatora "==" (dla porównań przy poprawnej obsłudze wyjątkowości w zbiorach).
        """
        return hash(tuple(sorted(self.__dict__.items())))

    def podaj_wspolrzedne(self):
        """Podaj współrzędne pola."""
        return self.kolumna, self.rzad

    def str_w_nawiasach(self):
        """Zwróć informację o polu w formacie __str__ , dodając nawiasy, np. (B9)"""
        return "(" + str(self) + ")"


class Salwa:
    """Kolekcja pól planszy, w które strzela napastnik wraz ze źródłem (jego położeniem)."""
    # UWAGA - nie są to pola planszy napastnika

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
    MIN_ROZMIAR, MAX_ROZMIAR = Parser.podaj_minmax_rozmiar_salwy()

    @staticmethod
    def filtruj_pola(pola):
        """Filtruj niewypały (strzały poza planszę) od prawidłowych pól salwy."""
        pola = [pole for pole in pola if pole is not None]
        return sorted(pola, key=lambda p: p.kolumna + p.rzad)  # sortowanie od pola najbardziej na NW (self.polozenie) do pola najbardziej na SE

    def __init__(self, zrodlo, pola):
        self.zrodlo = zrodlo  # polozenie statku który oddał salwę
        self.pola = self.filtruj_pola(pola)  # w otrzymanych polach może być None
        self.niewypaly = [None for pole in pola if pole is None]  # strzały poza planszę
        self.trafienia = [True if pole.znacznik in (
            Pole.ZNACZNIKI.trafiony,
            Pole.ZNACZNIKI.zatopiony
        ) else False for pole in self.pola]
        self.pudla = [True if pole.znacznik == Pole.ZNACZNIKI.pudlo
                      else False for pole in self.pola]
        self.sprawdz_rozmiar()
        self.sprawdz_pola()

    def __eq__(self, other):
        """
        Przeładowanie operatora '=='. Salwy są równe, jeśli: 1) mają to samo źródło, 2) mają tyle samo pól i 3) wszystkie ich pola są równe.
        """
        if isinstance(self, other.__class__):
            if self.zrodlo == other.zrodlo:
                if len(self) == len(other):
                    for pole_tu, pole_tam in zip(self.pola, other.pola):
                        if pole_tu != pole_tam:
                            return False
                    return True
                return False
            return False
        return NotImplemented

    def __str__(self):
        """
        Zwróć reprezentację salwy w postaci współrzędnych pól w formacie: (A5), (B4) i (C6). Zakłada 1-3 pola jako dopuszczalny rozmiar salwy.
        """
        pola_tekst = ["(" + str(pole) + ")" for pole in self.pola]
        if len(self.pola) == 1:
            return pola_tekst[0]
        elif len(self.pola) == 2:
            return " i ".join(pola_tekst)
        elif len(self.pola) == 3:
            return pola_tekst[0] + ", " + " i ".join(pola_tekst[1:])
        else:
            tekst_bledu = "Błąd konwersji do str."
            tekst_bledu += " Nieobsługiwana ilość pól salwy: {}."
            raise ValueError(tekst_bledu.format(len(self)))

    def __len__(self):
        return len(self.pola) + len(self.niewypaly)

    def sprawdz_rozmiar(self):
        """Zweryfikuj rozmiar tworzonej salwy."""
        if len(self) not in range(self.MIN_ROZMIAR, self.MAX_ROZMIAR + 1):
            tekst_bledu = "Błąd rozmiaru salwy. Salwa może składać się z {}-{} pól. "
            tekst_bledu += "Otrzymany rozmiar: {}"
            raise ValueError(tekst_bledu.format(self.MIN_ROZMIAR, self.MAX_ROZMIAR, len(self)))

    # TODO: przenieść tworzenie i sprawdzanie salw do Planszy
    def sprawdz_pola(self):
        """Zweryfikuj poprawność pól tworzonej salwy."""
        sumy_wsplrz = [pole.kolumna + pole.rzad for pole in self.pola]
        if len(sumy_wsplrz) > 1:
            roznice = [sumy_wsplrz[i + 1] - sumy_wsplrz[i] for i in range(len(sumy_wsplrz) - 1)]
            if sum(roznice) == 0 or any(False if roznica in range(2) else True
                                        for roznica in roznice):
                tekst_bledu = "Błąd pól salwy. Salwa może składać się tylko z pól "
                tekst_bledu += "sąsiadujących ze sobą ortogonalnie. Otrzymane pola: {}."
                raise ValueError(tekst_bledu.format([str(pole) for pole in self.pola]))


class Statek:
    """Statek. Klasa abstrakcyjna - inicjalizowane są tylko obiekty klas potomnych."""

    RANGI = Parser.podaj_rangi()  # namedtuple
    ORDER = "★"  # TODO

    @classmethod
    def fabryka(cls, pola_statku):
        """Twórz z podanych pól statek odpowiedniej rangi."""
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
        self.pola = pola
        self.polozenie = sorted(pola, key=lambda p: p.kolumna + p.rzad)[0]
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
        Zwróć informację o statku w formacie:

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
        """Podaj ilość otrzymanych trafień."""
        licznik_trafien = 0
        for pole in self.pola:
            if pole.znacznik in (Pole.ZNACZNIKI.trafiony, Pole.ZNACZNIKI.zatopiony):
                licznik_trafien += 1
        return licznik_trafien

    def czy_zatopiony(self):
        """Sprawdź czy statek jest zatopiony."""
        if self.ile_otrzymanych_trafien() == self.rozmiar:
            return True
        else:
            return False

    def zatop(self):
        """Zatop ten statek."""
        for pole in self.pola:
            pole.znacznik = Pole.ZNACZNIKI.zatopiony

    def o_zatopieniu(self):
        """Zwróć komunikat o swoim zatopieniu."""
        if self.RANGA_BAZOWA in self.RANGI[2:4]:  # korweta lub fregata
            return "{} zatopiona!".format(str(self))
        else:
            return "{} zatopiony!".format(str(self))

    def obniz_range(self):
        """Obniż rangę statku (na skutek otrzymanych trafień)."""
        indeks = self.RANGI.index(self.ranga) - 1
        if indeks >= 0:  # obniżać można tylko powyżej kutra
            self.ranga = self.RANGI[indeks]
            self.sila_ognia = self.ranga.sila_ognia[:]

    def podaj_nietrafione_na_rozmiar(self):
        """
        Podaj informację o stosunku pól nietrafionych do wszystkich pól jako string w formacie: 16/20.
        """
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
