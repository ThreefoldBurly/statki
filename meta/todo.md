## GUI

1. [ZROBIONE] <del>PlanszaGUI powinna być pochodną ttk.Frame i zawierać tylko obiekty klas ttk.Label i ttk.Button zorganizowane mniej więcej tak jak teraz. Przy ekranie 1920x1200 sensowne wymiary (jednej) planszy to od 5x5 do 50x30, przy dwóch planszach (gracz+przeciwnik) to 5x5 do 25x30, przy czym minimalny rozmiar powinien prawdopodobnie być większy ze względów na konieczność miejsca na elementy kontrolne interfejsu na prawo od plansz.</del>

2. [ZROBIONE] <<del>W głównej ramce powinny znajdować się dwa obiekty PlanszaGUI - 1 dla własnych statków, drugi dla statków przeciwnika (jak w klasycznej grze).</del>

3. [ZROBIONE] <del>Na prawo od obu plansz powinna znajdować się ramka z widgetami kontrolującymi przebieg gry i zwracającymi informację o nim. Składająca się z 3 sekcji:
    * A.ramki ataku (układ minimum: 3 comboboksy: 1) wyboru statku, 2) wyboru salwy i 3) wyboru orientacji).
    * B.ramki floty (listy statków) - swojej i przeciwnika. Prawdopodobnie najlepszą implementacją będzie Treeview zamknięte w Notebooku.
    * C.ramki ogólnej informacji o grze (która tura/runda, kto wygrywa (np. procent nietrafionych pól każdego gracza) oraz przycisk Koniec Rundy - najprostsza implementacja, wystarczy kilka etykiet i jeden przycisk.</del>

4. [ZROBIONE] <del>Na dole okna głównego powinna znajdować się ramka z polem tekstowym wypluwającym historię gry - krótki opis kolejnych rund (jaki statek strzela gdzie i z jakim skutkiem + informacje o zatopieniu kolejnych statków).</del>

5. Skalowanie interfejsu. Główne okno powinno być skalowalne ale jego powiększanie w dół powinno powiększać tylko ramkę dolną (albo głównie ramkę dolną oraz ramkę 3B (listę statków) z sekcji kontrolnej po prawo) a powiększanie w prawo tylko ramkę prawą.

6. Do powyższego należy dołożyć proste menu i 2 okna dialogowe:
    * A. rozpoczęcia gry z ustawieniami początkowymi (przy grze sieciowej inna dla gracza-gospodarza, inna dla gracza-gościa).
    * B. zakończenia gry z informacją podsumowującą jej przebieg i opcją wyjścia/restartu.

7. [ZROBIONE] <<del>Pola statków na własnej planszy powinny mieć literowe oznaczenia rangi:

- T: kuter
- L: patrolowiec
- W: korweta
- F: fregata
- N: niszczyciel
- K: krążownik
- P: pancernik

Te oznaczenia powinny pojawiać się również na planszy przeciwnika, ale tylko na polach zatopionych statków.</del>

8. Tooltipy. Pola planszy (wszystkie: nieodkryte, wody, statków (niezatopionych i zatopionych), oddanych salw (trafień i pudeł)) powinny mieć tooltipy z informacjami, jednak pojawiające się tylko po określonym czasie bezruchu kursora (podobnie jak w Civ5).

9. Plansza Gracza:

    * [ZROBIONE] <del>Przewijanie statków klawiszami '[',']'</del>
    * [ZROBIONE] <del>Dodatkowe graficzne wyróżnienie statków, które nie mogą strzelać w danej rundzie</del>

9. Plansza Przeciwnika.

    * [ZROBIONE] <del>Dokończyć obracanie podświetlaniem (dołożyć pełen obrót 2-polowej salwy)</del>
    * wyróżnianie zatopionych statków po wyborze w drzewie Kontroli Floty

10. Kontrola Floty:

    1. Drzewo.

        * [ZROBIONE] <del>Scrollbary</del>
        * [ZROBIONE] <del>Automatyczne przesuwanie widoku na wybrany element (teraz jeśli przewijając wybierze się statek poza widokiem to pozostaje niewidoczny)</del>
        * [ZROBIONE] <del>Prawidłowe ustawienie na gridzie</del>
        * [ZROBIONE] <del>Przesunięcie drzewa do osobnej klasy</del>
        * [ZROBIONE] <del>Notebook i drzewo statków przeciwnika</del>
        * Sortowanie kolumn - wg nazwy, wg pozycji i wg ilości nietrafionych pól (każde sortowanie odbywa się osobno w każdej kategorii) ==> TODO
        * [ZROBIONE] <del>Obsługa możliwości wyboru tylko statków, które jeszcze nie miały swojej rundy w danej turze ==> TODO w trakcie prac nad mechaniką</del>
        * Obsługa zatapiania (odpowiednie formatowanie tej sekcji) ==> TODO w trakcie prac nad mechaniką
        * Obsługa dodawania zatopionych statków (odpowiednie formatowanie tej sekcji) ==> TODO w trakcie prac nad mechaniką
        * [ZROBIONE]<del>WAŻNE: dodać kolumnę SALWY (ilość salw danego statku zmienia się w trakcie gry - jak na razie ta informacja jest śledzona tylko przez sekcje Kontroli Ataku)</del>


    2. [ZROBIONE] <del>Przyciski Poprzedni/Kolejny Statek</del>
        * [ZROBIONE] <del>wyświetlanie zmieniającego się położenia kursora na planszy gracza - najlepiej na etykiecie pomiędzy przyciskami przewijania</del>

    3. Schemat zagnieżdżonego layoutu:

        [1] Okno Główne (Tk) >> [2] GraGUI (Frame) >> [3] Kontrola Floty (Frame) >> [4] etyramka (LabelFrame) >> [5] notes (Notebook) >> [6] ramka (Frame) >> [7] drzewo (Treeview)

        [3] + [4] = `Sekcja`

11. Kontrola Gry.

    * [ZROBIONE] <del>Podstawowy wygląd</del>
    * [ZROBIONE] <del>Powiązanie z mechanika.py</del>
    * [ZROBIONE] <del>Kontrola pozostałych sekcji</del>

12. Pasek komunikatów.

    * [ZROBIONE] <del>Sterowanie via `Komunikator`</del>

13. Grid - całość.

    * [ZROBIONE] <del>Ustawienie kolumny prawej (sekcje kontroli) tak by o rozmieszczeniu wzajemnym sekcji decydowała głównie wysokość sekcji kontroli floty - uzależniona od wybranego rozmiaru planszy</del>
    * Przy wysokości planszy 10-11 wierszy (a być może nawet 10-15 (ze względu na czytelność drzewa w sekcji kontroli ataku)) muszą się automatycznie zmieniać ustawienia siatki głównego okna. Powyżej tego zakresu plansza jest na tyle duża że ma sens by sekcja kontroli gry zajmowała dwa dolne rzędy siatki (a pasek komunikatów jeden). Poniżej tego zakresu plansza jest na tyle mała, że o wiele sensowniejsze jest gdy to pasek komunikatów zajmuje 2 dolne rzędy siatki a sekcja kontroli gry tylko jeden.
    * Testy pod Windowsem

14. Całość.

    * **Dopuszczalny rozmiar planszy: 8-26 kolumn x 8-30 rzędów**
    * [ZROBIONE] <del>Przenieść kod pogrubiający czcionkę etyramek wszystkich sekcji do okna głównego</del>(
    przeniesione do klasy Sekcja, z której reszta dziedziczy)

----

## MECHANIKA

Ogólna struktura OOP modułów:

plansza.py <<--->> mechanika.py <<--->> gui.py

  (stan)            (proces)          (interfejs)

  (dane)       (zapis/komunikacja)   (input/output)

----

#### ZMIANA STATKU [ZROBIONE]

Zmiana wybranego statku odbywa się na kilka sposobów:

1. Poprzez kliknięcie na statku w Planszy Gracza.
2. Poprzez naciśnięcie przycisku "[" lub "]" na klawiaturze (bedąc gdziekolwiek w aplikacji).
3. Poprzez wybór z listy comboboksu Kontroli Ataku.
4. Poprzez podwójne kliknięcie w drzewie Kontroli Floty.
5. Poprzez kliknięcie przycisków zmiany statku w Kontroli Floty.

We wszystkich ww. przypadkach zmiana dokonywana jest przez wywołanie metody `zmien_statek(statek)` klasy `PlanszaGracza`, która wygląda tak:

`if statek and not statek.czy_zatopiony():
    self.kasuj_wybor_statku(self.gracz.tura.runda.napastnik)
    self.wybierz_statek(statek)`

`kasuj_wybor_statku()` pobiera aktualny statek rundy, a `wybierz_statek()` ustala statek podany do `zmien_statek` jako nowy aktualny statek rundy.

Przyjrzyjmy się w takim razie, co dokładnie jest podawane metodzie `zmien_statek()` we wszystkich jej wywołaniach. Tym bardziej, że zakażdym razem sprawdza czy w ogóle dostała coś innego niż obiekt fałszywy.

1. Jeżeli aktualna runda nie ma blokady zmiany, podaje statek wg współrzędnych klikniętego pola. [BŁĄD - powinny być brane pod uwagę tylko statki znajdujące się w liście aktualnej tury (czyli te które jeszcze nie strzelały w tej turze)].

2. Jeśli aktualna runda nie ma blokady zmiany i jeśli jest co wybierać (lista statków aktualnej tury jest większa niż 1), podaje kolejny lub poprzedni względem aktualnego statek z listy aktualnej tury [DOBRZE]

3. Bez warunków (blokada zmiany jest zakładana na wyższym poziomie na całego widżeta) podaje statek z listy aktualnej tury odpowiadający statkowi klikniętemu w comboboksie [DOBRZE].

4. Jeżeli aktualna runda nie ma blokady zmiany, podaje statek z listy aktualnej tury na podstawie kolejności wprowadzania statków do drzewa [BŁĄD - raz że statki są wprowadzane do drzewa na poczatku gry wg listy niezatopionych w planszy a nie na podstawie listy tury, a dwa taka translacja się rozjedzie zaraz po pierwszej rundzie - trzeba znaleźć metodę na wydobycie statku z drzewa na podstawie najlepiej stringowej reprezentacji jego położenia, która jest zapisywana w drzewie i jest unikalna dla danej planszy, ewentualnie na podstawie nazwy statku, która powinna teoretycznie być unikalna dla całej gry]

5. == 2.

Jeśli za każdym razem zostanie zapewnione, że nie ma blokady zmiany statku w rundzie i że podany jest na liście statków aktualnej tury - statek powinien być móc wybrany. Stąd wynika że ten warunek (i tylko ten) powinien być zawarty w metodzie `zmien_statek()` klasy `PlanszaGracza`.

----

#### AI

Zremby algorytmu oparte na artykule dotyczącym zwyczajnych Statków (w wersji amerykańskiej - statki tylko 2-5 pól, ortogonalnie, możliwość stykania się): http://www.datagenetics.com/blog/december32011/index.html

Szkielet działania:
1. Wybór napastnika.
2. Wybór celu i orientacji salwy (polowanie lub celowanie).
3. Oddanie salwy.
Punkty 2-4 powtarzane są tak długo jak długo są salwy do oddania.

Ad 1. Wybór napastnika - statek z o największej sile ognia w danej rundzie.
Ad 2. Wybór salwy - polowanie lub celowanie:
        <del>Algorytm powinien brać pod uwagę:
        1. wybrane na początku gry ustawienia dotyczące umieszczania statków na planszy (parametry rozkładu Gaussa losowania rozmiaru statku)
        2. algorytm umieszczania statków (brak stykania się)
        Na podstawie 1) powinna odbyć się symulacja najbardziej prawdopodobnych wybranych rozmiarów i ilości statków przeciwnika.</del>
        Wystarczy przeprowadzić symulację umieszczania statków na planszy wg wybranych wcześniej w grze parametrów i zapisać ilość wystąpień pola statku w danej lokalizacji planszy. Mając taką mapę aproksymującą statystyczne występowanie statków na planszy będzie można zarówno wybrać za każdym razem najlepszy cel polowania jak i przy celowaniu ocenić wszystkie możliwe do oddania salwy.
