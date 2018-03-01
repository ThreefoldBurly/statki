"""

    statki.mechanika
    ~~~~~~~~~~~~~~~~

    Mechanika i przebieg gry w rozbiciu na tury i rundy - wg opisu zawartego w meta/zasady.md. Gra składa się z tur, które składają się z rund. Runda odpowiada atakowi pojedynczego statku na pola planszy przeciwnika podzielonemu na salwy. Ilość salw oddawanych przez statek w rundzie zależy od jego aktualnej siły ognia. Tura składa się z tylu rund ile statków na planszy może atakować (nie są zatopione). Gra składa się z tak wielu tur, jak wiele razy po wykonaniu wszystkich ataków na planszy atakującego gracza pozostał jeszcze jakiś niezatopiony statek.

"""

from copy import deepcopy


class Gra:
    """
    Abstrakcyjna reprezentacja przebiegu gry na danej planszy. Zapisuje kolejne tury.
    """

    def __init__(self, plansza):
        self.plansza = plansza
        self.tura = Tura(self.plansza)
        self.tury = [self.tura]
        self.ofiary = []  # zatopione statki przeciwnika

    def dodaj_ture(self):
        """Tworzy nową turę i dodaje do listy tur"""
        self.tura = Tura(self.plansza)
        self.tury.append(self.tura)

    def podaj_info_o_rundzie(self):
        """Zwraca informację o rundzie w formacie: `tura #[liczba] / runda #[liczba] ([ilość statków])."""
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
    Abstrakcyjna reprezentacja tury. Zapisuje kolejne rundy i śledzi statki zdolne do ataku w kolejnych rundach. Startuje z listą niezatopionych statków.
    """

    def __init__(self, plansza):
        self.plansza = plansza
        self.migawki_planszy = [deepcopy(self.plansza)]  # +1 koniec każdej rundy
        self.napastnicy = self.plansza.niezatopione[:]  # śledzona jest tylko ilość elementów nie ich zawartość, więc wystarczy płytka kopia
        self.runda = Runda(self.napastnicy[0])
        self.rundy = [self.runda]

    def dodaj_runde(self):
        """Tworzy nową rundę i dodaje do listy rund"""
        self.napastnicy.remove(self.runda.napastnik)
        self.migawki_planszy.append(deepcopy(self.plansza))
        self.runda = Runda(self.napastnicy[0])
        self.rundy.append(self.runda)

    def filtruj_zatopione(self):
        """Filtruje z listy napastników statki zatopione w ostatniej rundzie przez przeciwnika."""
        aktualni_napastnicy = [napastnik for napastnik in self.napastnicy if napastnik not in self.plansza.zatopione]
        self.napastnicy = aktualni_napastnicy


class Runda:
    """
    Abstrakcyjna reprezentacja rundy. Śledzi atakujący statek i zapisuje salwy, które oddał oraz salwy otrzymane od przeciwnika. Startuje z pierwszym statkiem z listy tury.
    """

    def __init__(self, statek):
        self.napastnik = statek  # wartość zmieniana przez użytkownika via GUI
        self.sila_ognia = self.napastnik.sila_ognia[:]
        self.salwy_oddane = []
        self.salwy_otrzymane = []  # lista salw przeciwnika otrzymywana i zapisywana na początku rundy
        # flagi
        self.mozna_zmienic_napastnika = True
        self.mozna_atakowac = True

    def ustaw_napastnika(self, statek):
        """Ustawia podany statek jako aktualnego napastnika i jego siłę ognia jako aktualną dla rundy."""
        self.napastnik = statek
        self.sila_ognia = self.napastnik.sila_ognia[:]

    def dodaj_salwe_oddana(self, salwa):
        """Dodaje salwę, aktualizuje siłę ognia."""
        self.salwy_oddane.append(salwa)
        self.sila_ognia.remove(len(salwa))


class AI(Gra):
    """
    Abstrakcyjna reprezentacja przebiegu gry na danej planszy w wykonaniu komputera.

    Zremby algorytmu oparte na artykule dotyczącym zwyczajnych Statków (w wersji amerykańskiej - statki tylko 2-5 pól, ortogonalnie, możliwość stykania się): http://www.datagenetics.com/blog/december32011/index.html

    Szkielet działania:
    ~~~~~~~~~~~~~~~~~~~
    1. Wybór napastnika.
    2. Wybór salwy.
    3. Wybór ofiary - polowanie lub celowanie.
    4. Oddanie salwy.
    Punkty 2-4 powtarzane są tak długo jak długo są salwy do oddania.

    """

    def __init__(self, plansza_wlasna, plansza_gracza):
        super().__init__(plansza_wlasna)
        self.druga_plansza = deepcopy(plansza_gracza)

    def mysl(self):
        """
        Myśli, jakie salwy wykonać w tej rundzie.
        """
        pass

    def poluj(self):
        """
        Poluje na ofiarę - czyli wybiera i zwraca najlepsze możliwe miejsce na oddanie salwy, gdy nie ma żadnej trafionej ofiary.
        """
        pass

    def celuj(self):
        """
        Wybiera i zwraca najlepsze możliwe miejsce na oddanie salwy, gdy jest jakaś trafiona ofiara.
        """
        pass

    def wybierz_napastnika(self):
        """
        Wybiera atakujący statek. Wybierany jest statek posiadający największą siłę ognia w danej rundzie.
        """
        napastnik = sorted(self.tura.napastnicy, key=lambda s: sum(s.sila_ognia), reverse=True)[0]
        self.tura.runda.ustaw_napastnika(napastnik)

    def zrob_ruch(self):
        """
        Wykonuje ruch dla przeciwnika. Wymyśla salwy i dodaje rundę/turę.
        """
        pass

# TODO


class GraSieciowa(Gra):
    """
    Abstrakcyjna reprezentacja przebiegu gry na danej planszy w wykonaniu drugiego gracza połączonego przez sieć.
    """

    def __init__(self, plansza_wlasna, plansza_gracza):
        super().__init__(plansza_wlasna)
        self.druga_plansza = deepcopy(plansza_gracza)

    def zrob_ruch(self):
        """
        Wykonuje ruch dla przeciwnika. Pobiera salwy przez sieć od drugiego gracza i dodaje rundę/turę.
        """
        pass

    def pobierz_salwy_oddane(self):
        """
        Pobiera przez sieć salwy oddane przez drugiego gracza.
        """
        pass
