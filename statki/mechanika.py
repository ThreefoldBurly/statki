"""

    statki.mechanika
    ~~~~~~~~~~~~~~~~

    Mechanika i przebieg gry w rozbiciu na tury i rundy. Gra składa się z tur, które składają się z rund. Runda odpowiada atakowi pojedynczego statku na pola planszy przeciwnika podzielonemu na salwy. Ilość salw oddawanych przez statek w rundzie zależy od jego aktualnej siły ognia. Tura składa się z tylu rund ile statków na planszy może atakować (nie są zatopione). Gra składa się z tak wielu tur, jak wiele razy po wykonaniu wszystkich ataków na planszy atakującego gracza pozostał jeszcze jakiś niezatopiony statek.

"""

from copy import deepcopy
from random import choice

from statki.plansza import Plansza, Pole, Salwa

# TODO: oczyścić docstringi z bieżących komentarzy i rozważań


class Gra:
    """
    Reprezentacja przebiegu gry na danej planszy. Zapisuje kolejne tury.
    """

    def __init__(self, plansza):
        self.plansza = plansza
        self.tura = Tura(self.plansza)
        self.tury = [self.tura]
        self.ofiary = []  # zatopione statki przeciwnika

    def dodaj_ture(self):
        """Stwórz nową turę i dodaj do listy tur"""
        self.tura = Tura(self.plansza)
        self.tury.append(self.tura)

    def podaj_info_o_rundzie(self):
        """Zwróć informację o rundzie w formacie: `tura #[liczba] / runda #[liczba] ([ilość statków])."""
        info = "tura #" + str(len(self.tury))
        info += " / runda #" + str(len(self.tura.rundy))
        info += " (" + str(len(self.tura.napastnicy)) + ")"
        return info  # w minuskule!

    def zrob_ruch(self):
        """
        Wykonuje ruch dla przeciwnika. Implementacja w klasach potomnych.
        """
        pass


class Tura:
    """
    Reprezentacja przebiegu tury. Zapisuje kolejne rundy i śledzi statki zdolne do ataku w kolejnych rundach. Startuje z listą niezatopionych statków.
    """

    def __init__(self, plansza):
        self.plansza = plansza
        self.migawki_planszy = [deepcopy(self.plansza)]  # +1 koniec każdej rundy
        self.napastnicy = self.plansza.niezatopione[:]  # śledzona jest tylko ilość elementów nie ich zawartość, więc wystarczy płytka kopia
        self.runda = Runda(self.napastnicy[0])
        self.rundy = [self.runda]

    def dodaj_runde(self):
        """Stwórz nową rundę i dodaj do listy rund"""
        self.napastnicy.remove(self.runda.napastnik)
        self.migawki_planszy.append(deepcopy(self.plansza))
        self.runda = Runda(self.napastnicy[0])
        self.rundy.append(self.runda)

    def filtruj_zatopione(self):
        """Filtruj z listy napastników statki zatopione w ostatniej rundzie przez przeciwnika."""
        aktualni_napastnicy = [napastnik for napastnik in self.napastnicy if napastnik not in self.plansza.zatopione]
        self.napastnicy = aktualni_napastnicy


class Runda:
    """
    Reprezentacja przebiegu rundy. Śledzi aktualnego napastnika i zapisuje salwy, które oddał oraz salwy otrzymane od przeciwnika. Startuje z pierwszym statkiem z listy napastników tury.
    """

    def __init__(self, statek):
        self.napastnik = statek
        self.sila_ognia = self.napastnik.sila_ognia[:]
        self.salwy_oddane = []
        self.salwy_otrzymane = []  # lista salw przeciwnika otrzymywana i zapisywana na początku rundy
        # flagi
        self.mozna_zmienic_napastnika = True
        self.mozna_atakowac = True

    def ustaw_napastnika(self, statek):
        """Ustaw podany statek jako aktualnego napastnika i jego siłę ognia jako aktualną dla rundy."""
        self.napastnik = statek
        self.sila_ognia = self.napastnik.sila_ognia[:]

    def dodaj_salwe_oddana(self, salwa):
        """Dodaj salwę, aktualizuj siłę ognia."""
        self.salwy_oddane.append(salwa)
        self.sila_ognia.remove(len(salwa))


class AI(Gra):
    """
    Reprezentacja przebiegu gry na danej planszy w wykonaniu komputera.

    Szkielet działania:
    ~~~~~~~~~~~~~~~~~~~
    1. Wybór napastnika.
    2. Wybór celu i orientacji salwy (polowanie lub celowanie).
    3. Oddanie salwy.
    Punkty 2-4 powtarzane są tak długo jak długo są salwy do oddania.

    To AI dokonuje prostych, losowych wyborów. Bardziej zaawansowana implementacja w klasach potomnych.
    """

    KIERUNKI_SALWY = {
        Salwa.ORIENTACJE.C: [],
        Salwa.ORIENTACJE.E: [Plansza.KIERUNKI.E],
        Salwa.ORIENTACJE.S: [Plansza.KIERUNKI.S],
        Salwa.ORIENTACJE.W: [Plansza.KIERUNKI.W],
        Salwa.ORIENTACJE.N: [Plansza.KIERUNKI.N],
        Salwa.ORIENTACJE.WE: [Plansza.KIERUNKI.E, Plansza.KIERUNKI.W],
        Salwa.ORIENTACJE.NS: [Plansza.KIERUNKI.S, Plansza.KIERUNKI.N],
        Salwa.ORIENTACJE.NE: [Plansza.KIERUNKI.E, Plansza.KIERUNKI.N],
        Salwa.ORIENTACJE.SE: [Plansza.KIERUNKI.E, Plansza.KIERUNKI.S],
        Salwa.ORIENTACJE.SW: [Plansza.KIERUNKI.S, Plansza.KIERUNKI.W],
        Salwa.ORIENTACJE.NW: [Plansza.KIERUNKI.W, Plansza.KIERUNKI.N]
    }
    ODWIEDZONE = (Pole.ZNACZNIKI.pudlo, Pole.ZNACZNIKI.trafiony, Pole.ZNACZNIKI.zatopiony)

    def __init__(self, plansza_wlasna, plansza_gracza):
        super().__init__(plansza_wlasna)
        self.druga_plansza = deepcopy(plansza_gracza)

    def mysl(self):
        """
        Wybierz strategię ataku: polowanie (atak bez wcześniejszego trafienia) albo celowanie (atak po wcześniejszym trafieniu).
        """
        znaczniki = [pole.znacznik for rzad in self.druga_plansza.pola for pole in rzad]
        if Pole.ZNACZNIKI.trafiony in znaczniki:
            self.celuj()
        else:
            self.poluj()

    def poluj(self):
        """
        Atakuj, gdy nie wiesz, gdzie jest ofiara. Losuj 'na ślepo' potencjalny cel z wszystkich nieodwiedzonych jeszcze pól i wybierz do niego najlepszą konfigurację.
        """
        # TODO: mocniejsze AI mogłoby najpierw sprawdzić, które spośród wszystkich nieodwiedzonych jeszcze pól dają najlepszą konfigurację i wylosować cel tylko spośród nich
        wielkosc_salwy = self.tura.runda.napastnik.sila_ognia[0]
        pola = [pole for rzad in self.druga_plansza.pola for pole in rzad]
        nieodwiedzone = [pole for pole in pola if pole.znacznik not in self.ODWIEDZONE]
        cel = choice(nieodwiedzone)
        konfiguracja_pol = self.wybierz_konfiguracje_pol(cel)
        self.druga_plansza.odkryj_pola(konfiguracja_pol)
        self.druga_plansza.oznacz_zatopione()
        self.tura.runda.dodaj_salwe_oddana(Salwa(
            self.tura.runda.napastnik.polozenie,
            konfiguracja_pol,
            [None for i in range(wielkosc_salwy - len(konfiguracja_pol))]
        ))

    def celuj(self):
        """
        Atakuj, gdy wiesz, gdzie jest ofiara.

        Szkielet algorytmu
        ~~~~~~~~~~~~~~~~~~
        1. Wybierz największą ofiarę (sprawdź do ilu statków należą wszystkie odkryte, trafione pola i wybierz ten, którego najwięcej pól zostało trafionych).
        2. Sprawdź wszystkie nieodwiedzone pola, które są jednocześnie bezpośrednimi sąsiadami (stykającymi się ortogonalnie - nie na ukos) wszystkich trafionych pól ofiary jako potencjalny cel.
        3. Dla każdego potencjalnego celu wybierz najlepszą konfigurację pól na podstawie dwóch czynników (w podanej kolejności:
            a) ilości rażonych (nieodwiedzonych) pól
            b) ilości trafionych pól ofiary, które stykają się bezpośrednio (2 punkty) lub na ukos (1 punkt) z wszystkimi polami danej konfiguracji
        4. Spośród tak wybranych konfiguracji wybierz najlepszą (kolejny raz stosując tę samą ocenę (a) i b)).

        """
        # Mocniejsze AI weźmie pod uwagę trzecią kategorię wyboru - wagę danego pola (ustalaną na podstawie symulacji możliwych ustawień statków na planszy)
        pass

    def wybierz_konfiguracje_pol(self, cel):
        """
        Wybierz najlepszą konfiguracje pól salwy dla wskazanego celu. Przy ocenie weź pod uwagę tylko ilość rażonych (nieodwiedzonych) pól.
        """
        konfiguracje_pol = []
        wielkosc_salwy = self.tura.runda.napastnik.sila_ognia[0]
        if wielkosc_salwy == 1:
            konfiguracje_pol.append([cel])
        elif wielkosc_salwy == 2:
            for orientacja in Salwa.ORIENTACJE[1:5]:
                konfiguracje_pol.append(self.podaj_konfiguracje_pol(cel, self.KIERUNKI_SALWY[orientacja]))
        elif wielkosc_salwy == 3:
            for orientacja in Salwa.ORIENTACJE[5:]:
                konfiguracje_pol.append(self.podaj_konfiguracje_pol(cel, self.KIERUNKI_SALWY[orientacja]))

        return sorted(konfiguracje_pol, key=lambda kp: len([True for pole in kp if pole.znacznik not in self.ODWIEDZONE]), reverse=True)[0]

    def podaj_konfiguracje_pol(self, cel, kierunki):
        """
        Podaj konfigurację pól salwy wg podanego celu. Pierwsze pole konfiguracji to pole celu, pozostałe dobierane są na podstawie wskazanych kierunków.
        """

        # termin 'orientacja salwy' zarezerwowany jest dla stałej klasy 'statki.plansza.Salwa'. 'Konfiguracja pól' natomiast to pola planszy odpowiadające danej orientacji, z których jeszcze nie został utworzony obiekt klasy 'statki.plansza.Salwa'
        konfiguracja_pol = [cel]
        for kierunek in kierunki:
            sasiad = self.druga_plansza.podaj_sasiednie_pole(cel, kierunek)
            if sasiad is not None:
                konfiguracja_pol.append(sasiad)
        return konfiguracja_pol

    def wybierz_napastnika(self):
        """
        Wybierz napastnika. Wybierany jest statek posiadający największą siłę ognia w danej rundzie.
        """
        napastnik = sorted(self.tura.napastnicy, key=lambda s: sum(s.sila_ognia), reverse=True)[0]
        self.tura.runda.ustaw_napastnika(napastnik)

    def zrob_ruch(self):
        """
        Wykonaj ruch (wybierz napastnika, wymyśl i oddaj salwę/-y, dodaj kolejną rundę/turę).
        """
        self.wybierz_napastnika()
        while len(self.tura.runda.sila_ognia) > 0:
            self.mysl()
        self.dodaj_ture() if len(self.tura.napastnicy) == 1 else self.tura.dodaj_runde()


class MocneAI(AI):
    """
    AI wykorzystujące do polowania i celowania symulację statystycznego występowania statków na planszy.
    """

    # inspiracja algorytmu pochodzi z tego artykułu dotyczącego zwyczajnych Statków (w wersji amerykańskiej - statki tylko 2-5 pól, ortogonalnie, możliwość stykania się): http://www.datagenetics.com/blog/december32011/index.html
    def __init__(self, plansza_wlasna, plansza_gracza):
        super().__init__(plansza_wlasna)
        self.druga_plansza = deepcopy(plansza_gracza)

    def wybierz_konfiguracje_pol(self, cel):
        """
        Wybiera najlepszą orientację salwy dla wskazanego celu. Przy ocenie bierze pod uwagę tylko ilość rażonych pól.
        """
        pass  # TODO: przeładowanie metody rodzica


class GraSieciowa(Gra):  # TODO
    """
    Przebieg gry na danej planszy w wykonaniu drugiego gracza połączonego przez sieć.
    """

    def __init__(self, plansza_wlasna, plansza_gracza):
        super().__init__(plansza_wlasna)
        self.druga_plansza = deepcopy(plansza_gracza)

    def zrob_ruch(self):
        """
        Wykonaj ruch (wybierz napastnika, wymyśl i oddaj salwę/-y, dodaj kolejną rundę/turę).
        """
        pass

    def pobierz_salwy_oddane(self):
        """
        Pobierz przez sieć salwy oddane przez drugiego gracza.
        """
        pass
