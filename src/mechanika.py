"""
Mechanika i przebieg gry w rozbiciu na tury i rundy - wg opisu zawartego w meta/zasady.md. Gra składa się z tur, które składają się z rund. Runda odpowiada atakowi pojedynczego statku na pola planszy przeciwnika podzielonemu na salwy. Ilość salw oddawanych przez statek w rundzie zależy od jego aktualnej siły ognia. Tura składa się z tylu rund ile statków na planszy może atakować (nie są zatopione). Gra składa się z tak wielu tur, jak wiele razy po wykonaniu wszystkich ataków na planszy atakującego gracza pozostał jeszcze jakiś niezatopiony statek.
"""

from copy import deepcopy

# TODO: mechanika przejścia w nową turę gdy liczba statków w rundzie == 1 (powinna być ujęta w metodzie `dodaj_runde()` i mimo że dotyczy głównie rundy (i jest aktualnie częścią Rundy), musi być wywoływana z gry)


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
        info += " (" + str(len(self.tura.statki)) + ")"
        return info  # w minuskule!


class Tura:
    """
    Abstrakcyjna reprezentacja tury. Zapisuje kolejne rundy i śledzi statki zdolne do ataku w kolejnych rundach. Startuje z listą niezatopionych statków.
    """

    def __init__(self, plansza):
        self.plansza = plansza
        self.migawki_planszy = []  # wykonywane na koniec każdej rundy
        self.statki = self.plansza.niezatopione[:]  # śledzona jest tylko ilość elementów nie ich zawartość, więc wystarczy płytka kopia
        self.runda = Runda(self.statki[0])
        self.rundy = [self.runda]

    def dodaj_runde(self):
        """Tworzy nową rundę i dodaje do listy rund"""
        self.statki.remove(self.runda.statek)
        self.migawki_planszy.append(deepcopy(self.plansza))
        self.runda = Runda(self.statki[0])
        self.rundy.append(self.runda)

    def filtruj_zatopione(self):
        """Filtruje z listy statków statki zatopione w ostatniej rundzie przez przeciwnika."""
        aktualne_statki = [statek for statek in self.statki if statek not in self.plansza.zatopione]
        self.statki = aktualne_statki


class Runda:
    """
    Abstrakcyjna reprezentacja rundy. Śledzi atakujący statek i zapisuje salwy, które oddał oraz salwy otrzymane od przeciwnika. Startuje z pierwszym statkiem z listy tury.
    """

    def __init__(self, statek, salwy_otrzymane=None):
        self.statek = statek  # wartość zmieniana przez użytkownika via GUI
        self.sila_ognia = self.statek.sila_ognia[:]
        self.salwy_oddane = []
        self.salwy_otrzymane = salwy_otrzymane  # TODO: lista salw przeciwnika otrzymywana i zapisywana na początku rundy
        # flagi
        self.mozna_zmienic_statek = True
        self.mozna_atakowac = True

    def ustaw_statek(self, statek):
        """Ustawia podany statek i jego siłę ognia jako aktualne dla rundy."""
        self.statek = statek
        self.sila_ognia = statek.sila_ognia[:]
