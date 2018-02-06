## GUI

1. [ZROBIONE] <del>PlanszaGUI powinna być pochodną ttk.Frame i zawierać tylko obiekty klas ttk.Label i ttk.Button zorganizowane mniej więcej tak jak teraz. Przy ekranie 1920x1200 sensowne wymiary (jednej) planszy to od 5x5 do 50x30, przy dwóch planszach (gracz+przeciwnik) to 5x5 do 25x30, przy czym minimalny rozmiar powinien prawdopodobnie być większy ze względów na konieczność miejsca na elementy kontrolne interfejsu na prawo od plansz.</del>

2. [ZROBIONE] <<del>W głównej ramce powinny znajdować się dwa obiekty PlanszaGUI - 1 dla własnych statków, drugi dla statków przeciwnika (jak w klasycznej grze).</del>

3. Na prawo od obu plansz powinna znajdować się ramka z widgetami kontrolującymi przebieg gry i zwracającymi informację o nim. Składająca się z 3 sekcji:
    * A.[ZROBIONE] <del>ramki ataku (układ minimum: 3 comboboksy: 1) wyboru statku, 2) wyboru salwy i 3) wyboru orientacji).</del>
    * B.ramki floty (listy statków) - swojej i przeciwnika. Prawdopodobnie najlepszą implementacją będzie Treeview zamknięte w Notebooku.
    * C.ramki ogólnej informacji o grze (która tura/runda, kto wygrywa (np. procent nietrafionych pól każdego gracza) oraz przycisk Koniec Rundy - najprostsza implementacja, wystarczy kilka etykiet i jeden przycisk.

4. Na dole okna głównego powinna znajdować się ramka z polem tekstowym wypluwającym historię gry - krótki opis kolejnych rund (jaki statek strzela gdzie i z jakim skutkiem + informacje o zatopieniu kolejnych statków).

5. Główne okno powinno być skalowalne ale jego powiększanie w dół powinno powiększać tylko ramkę dolną (albo głównie ramkę dolną oraz ramkę 3B (listę statków) z sekcji kontrolnej po prawo) a powiększanie w prawo tylko ramkę prawą.

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

8. Pola planszy (wszystkie: nieodkryte, wody, statków (niezatopionych i zatopionych), oddanych salw (trafień i pudeł)) powinny mieć tooltipy z informacjami, jednak pojawiające się tylko po określonym czasie bezruchu kursora (podobnie jak w Civ5).

9. Plansza Gracza:

    * [ZROBIONE] <<del>Przewijanie statków klawiszami '[',']'</del>

9. Plansza Przeciwnika.

    * [ZROBIONE] <del>Dokończyć obracanie podświetlaniem (dołożyć pełen obród 2-polowej salwy)</del>
    * wyróżnianie zatopionych statków po wyborze w drzewie Kontroli Floty

10. Kontrola Floty:

    1. Drzewo.
        * [ZROBIONE] <del>Scrollbary</del>
        * [ZROBIONE] <del>Automatyczne przesuwanie widoku na wybrany element (teraz jeśli przewijając wybierze się statek poza widokiem to pozostaje niewidoczny)</del>
        * [ZROBIONE] <del>Prawidłowe ustawienie na gridzie</del>
        * [ZROBIONE] <del>Przesunięcie drzewa do osobnej klasy</del>
        * Notebook i drzewo statków przeciwnika
        * Sortowanie kolumn - wg nazwy, wg pozycji i wg ilości nietrafionych pól (każde sortowanie odbywa się osobno w każdej kategorii)
        * Obsługa możliwości wyboru tylko statków, które jeszcze nie miały swojej rundy w danej turze
        * Obsługa zatapiania (odpowiednie formatowanie tej sekcji) ==> do dołożenia później, w trakcie prac nad mechaniką
        * Obsługa dodawania zatopionych statków (odpowiednie formatowanie tej sekcji) ==> do dołożenia później, w trakcie prac nad mechaniką
        * Etykiety pod drzewem ==> decyzja czy potrzebne później

    2. Przyciski Poprzedni/Kolejny Statek + Etykieta Wyboru

    3. Schemat zagnieżdżonego layoutu:

        [1] Okno Główne (Tk) >> [2] GraGUI (Frame) >> [3] Kontrola Floty (Frame) >> [4] etyramka (LabelFrame) >> [5] notes (Notebook) >> [6] ramka (Frame) >> [7] drzewo (Treeview)

11. Kontrola Gry. Dokładnie rozrysować.

12. Pasek stanu.

    * wyświetlanie w jednej linii zmieniającego się położenia kursora na każdej z plansz


13. Grid - całość. Aktualnie jest w miarę OK, ale wystarczy zmienić rozmiar na mniejszy od maksymalnego i cała Kontrola Ataku znika.

14. Całość - drobne.

    * przenieść kod pogrubiający czcionkę etyramek wszystkich sekcji do okna głównego

## MECHANIKA

Ogólna struktura OOP modułów:

plansza.py <<--->> mechanika.py <<--->> gui.py

  (stan)            (proces)          (interfejs)

  (dane)       (zapis/komunikacja)   (input/output)
