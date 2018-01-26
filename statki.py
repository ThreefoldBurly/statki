#!/usr/bin/env python3

"""
Gra w statki na planszy o arbitralnym rozmiarze
"""

import codecs
from random import randint, choice, gauss


class Plansza:
    """Abstrakcyjna reprezentacja planszy do gry w statki"""
    ZNACZNIKI = {
        "pusty": "0",
        "pudło": "x",
        "trafiony": "T",
        "zatopiony": "Z",
        "statek": "&",
        "obwiednia": "."
    }
    MIN_ROZMIAR_STATKU = 1
    MAX_ROZMIAR_STATKU = 20

    def __init__(self, kolumny, rzedy):
        # pola klasy
        self.kolumny = kolumny
        self.rzedy = rzedy
        self.rozmiar = rzedy * kolumny
        self.pola = self.stworz_pola()  # lista rzędów (list) pól
        self.statki = []
        # inicjalizacja
        self.drukuj_sie()
        self.wypelnij_statkami()
        self.drukuj_sie()

    def stworz_pola(self):
        """Tworzy pola planszy"""
        pola = []
        for y in range(1, self.rzedy + 1):
            rzad = []
            for x in range(1, self.kolumny + 1):
                rzad.append(Pole(x, y))
            pola.append(rzad)
        return pola

    def drukuj_sie(self):
        """Drukuje planszę w standard output"""
        # numeracja kolumn
        print()
        print("    " + "  ".join([str(liczba) for liczba in range(1, self.kolumny + 1) if liczba < 10]) + " " + " ".join([str(liczba) for liczba in range(1, self.kolumny + 1) if liczba >= 10]))
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
        """Podaje wskazane pole"""
        return self.pola[rzad - 1][kolumna - 1]

    def oznacz_pole(self, znacznik, kolumna, rzad):
        """Oznacza wskazane polę wskazanym znacznikiem"""
        self.pola[rzad - 1][kolumna - 1].znacznik = znacznik

    def czy_pole_puste(self, kolumna, rzad):
        """Sprawdza czy wskazane pole jest puste"""
        if self.pola[rzad - 1][kolumna - 1].znacznik == self.ZNACZNIKI["pusty"]:
            return True
        else:
            return False

    def czy_pole_w_planszy(self, kolumna, rzad):
        """Sprawdza czy wskazane pole jest w obrębie planszy"""
        if rzad < 1 or rzad > self.rzedy or kolumna < 1 or kolumna > self.kolumny:
            return False
        else:
            return True

    def umiesc_statek(self, rozmiar, kolumna, rzad):
        """
        Stara się umieścić statek o podanym rozmiarze na planszy. Statek rozrasta się w przypadkowych kierunkach ze wskazanego pola początkowego. W razie sukcesu metoda zwraca umieszczony statek, w razie porażki zwraca None (czyszcząc oznaczone wcześniej pola).
        """
        kierunki = ["prawo", "lewo", "gora", "dol"]
        licznik_oznaczen = 0
        licznik_iteracji = 0
        sciezka = []
        ozn_pola = []

        while licznik_oznaczen < rozmiar:

            if licznik_iteracji > rozmiar * 5:  # za dużo iteracji - NIEUDANE UMIESZCZENIE
                return None
            # do testów
            # print()
            # komunikat = "ITERACJA " + str(licznik_iteracji + 1)
            # print(komunikat.center(3 * self.kolumny))

            if licznik_iteracji == 0:  # pole startowe
                if self.czy_pole_w_planszy(kolumna, rzad) and self.czy_pole_puste(kolumna, rzad):
                    self.oznacz_pole(self.ZNACZNIKI["statek"], kolumna, rzad)
                    licznik_oznaczen += 1
                    ozn_pola.append(self.podaj_pole(kolumna, rzad))
                else:
                    return None  # NIEUDANE UMIESZCZENIE
            else:
                oznaczono = False
                pula_kierunkow = kierunki[:]

                while not oznaczono:

                    # obsługa zapętlenia - pętla może się wykonać maksymalnie 4 razy (tyle ile możliwych kierunków ruchu)
                    if len(pula_kierunkow) < 1:  # wyczerpaliśmy wszystkie możliwe kierunki - trzeba wracać (o ile jest gdzie!)
                        if len(sciezka) > 0:
                            ostatni_kierunek = sciezka[len(sciezka) - 1]
                            if ostatni_kierunek == "prawo":
                                kolumna -= 1
                                sciezka.pop()
                                # print("Cofam: '" + sciezka.pop() + "'")  # test
                            elif ostatni_kierunek == "lewo":
                                kolumna += 1
                                sciezka.pop()
                                # print("Cofam: '" + sciezka.pop() + "'")  # test
                            elif ostatni_kierunek == "gora":
                                rzad += 1
                                sciezka.pop()
                                # print("Cofam: '" + sciezka.pop() + "'")  # test
                            elif ostatni_kierunek == "dol":
                                rzad -= 1
                                sciezka.pop()
                                # print("Cofam: '" + sciezka.pop() + "'")  # test
                            # print "Uciekam z zapetlenia"  # test
                            break

                        else:  # nie ma gdzie wracać, jesteśmy w punkcie startowym - NIEUDANE UMIESZCZENIE statku
                            for pole in ozn_pola:  # czyszczenie planszy
                                kolumna, rzad = pole.podaj_wspolrzedne()
                                self.oznacz_pole(self.ZNACZNIKI["pusty"], kolumna, rzad)
                            return None

                    kierunek = pula_kierunkow[randint(0, len(pula_kierunkow) - 1)]
                    if kierunek == "prawo":
                        kolumna += 1
                        if self.czy_pole_w_planszy(kolumna, rzad) and self.czy_pole_puste(kolumna, rzad):
                            self.oznacz_pole(self.ZNACZNIKI["statek"], kolumna, rzad)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            ozn_pola.append(self.podaj_pole(kolumna, rzad))
                            # test
                            # print(kierunek.center(3 * self.kolumny), str(rzad), str(kolumna))
                        else:
                            kolumna -= 1
                            pula_kierunkow.remove(kierunek)
                    elif kierunek == "lewo":
                        kolumna -= 1
                        if self.czy_pole_w_planszy(kolumna, rzad) and self.czy_pole_puste(kolumna, rzad):
                            self.oznacz_pole(self.ZNACZNIKI["statek"], kolumna, rzad)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            ozn_pola.append(self.podaj_pole(kolumna, rzad))
                            # test
                            # print(kierunek.center(3 * self.kolumny), str(rzad), str(kolumna))
                        else:
                            kolumna += 1
                            pula_kierunkow.remove(kierunek)
                    elif kierunek == "gora":
                        rzad -= 1
                        if self.czy_pole_w_planszy(kolumna, rzad) and self.czy_pole_puste(kolumna, rzad):
                            self.oznacz_pole(self.ZNACZNIKI["statek"], kolumna, rzad)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            ozn_pola.append(self.podaj_pole(kolumna, rzad))
                            # test
                            # print(kierunek.center(3 * self.kolumny), str(rzad), str(kolumna))
                        else:
                            rzad += 1
                            pula_kierunkow.remove(kierunek)
                    else:  # idziemy w dół
                        rzad += 1
                        if self.czy_pole_w_planszy(kolumna, rzad) and self.czy_pole_puste(kolumna, rzad):
                            self.oznacz_pole(self.ZNACZNIKI["statek"], kolumna, rzad)
                            oznaczono = True
                            licznik_oznaczen += 1
                            sciezka.append(kierunek)
                            ozn_pola.append(self.podaj_pole(kolumna, rzad))
                            # test
                            # print(kierunek.center(3 * self.kolumny), str(rzad), str(kolumna))
                        else:
                            rzad -= 1
                            pula_kierunkow.remove(kierunek)

            # self.drukuj_sie() #test
            licznik_iteracji += 1

        if rozmiar == 1:
            return Kuter(self, ozn_pola)
        elif rozmiar in range(2, 4):
            return Patrolowiec(self, ozn_pola)
        elif rozmiar in range(4, 7):
            return Korweta(self, ozn_pola)
        elif rozmiar in range(7, 10):
            return Fregata(self, ozn_pola)
        elif rozmiar in range(10, 13):
            return Niszczyciel(self, ozn_pola)
        elif rozmiar in range(13, 17):
            return Krazownik(self, ozn_pola)
        elif rozmiar in range(17, 21):
            return Pancernik(self, ozn_pola)

    def umiesc_obwiednie_statku(self, statek):
        """Umieszcza na planszy obwiednię wskazanego statku"""

        # wystarczy zaznaczyć wszystkich 8 bezpośrednich sąsiadów danego punktu (sprawdzając za kazdym razem czy sa w planszy i czy sa puste)
        for pole in statek.pola:
            kolumna, rzad = pole.podaj_wspolrzedne()
            a = 0  # współczynnik przesunięcia w pionie (x)
            b = 0  # współczynnik przesunięcia w poziomie (y)

            for i in [j for j in range(9) if j != 4]:
                if i in range(3):  # 1szy rząd sąsiadów
                    a = -1
                    b = i - 1
                elif i in range(3, 6):  # 2gi rząd sąsiadów
                    a = 0
                    b = i - 4
                else:  # 3ci rząd sąsiadów
                    a = 1
                    b = i - 7

                x = kolumna + a
                y = rzad + b

                if self.czy_pole_w_planszy(x, y) and self.czy_pole_puste(x, y):
                    self.oznacz_pole(self.ZNACZNIKI["obwiednia"], x, y)

    def podaj_statek(self, pole):
        """Zwraca statek zajmujący podane pole"""
        for statek in self.statki:
            if pole in statek.pola:
                return statek
        return None

    def zatop_statek(self, statek):
        """Oznacza pola wskazanego statku jako zatopione"""
        for pole in statek.pola:
            kolumna, rzad = pole.podaj_wspolrzedne()
            self.oznacz_pole(self.ZNACZNIKI["zatopiony"], kolumna, rzad)

    def wypelnij_statkami(self, zapelnienie=15, odch_st=9, prz_mediany=-7):
        """
        Wypełnia planszę statkami. Każdy kolejny statek ma losowy rozmiar w zakresie 1-20 i jest umieszczany w losowym miejscu. O ilości i rozmiarach statków decydują parametry metody
        """
        # zapelnienie to wyrażony w procentach stosunek sumarycznego rozmiaru umieszczonych
        # statków do rozmiaru planszy

        # odch_st to odchylenie standardowe w rozkładzie Gaussa, z którego losowany
        # jest rozmiar statku
        # czym wyższa wartość, tym większy rozrzut rozmiarów

        # prz_mediany to przesunięcie mediany w rozkładzie Gaussa, z którego losowany
        # jest rozmiar statku
        # wartość ujemna spowoduje losowanie większej ilości małych statków
        # wartość dodatnia spowodują losowanie większej ilości dużych statków
        # zero (brak przesunięcia) powoduje losowanie wg standardowego rozkładu normalnego,
        # gdzie mediana jest średnią arytmetyczną przedziału losowania

        # wartości domyślne parametrów zostały ustalone po testach
        # większa granulacja rozmiarów statków (z zapewnieniem sporadycznego występowania dużych
        # statków) zapewnia ciekawszą grę

        def podaj_int_z_rozkladu_Gaussa(mediana, odch_st, minimum, maximum, prz_mediany=0):
            """
            Podaje losowy int wg rozkładu Gaussa we wskazanym przedziale oraz ze wskazanym przesunięciem mediany. Liczby spoza zadanego przedziału zwracane przez random.gauss() są odbijane proporcjonalnie do wewnątrz przedziału. PRZYKŁAD: dla przedziału <1, 20>, jeśli random.gauss() zwraca -2, to zwróconą liczbą będzie 3, jeśli -5, to 6 jeśli random.gauss() zwraca 22, to zwróconą liczbą, będzie 19, jeśli 27, to 14.
            """
            i = int(round(gauss(mediana + prz_mediany, odch_st)))
            if i < minimum:
                i = minimum - i
                if i > maximum:  # odbicie do wewnątrz przedziału jest jednokrotne (jeśli odbite minimum- miałoby wyjść poza zadany przedział, jest przycinane do maximum bez odbicia)
                    i = maximum
            if i > maximum:
                i = maximum - (i - maximum) + 1
                if i < minimum:  # odbicie do wewnątrz przedziału jest jednokrotne (jeśli odbite maximum+ miałoby wyjść poza zadany przedział, jest przycinane do minimum bez odbicia)
                    i = minimum
            return i

        mediana = (self.MIN_ROZMIAR_STATKU + self.MAX_ROZMIAR_STATKU) / 2.0  # 10.5

        licznik_iteracji = 0
        sum_rozmiar_statkow = int(self.rozmiar * zapelnienie / 100)
        akt_rozmiar_statkow = sum_rozmiar_statkow

        while akt_rozmiar_statkow > 0:
            rozmiar_statku = podaj_int_z_rozkladu_Gaussa(mediana, odch_st, self.MIN_ROZMIAR_STATKU, self.MAX_ROZMIAR_STATKU, prz_mediany)
            if rozmiar_statku > akt_rozmiar_statkow:
                continue
            pole_startowe_x = randint(1, self.kolumny)
            pole_startowe_y = randint(1, self.rzedy)

            umieszczony_statek = self.umiesc_statek(rozmiar_statku, pole_startowe_x, pole_startowe_y)

            if umieszczony_statek is not None:
                self.umiesc_obwiednie_statku(umieszczony_statek)
                self.statki.append(umieszczony_statek)
                # print("\nUmieszczony statek: {} {}".format(umieszczony_statek.ranga, umieszczony_statek.rozmiar)  # test
                akt_rozmiar_statkow -= rozmiar_statku

            # obsługa wyjścia
            if licznik_iteracji > sum_rozmiar_statkow * 10:  # wielkość do przetestowania
                print("Ilość iteracji pętli zapełniającej planszę statkami większa od oczekiwanej. Nastąpiło przedwczesne przerwanie petli. Umieszczono mniej statków")  # test
                break

            licznik_iteracji += 1

        self.statki.sort(key=lambda s: s.rozmiar, reverse=True)  # nie wierzę że to było takie proste!

        # do testów
        sum_rozmiar = 0
        for statek in self.statki:
            sum_rozmiar += statek.rozmiar
            print('\nUmieszczony statek: {} "{}" [{}]'.format(statek.ranga, statek.nazwa, statek.rozmiar))
        print("\nWszystkich umieszczonych statków: {}. Ich sumaryczny rozmiar: [{}]".format(len(self.statki), sum_rozmiar))


class Pole:
    """Abstrakcyjna reprezentacja pola planszy"""

    def __init__(self, kolumna, rzad, znacznik=Plansza.ZNACZNIKI["pusty"]):
        self.kolumna = kolumna
        self.rzad = rzad
        self.znacznik = znacznik

    def __str__(self):
        """Zwraca informację o polu w formacie: (kolumna,rzad)"""
        return "({},{})".format(self.kolumna, self.rzad)

    # przeładowanie operatora "==" (wzięte z: https://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes)
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    # przeładowanie operatora "=="
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def podaj_wspolrzedne(self):
        return (self.kolumna, self.rzad)


class Parser:
    """Parsuje nazwy statków z 'dane/nazwy.sti'"""

    @staticmethod
    def sparsuj_nazwy(rangi):
        """Parsuje z pliku tekstowego 'dane/nazwy.sti' listę nazw dla każdej rangi statku (całość jako słownik)"""
        nazwy = {}

        def parsuj_wg_rangi(linie, ranga):  # funkcja pomocnicza dla bloku poniżej
            lista_nazw = []
            for linia in linie:
                if ranga in linia:
                    linia = linia.rstrip('\n')
                    lista_nazw.append(linia.split(':::')[0])
            return lista_nazw

        linie = []
        with codecs.open('dane/nazwy.sti', encoding='utf-8') as plik:
            for linia in plik:
                linie.append(linia)

        for ranga in rangi:
            lista_nazw = parsuj_wg_rangi(linie, ranga)
            print("\nRanga: {}. Dodano nazw: [{}]".format(ranga, len(lista_nazw)))  # test
            nazwy[ranga] = lista_nazw

        def czy_nazwy_OK():  # czy do wszystkich rang statków przypisano jakieś nazwy?
            czy_OK = True
            for ranga in nazwy:
                if len(nazwy[ranga]) == 0:
                    czy_OK = False
            return czy_OK

        assert czy_nazwy_OK(), "Nieudane parsowanie nazw statków. Brak pliku 'dane/nazwy.sti' lub plik nie zawiera danych w prawidłowym formacie"

        return nazwy

    @staticmethod
    def sklonuj_nazwy(nazwy_wg_rangi):
        """
        Klonuje słownik nazw wg rangi, wykonując kopię każdej składowej listy
        """
        nazwy = {}
        for klucz in nazwy_wg_rangi:
            nazwy[klucz] = nazwy_wg_rangi[klucz][:]
        return nazwy


class Statek:
    """Abstrakcyjna reprezentacja statku"""

    RANGI = ["kuter", "patrolowiec", "korweta", "fregata", "niszczyciel", "krążownik", "pancernik"]
    NAZWY_WG_RANGI = Parser.sparsuj_nazwy(RANGI)  # słownik w formacie {ranga: [lista nazw]}
    pula_nazw = Parser.sklonuj_nazwy(NAZWY_WG_RANGI)  # słownik zawierający listy (wg rang statków) aktualnie dostępnych nazw dla instancji klasy
    rzymskie = dict([[ranga, ["II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]] for ranga in RANGI])

    def __init__(self, plansza, pola):
        self.plansza = plansza
        self.pola = sorted(pola, key=lambda p: p.kolumna + p.rzad)  # lista pól posortowana od pola najbardziej na NW do pola najbardziej na SE
        self.polozenie = self.pola[0]
        self.rozmiar = len(pola)
        self.czy_zatopiony = False
        self.zatopione = []  # lista statków przeciwnika zatopionych przez ten statek
        self.ranga = None  # implementacja w klasach potomnych
        self.nazwa = None  # implementacja w klasach potomnych
        self.salwy = None  # implementacja w klasach potomnych

    def __str__(self):
        """
        Zwraca informację o statku w formacie:

        ranga "nazwa" (4,5) [10/17] **

        gdzie:
        - (4,5) to położenie pola najbardziej wysuniętego na NW (self.polozenie)
        - [10/17] to pola nietrafione/wszystkie pola
        - ** - tyle gwiazdek ile dodatkowych salw za zatopienie przeciwnika
        """
        nietrafione = self.rozmiar - self.ile_otrzymanych_trafien()
        info = '{} "{}" {} [{}/{}] '.format(
            self.ranga,
            self.nazwa,
            str(self.polozenie),
            str(nietrafione),
            str(self.rozmiar)
        )
        for gwiazdka in ["*" for zatopiony in self.zatopione]:
            info += gwiazdka

        return info

    @classmethod
    def zresetuj_nazwy(cls, ranga):
        """
        Resetuje wyczerpaną listę nazw dostępnych dla instancji klasy, pobierając ze stałej modułu wspolne.py pełną listę nazw, dodając do każdej nazwy kolejny liczebnik rzymski i zwracając tak zmienioną listę
        """
        assert len(cls.rzymskie[ranga]) > 0, "Wyczerpano liczbę możliwych nazw dla statków"
        rzymska = cls.rzymskie[ranga][0]

        nowa_lista = []
        for nazwa in NAZWY_WG_RANGI[ranga]:
            nowa_lista.append(u" ".join([nazwa, rzymska]))

        cls.rzymskie[ranga].remove(rzymska)
        return nowa_lista

    @classmethod
    def losuj_nazwe(cls, ranga):
        """
        Losuje nazwę dla statku o określonej randze z listy w polu klasy. By zapewnić unikalność statku, nazwa po użyciu jest usuwana z listy
        """
        lista_nazw = Statek.pula_nazw[ranga]
        if len(lista_nazw) > 0:
            nazwa = choice(lista_nazw)
        else:  # obsługa wyczerpania dostępnych nazw dla danej rangi
            lista_nazw = Statek.pula_nazw[ranga] = cls.zresetuj_nazwy(ranga)
            nazwa = choice(lista_nazw)

        lista_nazw.remove(nazwa)
        return nazwa

    def ile_otrzymanych_trafien(self):
        """Podaje ilość otrzymanych trafień"""
        licznik_trafien = 0
        for pole in self.pola:
            kolumna, rzad = pole.podaj_wspolrzedne()
            if self.plansza.pola[rzad - 1][kolumna - 1].znacznik in (Plansza.ZNACZNIKI["trafiony"], Plansza.ZNACZNIKI["zatopiony"]):
                licznik_trafien += 1
        return licznik_trafien


class Kuter(Statek):
    """Statek o rozmiarze 1 pola"""

    RANGA = Statek.RANGI[0]
    SALWY = [1]
    SYMBOL = "T"

    def __init__(self, plansza, pola):
        super().__init__(plansza, pola)
        self.ranga = self.RANGA  # ranga rzeczywista - zależna od ilości trafień
        self.nazwa = self.losuj_nazwe(self.ranga)
        self.salwy = self.SALWY  # salwy rzeczywiste - zależne od aktualnej rangi rzeczywistej


class Patrolowiec(Statek):
    """Statek o rozmiarze 2-3 pól"""

    RANGA = Statek.RANGI[1]
    SALWY = [2]
    SYMBOL = "L"

    def __init__(self, plansza, pola):
        super().__init__(plansza, pola)
        self.ranga = self.RANGA  # ranga rzeczywista - zależna od ilości trafień
        self.nazwa = self.losuj_nazwe(self.ranga)
        self.salwy = self.SALWY  # salwy rzeczywiste - zależne od aktualnej rangi rzeczywistej


class Korweta(Statek):
    """Statek o rozmiarze 4-6 pól"""

    RANGA = Statek.RANGI[2]
    SALWY = [3]
    SYMBOL = "W"

    def __init__(self, plansza, pola):
        super().__init__(plansza, pola)
        self.ranga = self.RANGA  # ranga rzeczywista - zależna od ilości trafień
        self.nazwa = self.losuj_nazwe(self.ranga)
        self.salwy = self.SALWY  # salwy rzeczywiste - zależne od aktualnej rangi rzeczywistej


class Fregata(Statek):
    """Statek o rozmiarze 7-9 pól"""

    RANGA = Statek.RANGI[3]
    SALWY = [2, 2]
    SYMBOL = "F"

    def __init__(self, plansza, pola):
        super().__init__(plansza, pola)
        self.ranga = self.RANGA  # ranga rzeczywista - zależna od ilości trafień
        self.nazwa = self.losuj_nazwe(self.ranga)
        self.salwy = self.SALWY  # salwy rzeczywiste - zależne od aktualnej rangi rzeczywistej


class Niszczyciel(Statek):
    """Statek o rozmiarze 10-12 pól"""

    RANGA = Statek.RANGI[4]
    SALWY = [3, 2]
    SYMBOL = "N"

    def __init__(self, plansza, pola):
        super().__init__(plansza, pola)
        self.ranga = self.RANGA  # ranga rzeczywista - zależna od ilości trafień
        self.nazwa = self.losuj_nazwe(self.ranga)
        self.salwy = self.SALWY  # salwy rzeczywiste - zależne od aktualnej rangi rzeczywistej


class Krazownik(Statek):
    """Statek o rozmiarze 13-16 pól"""

    RANGA = Statek.RANGI[5]
    SALWY = [3, 3]
    SYMBOL = "K"

    def __init__(self, plansza, pola):
        super().__init__(plansza, pola)
        self.ranga = self.RANGA  # ranga rzeczywista - zależna od ilości trafień
        self.nazwa = self.losuj_nazwe(self.ranga)
        self.salwy = self.SALWY  # salwy rzeczywiste - zależne od aktualnej rangi rzeczywistej


class Pancernik(Statek):
    """Statek o rozmiarze 17-20 pól"""

    RANGA = Statek.RANGI[6]
    SALWY = [3, 2, 2]
    SYMBOL = "P"

    def __init__(self, plansza, pola):
        super().__init__(plansza, pola)
        self.ranga = self.RANGA  # ranga rzeczywista - zależna od ilości trafień
        self.nazwa = self.losuj_nazwe(self.ranga)
        self.salwy = self.SALWY  # salwy rzeczywiste - zależne od aktualnej rangi rzeczywistej
